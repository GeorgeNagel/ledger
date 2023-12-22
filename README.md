# Ledger

A proof of concept of double-entry bookkeeping in Django

# Installation

This project has been tested using python 3.10

Get python 3.10
```
brew install pyenv
# Finish pyenv setup instructions to add python to PATH
# https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv
pyenv install 3.10
pyenv local 3.10
```

Install python requirements
```
# Create a virtualenv
python -m venv venv
# Activate the virtualenv
source venv/bin/activate
# Install Python package requirements
pip install -r requirements.txt
```

# Run the server

```
python manage.py runserver
```

# Run the test suite

```
python manage.py test
```
