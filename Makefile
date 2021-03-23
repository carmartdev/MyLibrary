SOURCES = $(wildcard *.py) $(wildcard */*.py)
INTERPRETER = python
MANAGE = $(INTERPRETER) manage.py

runserver:
	$(MANAGE) runserver

tests: behave unit_tests

behave:
	$(MANAGE) behave

unit_tests:
	$(MANAGE) test

tags:
	ctags -f tags -R --fields=+iaS --extras=+q $(SOURCES)

include_tags:
	ctags -f include_tags -R --languages=python --fields=+iaS --extras=+q \
		/usr/lib/python3.8/

recreate_database: store/fixtures/authors.json store/fixtures/books.json
	rm -f db.sqlite3
	$(MANAGE) migrate
	$(MANAGE) loaddata authors
	$(MANAGE) loaddata books

store/fixtures/authors.json:
	rm -f misc/*.json
	cd misc; $(INTERPRETER) create_fixtures.py
	mv misc/*.json store/fixtures/

store/fixtures/books.json: store/fixtures/authors.json

update: | sync_with_git recreate_static

sync_with_git:
	git fetch
	git reset origin/main --hard

recreate_static:
	rm -rf static/
	python manage.py collectstatic

coverage_measure:
	coverage run --source=store --omit=*/tests.py,*/apps.py,*/migrations/* \
		./manage.py test
	coverage report -m

coverage_measure_html:
	coverage run --source=store --omit=*/tests.py,*/apps.py,*/migrations/* \
		./manage.py test
	coverage html
	@xdg-open htmlcov/index.html

clean:
	rm -rf tags include_tags __pycache__ */__pycache__ */*/__pycache__ \
		.mypy_cache */.mypy_cache */*/.mypy_cache .coverage htmlcov static

.PHONY: clean include_tags tags
