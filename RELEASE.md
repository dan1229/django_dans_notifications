## Packaging

To build run:

```bash
python setup.py sdist
python setup.py bdist_wheel
```

To release run:

```bash
python3 -m twine upload --repository pypi dist/*
```

This expects you to have the proper credentials in your `$HOME/.pypirc` file