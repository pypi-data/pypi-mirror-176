click_logging_config
====================

Quick and easy logging parameters for click commands.


.. contents::

.. section-numbering::


Installation
------------

The ``click_logging_config`` package is available from PyPI. Installing
into a virtual environment is recommended.

.. code-block::

   python3 -m venv .venv; .venv/bin/pip install click_logging_config


Getting Started
---------------

Using ``click_logging_config`` is intended to be very simple. A single
decorator applied to your click command or group adds some click options
specifically for managing logging context.

.. code-block::

   import click
   import logging
   from click_logging import logging_parameters

   log = logging.getLogger(__name__)

   def do_something()

   @click.command()
   # NOTE: Empty braces required for hard-coded click_logging.parameters defaults.
   @click.option("--my-option", type=str)
   @logging_parameters()
   def my_command(my_option: str) -> None:
       log.info("doing something")
       try:
           do_something(my_option)
       except Exception as e:
           log.critical(f"something bad happened, {str(e)}")
           raise


Application of ``@logging_parameters`` decorator must be applied immediately
*above* your click command function and *below* any other click decorators such
as arguments and options.
