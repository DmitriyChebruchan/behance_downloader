build:
	poetry build

lint:
	poetry run flake8

push:
	make lint
	git add .
	git commit -m '$(M)'
	git push