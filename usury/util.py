import logging
from datetime import date

from . import context_get

_l = logging.getLogger(__name__)


def days_in_year(context=None, year=None):
    """
    Returns the number of days in a year, according to the context

    :param context: Context of which mode(s) this function should operate in
    :type context: usury.Context
    :param year: Year for calculation, if context has year_mode of
        YEAR_DAYS_ACTUAL
    :type year: int
    :raises TypeError: if year isn't provided when context.year_mode is
        YEAR_DAYS_ACTUAL
    :return: Number of days in year
    :rtype: int
    """
    if context is None:
        context = context_get()
    if context.year_mode == context.YEAR_DAYS_ACTUAL:
        try:
            year = int(year)
        except TypeError:
            raise TypeError(
                'days_in_year() year argument must be convertible to int when '
                'context.year_mode is YEAR_DAYS_ACTUAL'
            )
        _l.debug('params(context=%s, year=%s)', repr(context), repr(year))
        return (date(year, 12, 31) - date(year-1, 12, 31)).days
    _l.debug('params(context=%s)', repr(context))
    if context.year_mode == context.YEAR_DAYS_365:
        return 365
    if context.year_mode == context.YEAR_DAYS_360:
        return 360
