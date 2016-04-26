.. _api

Usury
=====

The parent usury module contains the `Context` class, along with helper
functions to manage context.  Context is used to tell the actual calculation
functions how to go about their calculations; things like 'how many days are in
a year' (for most commercial loans, that answer is 360, but occasionally, it's
365) or to what decimal-precision should interest be rounded to, or to what
currency precision should currency be rounded to.

.. module:: usury

.. autoclass:: Context

.. autofunction:: context_get
.. autofunction:: context_set
.. autofunction:: context_local



Simple Interest
---------------

.. module:: usury.simple
.. automodule:: usury.simple

.. autofunction:: calc_interest
.. autofunction:: daily_rate
.. autofunction:: calculate


Utilities
---------

.. module:: usury.util

.. autofunction:: days_in_year