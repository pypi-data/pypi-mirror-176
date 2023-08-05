.PHONY: lint-python
lint-python:
	poetry run flake8 hotools tests


.PHONY: format-apply
format-apply:
	poetry run isort .

.PHONY: format-diff
format-diff:
	poetry run isort --diff .
