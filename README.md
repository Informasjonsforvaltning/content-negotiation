# content-negotiation

![Tests](https://github.com/Informasjonsforvaltning/content-negotiation/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/Informasjonsforvaltning/content-negotiation/branch/master/graph/badge.svg)](https://codecov.io/gh/Informasjonsforvaltning/content-negotiation)
[![PyPI](https://img.shields.io/pypi/v/content-negotiation.svg)](https://pypi.org/project/content-negotiation/)
[![Read the Docs](https://readthedocs.org/projects/content-negotiation/badge/)](https://content-negotiation.readthedocs.io/)

A small Python library for mapping a data catalog to rdf

The library contains helper classes for the following dcat classes:

- [Catalog](https://www.w3.org/TR/vocab-dcat-2/#Class:Catalog)
- [Dataset](https://www.w3.org/TR/vocab-dcat-2/#Class:Dataset)
- [Distribution](https://www.w3.org/TR/vocab-dcat-2/#Class:Distribution)
- [Data Service](https://www.w3.org/TR/vocab-dcat-2/#Class:Data_Service)

 Other relevant classes are also supported, such as:

- Contact [vcard:Kind](https://www.w3.org/TR/2014/NOTE-vcard-rdf-20140522/#d4e1819)

 The library will map to [the Norwegian Application Profile](https://data.norge.no/specification/dcat-ap-no) of [the DCAT standard](https://www.w3.org/TR/vocab-dcat-2/).

## Usage

### Install

```Shell
% pip install content-negotiation
```

### Getting started

```Python
from content_negotiation import decide_content_type

accept_weighted_media_ranges: List[str] = ["text/turtle", "application/ld+json"]
content_type = decide_content_type(
    accept_weighted_media_ranges, SUPPORTED_CONTENT_TYPES
)
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
% pyenv install 3.8.12
% pyenv install 3.9.10
% pyenv local 3.8.12 3.9.10 
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
nox -rs tests -- --pdb
```

You can set breakpoints directly in code by using the function `breakpoint()`.
