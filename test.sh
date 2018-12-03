pytest -s
python -m doctest README.md
black -l 80 . --check
isort -rc . --check-only
