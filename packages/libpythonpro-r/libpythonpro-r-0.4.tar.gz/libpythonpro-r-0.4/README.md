# libpythonpro
Módulo para exemplificar construção de projetos Python no curso PyTools

Neste curso é ensinado como contribuir com o projeto de código aberto

Link do curso [Python Pro](https://www.python.pro.br)

[![Build Status](https://travis-ci.com/ricardovezetiv/libpythonpro.svg?branch=main)](https://travis-ci.com/ricardovezetiv/libpythonpro)
[![Updates](https://pyup.io/repos/github/ricardovezetiv/libpythonpro/shield.svg)](https://pyup.io/repos/github/ricardovezetiv/libpythonpro/)
[![Python 3](https://pyup.io/repos/github/ricardovezetiv/libpythonpro/python-3-shield.svg)](https://pyup.io/repos/github/ricardovezetiv/libpythonpro/)
[![codecov](https://codecov.io/gh/ricardovezetiv/libpythonpro/branch/main/graph/badge.svg?token=zxhbnm5dpK)](https://codecov.io/gh/ricardovezetiv/libpythonpro)

Suportada a versão 3.9.5 do Python

### Para instalar:

```console
# python3 -m venv .venv
# source .venv/bin/activate
# pip install -r requirements-dev.txt
```

### Para conferir a qualidade do código:

```console
# flake8
```

### Tópicos a serem abordados:
 1. [Git](https://github.com/)
 2. Virtualenv
 3. Pip
 4. [Travis CI](https://travis-ci.org/)
 5. [PyUp](https://pyup.io/)
 6. [PyPI](https://pypi.org/)
 7. PyTest
 8. [PyTest Coverage](https://pytest-cov.readthedocs.io/en/latest/)
 9. [Code Coverage](https://about.codecov.io/)
 10. [Pytest-Mock](https://github.com/pytest-dev/pytest-mock)
 11. [Pipenv](https://github.com/pypa/pipenv)

### Bibliotecas de terceiros utilizadas: 
 1. [Requests](https://github.com/psf/requests/blob/master/README.md)
 2. [Flake8](https://github.com/PyCQA/flake8)
 3. Twine
 4. Pytest
 5. Pytest-cov
 6. Pytest-mock
 7. Pipenv


### Instalar o pacote 'libpythonpro' localmente:

```console
# python3 -m venv .venv
# source .venv/bin/activate
# pip install -e ./libpythonpro/
```

Verificar a Instalação do pacote: 

```console
# pip freeze
```

Testar o pacote, utilizando a biblioteca 'github_api'

```console
# python
Python 3.9.5 (default, May 11 2021, 08:20:37) 
[GCC 10.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.

>>> from libpythonpro.github_api import buscar_avatar
>>> buscar_avatar('ricardovezetiv')
>>> quit()
```

### Criando a versão '0.1' do projeto 'libpythonpro' no 'Git'

```console
# git tag 0.1
# git push --tags
```

### Upload de pacote para o PyPI

```console
# python setup.py sdist bdist_wheel
# pip install twine
# twine upload dist/*
```

Para instalar:
```console
# python3 -m venv test
# source test/bin/activate
# pip install libpythonpro-r

# pip freeze
certifi==2021.5.30
charset-normalizer==2.0.3
idna==3.2
libpythonpro-r==0.1
requests==2.26.0
urllib3==1.26.6
```

### Instalar o PyTest

```console
# pip install pytest
```

Executar o PyTest via linha de comando:

```console
# pytest libpythonpro/tests/
```

### Instalar o PyTest Coverage

```console
# pip install pytest-cov
```

Executar o PyTest com o Coverage

```console
# pytest libpythonpro --cov=libpythonpro
```

### Instalar o Pytest-Mock

```console
# pip install pytest-mock
```

### Instalar o Pipenv

```console
# pip install pipenv
```

Comandos utilizados para integrar o projeto ao 'Pipenv'

```console
# deactivate
# rm -Rf .venv
# pipenv install requests
# pipenv install --dev flake8 pytest coverage pytest-cov pytest-mock
# pipenv graph
# pipenv run flake8
```