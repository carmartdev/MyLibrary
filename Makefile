SOURCES = $(wildcard *.py) $(wildcard */*.py)
INTERPRETER = python
MANAGE = $(INTERPRETER) manage.py
NPX = node_modules/.bin

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

update: sync_with_git recreate_static

sync_with_git:
	git fetch
	git reset origin/main --hard

recreate_static: store/static/bootstrap store/static/react store/static/js
	rm -rf static/
	python manage.py collectstatic

store/static/bootstrap:
	wget -O store/static/bootstrap.zip \
		https://github.com/twbs/bootstrap/releases/download/v5.0.0-beta1/bootstrap-5.0.0-beta1-dist.zip
	unzip store/static/bootstrap.zip -d store/static/
	rm store/static/bootstrap.zip
	mv store/static/bootstrap-*/ store/static/bootstrap/

store/static/react:
	wget https://unpkg.com/react@17/umd/react.production.min.js \
		-P store/static/react/
	wget https://unpkg.com/react-dom@17/umd/react-dom.production.min.js \
		-P store/static/react/

store/static/js: $(NPX)/babel $(NPX)/terser react-components/index.js
	mkdir -p store/static/js
	$(NPX)/babel react-components --out-file index.js --presets react-app/prod
	$(NPX)/terser -c -m -o store/static/js/index.js -- index.js
	rm index.js

minify_html: $(NPX)/html-minifier-terser
	$(NPX)/html-minifier-terser --input-dir store/templates/store/ \
		--output-dir store/templates/store-min/ \
		--collapse-whitespace --remove-comments --remove-optional-tags \
		--remove-redundant-attributes --remove-script-type-attributes \
		--remove-tag-whitespace --use-short-doctype --minify-css true \
		--minify-js true
	rm -r store/templates/store/
	mv store/templates/store-min/ store/templates/store/

$(NPX)/babel: | package.json
	npm install babel-cli@6 babel-preset-react-app@3

$(NPX)/terser: | package.json
	npm install terser

$(NPX)/html-minifier-terser: | package.json
	npm install html-minifier-terser

package.json:
	npm init -y

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
		.mypy_cache */.mypy_cache */*/.mypy_cache .coverage htmlcov static \
		store/static/js

.PHONY: clean include_tags tags
