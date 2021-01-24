SOURCES = $(wildcard *.py) $(wildcard */*.py)
INTERPRETER = python3

runserver:
	$(INTERPRETER) manage.py runserver

tests: system_tests

system_tests:
	$(INTERPRETER) manage.py behave

tags:
	ctags -f tags -R --fields=+iaS --extras=+q $(SOURCES)

include_tags:
	ctags -f include_tags -R --languages=python --fields=+iaS --extras=+q \
		/usr/lib/python3.7/

clean:
	rm -rf tags include_tags __pycache__ */__pycache__ */*/__pycache__ \
		.mypy_cache */.mypy_cache */*/.mypy_cache .coverage htmlcov

.PHONY: clean include_tags tags
