import decimal as _decimal

__title__ = 'usury'
__version__ = '0.1.0'

__context = None


# TODO: enhance to use thread or coroutine local storage for contexts
def context_get():
    """
    Returns the module's current context

    :returns: module's current context
    :rtype: Context
    """
    global __context
    if __context is None:
        __context = Context()
    return __context


def context_set(context):
    """
    Sets the module's current context

    :type context: Context
    """
    global __context
    if context == DefaultContext:
        context = context.copy()
    __context = context


def context_local(context=None):
    """
    Overwrites the module's current context, while in a with statement.

    >>> import usury
    >>> print usury.Context.year_mode_to_str(usury.context_get().year_mode)
    Context.YEAR_DAYS_360
    >>> with usury.context_local() as ctx:
    ...     ctx.year_mode = usury.Context.YEAR_DAYS_365
    ...     print usury.Context.year_mode_to_str(usury.context_get().year_mode)
    ...
    Context.YEAR_DAYS_365
    >>> print usury.Context.year_mode_to_str(usury.context_get().year_mode)
    Context.YEAR_DAYS_360

    :param context:
    :type context: Context
    """
    class manager(object):
        def __init__(self, ctx):
            """
            :type ctx: Context
            """
            self.context = ctx.copy()

        def __enter__(self):
            self.orig_context = context_get()
            context_set(self.context)
            return self.context

        def __exit__(self, exc_type, exc_val, exc_tb):
            context_set(self.orig_context)

    if context is None:
        context = context_get()
    return manager(context)


class Context(object):
    """
    Contains the context for working with the usury modules

    Contains:
    decimal - decimal.Context for use in math operations
    year_mode -
    """

    YEAR_DAYS_ACTUAL = 1
    YEAR_DAYS_365 = 2
    YEAR_DAYS_360 = 3

    def __init__(self, decimal=None, year_mode=None, quantize_interest=None,
                 quantize_currency=None):
        try:
            default = DefaultContext
        except NameError:
            pass
        self.decimal = decimal if decimal is not None else default.decimal
        self.year_mode = year_mode \
            if year_mode is not None else default.year_mode
        self.quantize_interest = quantize_interest \
            if quantize_interest is not None else default.quantize_interest
        self.quantize_currency = quantize_currency \
            if quantize_currency is not None else default.quantize_currency

    def copy(self):
        """
        Returns a deep copy of itself
        :rtype: Context
        """
        rv = Context(self.decimal, self.year_mode, self.quantize_interest,
                     self.quantize_currency)
        return rv
    __copy__ = copy

    def __repr__(self):
        cv = []
        if self.decimal != DefaultContext.decimal:
            cv.append('decimal={!r}'.format(self.decimal))
        if self.year_mode != DefaultContext.year_mode:
            cv.append('year_mode={}'.format(
                self.year_mode_to_str(self.year_mode))
            )
        if self.quantize_interest != DefaultContext.quantize_interest:
            cv.append('quantize_interest={!r}'.format(self.quantize_interest))
        if self.quantize_currency != DefaultContext.quantize_currency:
            cv.append('quantize_currency={!r}'.format(self.quantize_currency))
        return 'Context({})'.format(', '.join(cv))

    @staticmethod
    def year_mode_to_str(year_mode):
        if year_mode == Context.YEAR_DAYS_ACTUAL:
            return 'Context.YEAR_DAYS_ACTUAL'
        elif year_mode == Context.YEAR_DAYS_365:
            return 'Context.YEAR_DAYS_365'
        elif year_mode == Context.YEAR_DAYS_360:
            return 'Context.YEAR_DAYS_360'


DefaultContext = Context(
    decimal=_decimal.Context(prec=8),
    year_mode=Context.YEAR_DAYS_360,
    quantize_currency=_decimal.Decimal('0.01'),  # aka, a penny
    quantize_interest=_decimal.Decimal('0.0000001')  # aka 0.00001%
)

del _decimal
