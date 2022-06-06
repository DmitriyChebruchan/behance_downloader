build:
	poetry build

publish:
	poetry publish --dry-run -u ' ' -p ' '

install:
	python3 -m pip install --user dist/*.whl

package-install:
	python3 -m pip install --force-reinstall --user dist/*.whl


update:
	make build
	make publish
	make package-install

lint:
	@poetry run flake8

push:
	make lint
	git add .
	git commit -m '$(M)'
	git push

run:
	poetry run page-loader https://google.com