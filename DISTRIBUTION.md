```bash
deactivate
python3.10 -m build --sdist --wheel
twine check dist/*
twine upload -r testpypi dist/*
```