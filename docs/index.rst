Content negotiation
===================

.. toctree::
   :hidden:
   :maxdepth: 1

   license
   reference

A small Python library supporting content-negotiation.

It is used to decide content type based on a list of media ranges in the accept header, as well as deciding content-language based on the accept-language header.

* Media ranges/language ranges with a q-value of 0.0 will be ignored.
* Q-values above 1.0 will be treated as 1.0. Q-values below 0.0 will be treated as 0.0.
* When a media range is not specified, it will be treated as */*.
* When a language range is not specified, it will be treated as \*.
* When media ranges and language ranges are equal, the first one will be returned.

For more information on the accept header, see [RFC 7231, section-5.3.2](https://tools.ietf.org/html/rfc7231#section-5.3.2).

For more information on the accept-language header, see [RFC 7231, section-5.3.5](https://www.rfc-editor.org/rfc/rfc7231#section-5.3.5)


Installation
------------

To install the content-negotiation package, run this command in your terminal:

.. code-block:: console

   $ pip install content-negotiation


Usage
-----

This package can be used like this:

.. code-block:: python

   from content_negotiation import decide_content_type, NoAgreeableContentTypeError

   accept_headers = ["application/json", "text/html", "text/plain, text/*;q=0.8"]
   supported_content_types = ["text/turtle", "application/json"]

   try:
      content_type = decide_content_type(accept_headers, supported_content_types)
   except NoAgreeableContentTypeError:
      print("No agreeable content type found.")
      # Handle error, by returning e.g. 406 Not Acceptable


.. code-block:: python

   from content_negotiation import decide_language, NoAgreeableLanguageError

   accept_language_headers = ["en-GB;q=0.8", "nb-NO;q=0.9"]
   supported_languages = ["en-GB", "en", "nb-NO", "nb", "en-US"]

   try:
      content_language = decide_decide_language(accept_language_headers, supported_languages)
   except NoAgreeableLanguageError:
      print("No agreeable language found.")
      # Handle error, by returning e.g. 406 Not Acceptable


