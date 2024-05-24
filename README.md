# Debt Warn System
> This system aims to help small to medium sized business notify customers of their debts.

[![Python Version][python-image]][python-url]
[![Poetry Version][poetry-image]][poetry-url]
[![Django Version][django-image]][django-url]


The Project described here aims to automate a debt collection process in micro, small and average size businesses, said process is done manually today, by automating we are freeing human resource to be better applied somewhere else. 
This Project offers a user friendly web interface for administrators, company users and debtors to interact. Considering LGPD norms.

![](header.png)

## Installation

OS X & Linux:

```sh
pip install poetry
poetry install 
```

Windows:

```sh
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
poetry install
```

## Usage example

Create a superUser and add a company from that you can create other users such as owners, admins, workers and debtors. Each of them will interact in a different way with the webservice.  

_For more examples and usage, please refer to the [Wiki][wiki]._

## Development setup

Run poetry's default installation of dependencies and check out the Makefile for the commands to run Django's surver locally and more useful stuff. 

```sh
make install
make test
```

## Release History

* 0.1.0
    * CHANGE: first version

## Meta

Dickson R. Silva – [@Linkedin](https://www.linkedin.com/in/dickson-rsg/)

"Distributed under the MIT License. See ``LICENSE`` for more information."

[https://github.com/Dicksonrsg/DebtWarnSys](https://github.com/Dicksonrsg)

## Contributing

1. Fork it (<https://github.com/Dicksonrsg/DebtWarnSys/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[poetry-image]: https://img.shields.io/badge/poetry-managed-blue.svg?style=flat-square
[poetry-url]: https://python-poetry.org/
[django-image]: https://img.shields.io/badge/django-4.2-green.svg?style=flat-square
[django-url]: https://www.djangoproject.com/
[python-image]: https://img.shields.io/badge/python-3.11-blue.svg?style=flat-square
[python-url]: https://www.python.org/downloads/release/python-3110/
[wiki]: https://github.com/yourname/yourproject/wiki