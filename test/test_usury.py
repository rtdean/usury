import unittest

import usury


class TestUsury(unittest.TestCase):
    def test_contexts(self):
        attributes = [
            'decimal',
            'year_mode',
            'quantize_interest',
            'quantize_currency',
        ]
        for attr in attributes:
            self.assertEqual(
                getattr(usury.context_get(), attr),
                getattr(usury.DefaultContext, attr),
                'running context != default context before changes on attribute'
                '{!r}, running: {!r} default: {!r}'.format(
                    attr,
                    usury.context_get(),
                    usury.DefaultContext
                )
            )
        with usury.context_local() as local_ctx:
            local_ctx.year_mode = usury.Context.YEAR_DAYS_365
            self.assertEqual(
                usury.context_get().year_mode,
                usury.Context.YEAR_DAYS_365,
            )
            local_ctx.year_mode = usury.Context.YEAR_DAYS_ACTUAL
            self.assertEqual(
                usury.context_get().year_mode,
                usury.Context.YEAR_DAYS_ACTUAL,
            )
        # make sure we went back to the defaults
        for attr in attributes:
            self.assertEqual(
                getattr(usury.context_get(), attr),
                getattr(usury.DefaultContext, attr),
                'running context != default context before changes on attribute'
                '{!r}, running: {!r} default: {!r}'.format(
                    attr,
                    usury.context_get(),
                    usury.DefaultContext
                )
            )


if __name__ == '__main__':
    unittest.main()
