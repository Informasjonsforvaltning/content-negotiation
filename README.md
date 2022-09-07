# content-negotiation

![Tests](https://github.com/Informasjonsforvaltning/content-negotiation/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/Informasjonsforvaltning/content-negotiation/branch/master/graph/badge.svg)](https://codecov.io/gh/Informasjonsforvaltning/content-negotiation)
[![PyPI](https://img.shields.io/pypi/v/content-negotiation.svg)](https://pypi.org/project/content-negotiation/)
[![Read the Docs](https://readthedocs.org/projects/content-negotiation/badge/)](https://content-negotiation.readthedocs.io/)

A small Python library supporting content-negotiation.

It can be used to deciding content type based on a list of media ranges, as well as deciding content-language based on the accpe-language header.

## Usage

### Install

```Shell
% pip install content-negotiation
```

### Getting started

#### Content type

```Python
from content_negotiation import decide_content_type, NoAgreeableContentTypeError

accept_headers = ["application/json", "text/html", "text/plain, text/*;q=0.8"]
supported_content_types = ["text/turtle", "application/json"]

try:
    content_type = decide_content_type(accept_headers, supported_content_types)
except NoAgreeableContentTypeError:
    print("No agreeable content type found.")
    # Handle error, by returning e.g. 406 Not Acceptable
```

#### Content language

```Python
from content_negotiation import decide_content_language, NoAgreeableContentLanguageError

accept_language_headers = ["application/json", "text/html", "text/plain, text/*;q=0.8"]
supported_languages = ["text/turtle", "application/json"]

try:
    content_language = decide_decide_language(accept_language_headers, supported_languages)
except NoAgreeableLanguageError:
    print("No agreeable language found.")
    # Handle error, by returning e.g. 406 Not Acceptable
```

## Development

### Requirements

- [pyenv](https://github.com/pyenv/pyenv) (recommended)
- python3
- [pipx](https://github.com/pipxproject/pipx) (recommended)
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)

```Shell
% pipx install poetry==1.1.13
% pipx install nox==2022.1.7
% pipx inject nox nox-poetry==0.9.0
```

### Install developer tools

```Shell
% git clone https://github.com/Informasjonsforvaltning/content-negotiation.git
% cd content-negotiation
% pyenv install 3.8.13
% pyenv install 3.9.13
% pyenv install 3.10.6
% pyenv local 3.8.13 3.9.13 3.10.6
% poetry install
```

### Run all sessions

```Shell
% nox
```

### Run all tests with coverage reporting

```Shell
% nox -rs tests
```

### Debugging

You can enter into [Pdb](https://docs.python.org/3/library/pdb.html) by passing `--pdb` to pytest:

```Shell
% nox -rs tests -- --pdb  --log-cli-level=DEBUG
```

You can set breakpoints directly in code by using the function `breakpoint()`.
