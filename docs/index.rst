Content negotiation
===================

.. toctree::
   :hidden:
   :maxdepth: 1

   license
   reference

A small Python library for deciding content type based on a list of media ranges


Installation
------------

To install the content-negotiation package, run this command in your terminal:

.. code-block:: console

   $ pip install content-negotiation


Usage
-----

This package can be used like this:

.. code-block:: python

   accept_headers = ["application/json", "text/html", "text/plain, text/*;q=0.8"]
   supported_content_types = ["text/turtle", "application/json"]

   try:
      content_type = decide_content_type(accept_headers, supported_content_types)
   except NoAgreeableContentTypeError:
      print("No agreeable content type found.")
      # Handle error, by returning e.g. 406 Not Acceptable


