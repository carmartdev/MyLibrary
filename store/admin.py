from functools import reduce
from pprint import pformat
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils.safestring import mark_safe
from .models import Author, Book


class BookAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Key", {"fields": ["key"], "classes": ["collapse"]}),
        ("Book details", {"fields": ("title", "authors", "description",
                                     "cover")}),
        ("Price", {"fields": ["price"]}),
        ("Publish information", {"fields": ("publisher", "publish_date")}),
        ("ISBN", {"fields": ("isbn_10", "isbn_13")}),
    )
    list_display = ("title", "_authors", "publish_date", "isbn_10", "isbn_13",
                    "price",)
    filter_horizontal = ("authors",)
    search_fields = ("title", "authors__name", "publish_date", "isbn_10",
                     "isbn_13", "price",)


class SessionAdmin(admin.ModelAdmin):
    readonly_fields = ("_session_data_formatted",)
    exclude = ("session_data", "session_key",)
    list_display = ("_session_data", "expire_date")

    def get_queryset(self, request):
        def filter_out_staff(sessions):
            """Filter out staff sessions to prevent cookie hijacking attack."""
            anonymous = None
            non_staff_sessions = set()
            for session in sessions:
                user_id = session.get_decoded().get("_auth_user_id")
                user = User.objects.get(id=user_id) if user_id else anonymous
                if user is anonymous or not user.is_staff:
                    non_staff_sessions.add(session.session_key)
            return sessions.filter(session_key__in=non_staff_sessions)

        return filter_out_staff(super().get_queryset(request))

    def _session_data(self, session):
        return session.get_decoded()

    def _session_data_formatted(self, session):
        return mark_safe(reduce(lambda a, old_new: a.replace(*old_new),
                                (("\n", "<br>\n"), ("    ", "&emsp;")),
                                pformat(session.get_decoded(), indent=4)))


admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(Session, SessionAdmin)
