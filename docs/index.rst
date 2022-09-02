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

To install the content-negotiation package,
run this command in your terminal:

.. code-block:: console

   $ pip install content-negotiation


Usage
-----

This package can be used like this:

.. code-block:: python

  from content_negotiation import decide_content_type

  accept_weighted_media_ranges: List[str] = ["text/turtle", "application/ld+json"]
  content_type = decide_content_type(
      accept_weighted_media_ranges, SUPPORTED_CONTENT_TYPES
  )
