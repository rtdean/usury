import unittest

from usury import Context
import usury.util


class TestUtil(unittest.TestCase):
    def test_days_in_year(self):
        self.assertEqual(
            usury.util.days_in_year(),
            360,
            'default of days_in_year, no args, has changed'
        )

        ctx = Context(year_mode=Context.YEAR_DAYS_360)
        self.assertEqual(
            usury.util.days_in_year(context=ctx),
            360,
            'days_in_year(context={!r}) failed to return 360'.format(ctx)
        )

        ctx = Context(year_mode=Context.YEAR_DAYS_365)
        self.assertEqual(
            usury.util.days_in_year(context=ctx),
            365,
            'days_in_year(context={!r}) failed to return 365'.format(ctx)
        )

        ctx = Context(year_mode=Context.YEAR_DAYS_ACTUAL)
        self.assertEqual(
            usury.util.days_in_year(context=ctx, year=2015),
            365,
            'days_in_year(context={!r}, year=2015) failed to return 365'.format(
                ctx
            )
        )
        self.assertEqual(
            usury.util.days_in_year(context=ctx, year=2016),
            366,
            'days_in_year(context={!r}, year=2016) failed to return 366'.format(
                ctx
            )
        )

if __name__ == '__main__':
    unittest.main()
