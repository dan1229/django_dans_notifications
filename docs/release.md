## Packaging

**IMPORTANT:** You MUST update your version number in `setup.cfg` before anything else as this is what actually determines the version!

### CD

To release automatically - go to GitHub Actions and simply run the 'release' phase.

It should ask for a version number of the form "X.X.X" and handle everything.

**NOTE:** even when releasing via CD, you MUST still update your version number in `setup.cfg`!

### Manual

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