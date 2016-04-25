import logging
import unittest
from datetime import date
from decimal import Decimal

from usury import Context
import usury.simple as simple

logging.basicConfig(level=logging.DEBUG)


class TestSimple(unittest.TestCase):
    def test_daily_rate_days_actual(self):
        ctx = Context(year_mode=Context.YEAR_DAYS_ACTUAL)
        rate = Decimal('0.10000')
        with self.assertRaises(TypeError):
            simple.daily_rate(rate, context=ctx)
        self.assertIsInstance(
            simple.daily_rate(rate, year=2014, context=ctx),
            Decimal
        )
        self.assertEqual(
            simple.daily_rate(rate, year=2014, context=ctx),
            simple.daily_rate(rate, year=2015, context=ctx),
        )
        self.assertNotEqual(
            simple.daily_rate(rate, year=2015, context=ctx),
            simple.daily_rate(rate, year=2016, context=ctx),
        )
        self.assertEqual(
            simple.daily_rate(rate, year=2015, context=ctx),
            Decimal('0.0002740')
        )
        self.assertEqual(
            simple.daily_rate(rate, year=2016, context=ctx),
            Decimal('0.0002732')
        )

    def test_daily_rate_days_360(self):
        ctx = Context(year_mode=Context.YEAR_DAYS_360)
        rate = Decimal('0.10000')
        self.assertIsInstance(
            simple.daily_rate(rate, context=ctx),
            Decimal
        )
        self.assertEqual(
            simple.daily_rate(rate, context=ctx),
            Decimal('0.0002778')
        )

    def test_daily_rate_days_365(self):
        ctx = Context(year_mode=Context.YEAR_DAYS_365)
        rate = Decimal('0.10000')
        self.assertIsInstance(
            simple.daily_rate(rate, context=ctx),
            Decimal
        )
        self.assertEqual(
            simple.daily_rate(rate, context=ctx),
            Decimal('0.0002740')
        )

    def test_calculate_interest(self):
        balance = Decimal('10000.00')
        rate = Decimal('0.1000000')  # aka 10.00000%

        # test to make sure if the start is after the end, we get a decimal 0
        # back
        self.assertEqual(
            simple.calc_interest(
                balance=balance,
                start=date.today(),
                end=date(2016, 1, 1),
                rate=rate
            ),
            Decimal('0.00')
        )

        self.assertEqual(
            simple.calc_interest(
                balance=balance,
                start=date(2016, 1, 1),
                end=date(2016, 1, 2),
                rate=rate,
            ),
            Decimal('2.78')
        )
        self.assertEqual(
            simple.calc_interest(
                balance=balance,
                start=date(2015, 9, 30),
                end=date(2016, 3, 31),
                rate=rate,
            ),
            Decimal('2.78') * 183
        )

    def test_calculate_interest_360(self):
        """
        test against a 360 day context

        this should be the same as testing the default context
        """
        ctx = Context(year_mode=Context.YEAR_DAYS_360)
        balance = Decimal('10000.00')
        rate = Decimal('0.1000000')  # aka 10.00000%

        # test to make sure if the start is after the end, we get a decimal 0
        # back
        self.assertEqual(
            simple.calc_interest(
                balance=balance,
                start=date.today(),
                end=date(2016, 1, 1),
                rate=rate,
                context=ctx,
            ),
            Decimal('0.00')
        )

        self.assertEqual(
            simple.calc_interest(
                balance=balance,
                start=date(2016, 1, 1),
                end=date(2016, 1, 2),
                rate=rate,
                context=ctx,
            ),
            Decimal('2.78')
        )
        self.assertEqual(
            simple.calc_interest(
                balance=balance,
                start=date(2015, 9, 30),
                end=date(2016, 3, 31),
                rate=rate,
                context=ctx,
            ),
            Decimal('2.78') * 183
        )

    def test_calculate_interest_365(self):
        """
        test against a 365 day context
        """
        ctx = Context(year_mode=Context.YEAR_DAYS_365)
        balance = Decimal('10000.00')
        rate = Decimal('0.1000000')  # aka 10.00000%

        # test to make sure if the start is after the end, we get a
        # decimal 0
        # back
        self.assertEqual(
            simple.calc_interest(
                balance=balance,
                start=date.today(),
                end=date(2016, 1, 1),
                rate=rate,
                context=ctx,
            ),
            Decimal('0.00')
        )

        self.assertEqual(
            simple.calc_interest(
                balance=balance,
                start=date(2016, 1, 1),
                end=date(2016, 1, 2),
                rate=rate,
                context=ctx,
            ),
            Decimal('2.74')
        )
        self.assertEqual(
            simple.calc_interest(
                balance=balance,
                start=date(2015, 9, 30),
                end=date(2016, 3, 31),
                rate=rate,
                context=ctx,
            ),
            Decimal('2.74') * 183
        )

    def test_calculate_interest_yr_actual(self):
        """
        test against the actual # of days in a year
        """
        ctx = Context(year_mode=Context.YEAR_DAYS_ACTUAL)
        balance = Decimal('10000.00')
        rate = Decimal('0.1000000')  # aka 10.00000%

        # test to make sure if the start is after the end, we get a
        # decimal 0
        # back
        self.assertEqual(
            simple.calc_interest(
                balance=balance,
                start=date.today(),
                end=date(2016, 1, 1),
                rate=rate,
                context=ctx,
            ),
            Decimal('0.00')
        )

        self.assertEqual(
            simple.calc_interest(
                balance=balance,
                start=date(2016, 1, 1),
                end=date(2016, 1, 2),
                rate=rate,
                context=ctx,
            ),
            Decimal('2.73')
        )
        self.assertEqual(
            simple.calc_interest(
                balance=balance,
                start=date(2015, 9, 30),
                end=date(2015, 12, 31),
                rate=rate,
                context=ctx,
            ),
            Decimal('2.74') * 92
        )
        self.assertEqual(
            simple.calc_interest(
                balance=balance,
                start=date(2015, 12, 31),
                end=date(2016, 3, 31),
                rate=rate,
                context=ctx,
            ),
            Decimal('2.73') * 91
        )
        self.assertEqual(
            simple.calc_interest(
                balance=balance,
                start=date(2015, 9, 30),
                end=date(2016, 3, 31),
                rate=rate,
                context=ctx,
            ),
            (Decimal('2.74') * 92) + (Decimal('2.73') * 91)
        )


class LoanCase(unittest.TestCase):
    def setUp(self):
        self.transactions = {
            date(2014, 10, 8): Decimal('10000.00'),
            date(2015, 1, 3): Decimal('-233.52'),
            date(2015, 4, 2): Decimal('-2500.00'),
            date(2015, 6, 29): Decimal('-2500.00'),
            date(2015, 10, 1): Decimal('-2500.00'),
            date(2015, 12, 20): Decimal('-2500.00'),
            date(2016, 3, 27): Decimal('-673.34'),
        }

    def test_calculate(self):
        self.maxDiff = None
        self.assertDictEqual(
            simple.calculate(
                self.transactions,
                rate=Decimal('0.1000000'),
                end=date.today()
            ),
            {
                date(2014, 10, 8): {
                    'balance': Decimal('10000.00'),
                    'interest_balance': Decimal('0.00'),
                    'interest_total': Decimal('0.00'),
                    'payment': Decimal('0.00'),
                    'payment_interest': Decimal('0.00'),
                    'payment_principal': Decimal('0.00'),
                },
                date(2015, 1, 3): {
                    'balance': Decimal('10000.00'),
                    'interest_balance': Decimal('8.34'),
                    'interest_total': Decimal('241.86'),
                    'payment': Decimal('233.52'),
                    'payment_interest': Decimal('233.52'),
                    'payment_principal': Decimal('0.00'),
                },
                date(2015, 4, 2): {
                    'balance': Decimal('7755.76'),
                    'interest_balance': Decimal('0.00'),
                    'interest_total': Decimal('489.28'),
                    'payment': Decimal('2500.00'),
                    'payment_interest': Decimal('255.76'),
                    'payment_principal': Decimal('2244.24'),
                },
                date(2015, 6, 29): {
                    'balance': Decimal('5444.96'),
                    'interest_balance': Decimal('0.00'),
                    'interest_total': Decimal('678.48'),
                    'payment': Decimal('2500.00'),
                    'payment_interest': Decimal('189.20'),
                    'payment_principal': Decimal('2310.80'),
                },
                date(2015, 10, 1): {
                    'balance': Decimal('3086.90'),
                    'interest_balance': Decimal('0.00'),
                    'interest_total': Decimal('820.42'),
                    'payment': Decimal('2500.00'),
                    'payment_interest': Decimal('141.94'),
                    'payment_principal': Decimal('2358.06'),
                },
                date(2015, 12, 20): {
                    'balance': Decimal('655.70'),
                    'interest_balance': Decimal('0.00'),
                    'interest_total': Decimal('889.22'),
                    'payment': Decimal('2500.00'),
                    'payment_interest': Decimal('68.80'),
                    'payment_principal': Decimal('2431.20'),
                },
                date(2016, 3, 27): {
                    'balance': Decimal('0.00'),
                    'interest_balance': Decimal('0.00'),
                    'interest_total': Decimal('906.86'),
                    'payment': Decimal('673.34'),
                    'payment_interest': Decimal('17.64'),
                    'payment_principal': Decimal('655.70'),
                }
            }
        )

if __name__ == '__main__':
    unittest.main()
