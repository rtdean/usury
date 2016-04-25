"""
calculation of simple-interest loans
"""
import decimal
import logging
from datetime import date

from . import context_get
from .util import days_in_year

_l = logging.getLogger(__name__)

_zero = decimal.Decimal('0.00')


def calculate(transactions, rate, end, context=None):
    """

    :param transactions: a dict containing key (datetime.date) pointing to a
        transaction value.  The transactional value is the amount to/from the
        borrower; positive values are money to the borrower, negative is money
        received from them
    :type transactions: dict
    :param rate: Interest rate of the loan, where 1.0 == 100%
    :type rate: decimal.Decimal
    :param end:
    :type end: date
    :param context: Context of which mode(s) this function should operate in
    :type context: usury.Context
    :return:
    """
    if context is None:
        context = context_get()
    rate = decimal.Decimal(rate)
    balance = _zero
    interest_balance = _zero
    interest_total = _zero
    tx_dates = sorted(transactions.keys())
    last_date = tx_dates[0]
    rv = {}
    for tx_date in tx_dates:
        _l.debug('processing entry for date %s', tx_date)

        disbursement = 0
        if tx_date > end:
            _l.debug('date is beyond end, changing date to end for final run')
            tx_date = end
            payment = _zero
        else:
            payment = decimal.Decimal(transactions[tx_date])

        if payment > _zero:
            disbursement = payment
            payment = _zero
        else:
            payment *= -1
        _l.debug(
            'prev date %s; curr date %s; payment %s; balance %s',
            last_date, tx_date, payment, balance
        )
        accrued = calc_interest(balance, start=last_date, end=tx_date,
                                rate=rate, context=context)
        interest_total += accrued
        interest_balance += accrued
        if interest_balance > payment:
            interest_balance -= payment
            interest_paid = payment
        else:
            if disbursement:
                balance += disbursement
            balance -= payment - interest_balance
            interest_paid = interest_balance
            interest_balance = _zero
        _l.debug(
            'interest accurred %s; interest balance %s; interest total %s; '
            'interest paid %s',
            accrued, interest_balance, interest_total, interest_paid
        )
        _l.debug(
            'updated balance %s',
            balance
        )

        rv[tx_date] = {
            'balance': balance,
            'interest_balance': interest_balance,
            'interest_total': interest_total,
            'payment': payment,
            'payment_interest': interest_paid,
            'payment_principal': payment - interest_paid,
        }

        if tx_date >= end:
            break
        last_date = tx_date

    if end not in rv and end > tx_dates[-1] and balance > 0:
        accrued = calc_interest(balance, start=last_date, end=end,
                                rate=rate, context=context)
        interest_total += accrued
        interest_balance += accrued
        rv[end] = {
            'balance': balance,
            'interest_balance': interest_balance,
            'interest_total': interest_total,
            'payment_interest': _zero,
            'payment_principal': _zero,
        }

    return rv


def daily_rate(rate, year=None, context=None):
    """
    Returns the daily interest rate on a simple loan

    :param rate: interest rate, where 1.0 is 100%
    :type rate: decimal.Decimal
    :param year: year for the interest rate, only used when context.year_mode
        is YEAR_DAYS_ACTUAL
    :type year: int
    :param context: Context of which mode(s) this function should operate in
    :type context: usury.Context
    :return: The per-day interest rate
    :rtype: decimal.Decimal
    """
    if context is None:
        context = context_get()
    return (decimal.Decimal(rate) /
            days_in_year(context=context, year=year)).quantize(
        context.quantize_interest
    )


def calc_interest(balance, start, end, rate, context=None):
    """
    Calculates the interest accrued between two dates for the given balance and
    interest rate.

    :param balance:
    :type balance: decimal.Decimal
    :param start:
    :type start: datetime.date
    :param end:
    :type end: datetime.date
    :param rate:
    :type rate: decimal.Decimal
    :param context: Context of which mode(s) this function should operate in
    :type context: usury.Context
    :return: Amount of interest accrued between start and end, for balance at
        rate
    :rtype: decimal.Decimal
    """
    if context is None:
        context = context_get()
    balance = decimal.Decimal(balance)
    rate = decimal.Decimal(rate)
    _l.debug(
        'entered, (balance=%s, start=%s, end=%s, rate=%s, context=%s',
        repr(balance),
        repr(start),
        repr(end),
        repr(rate),
        repr(context)
    )
    if start >= end:
        return _zero

    if context.year_mode == context.YEAR_DAYS_ACTUAL and \
            start < date(end.year-1, 12, 31):
        interest = _zero

        _l.debug(
            'time span crosses year boundaries in YEAR_DAYS_ACTUAL mode; going '
            'to iterate through the years now; start: %s, end; %s',
            start,
            end
        )

        for year in xrange(start.year, end.year+1):
            interest += calc_interest(
                balance,
                start if year == start.year else date(year-1, 12, 31),
                end if year == end.year else date(year, 12, 31),
                rate,
                context=context,
            )
        return interest

    days = (end - start).days
    daily_interest = (
        decimal.Decimal(balance) *
        daily_rate(rate, context=context, year=end.year)
    ).quantize(
        context.quantize_currency,
        context=context.decimal,
    )
    rv = daily_interest * days

    _l.debug(
        'daily interest: %s, days: %d, returning %s',
        daily_interest, days, rv
    )

    return rv
