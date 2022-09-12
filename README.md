# content-negotiation

![Tests](https://github.com/Informasjonsforvaltning/content-negotiation/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/Informasjonsforvaltning/content-negotiation/branch/master/graph/badge.svg)](https://codecov.io/gh/Informasjonsforvaltning/content-negotiation)
[![PyPI](https://img.shields.io/pypi/v/content-negotiation.svg)](https://pypi.org/project/content-negotiation/)
[![Read the Docs](https://readthedocs.org/projects/content-negotiation/badge/)](https://content-negotiation.readthedocs.io/)

A small Python library supporting content-negotiation.

It is used to decide content type based on a list of media ranges in the accept header, as well as deciding content-language based on the accept-language header.

* Media ranges/language ranges with a q-value of 0.0 will be ignored.
* Q-values above 1.0 will be treated as 1.0. Q-values below 0.0 will be treated as 0.0.
* When a media range is not specified, it will be treated as `*/*`.
* When a language range is not specified, it will be treated as `*`.
* When media ranges and language ranges are equal, the first one will be returned.

For more information on the accept header, see [RFC 7231, section-5.3.2](https://tools.ietf.org/html/rfc7231#section-5.3.2).
For more information on the accept-language header, see [RFC 7231, section-5.3.5](https://www.rfc-editor.org/rfc/rfc7231#section-5.3.5)

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

accept_language_headers = ["en-GB;q=0.8", "nb-NO;q=0.9"]
   supported_languages = ["en-GB", "en", "nb-NO", "nb", "en-US"]

try:
    content_language = decide_decide_language(accept_language_headers, supported_languages)
except NoAgreeableLanguageError:
    print("No agreeable language found.")
    # Handle error, by returning e.g. 406 Not Acceptable
```

## Development

### Requirements

* [pyenv](https://github.com/pyenv/pyenv) (recommended)
* python3
* [pipx](https://github.com/pipxproject/pipx) (recommended)
* [poetry](https://python-poetry.org/) # version v1.2.0 or higher
* [nox](https://nox.thea.codes/en/stable/)

```Shell
% pipx install poetry==1.2.0
% pipx install nox==2022.8.7
% pipx inject nox nox-poetry==1.0.1
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
