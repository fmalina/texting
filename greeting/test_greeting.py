from django.test import TestCase
from datetime import datetime
import greeting


class GreetingTestCase(TestCase):
    def test_greeting(self):
        """Greetings timely to current date and time."""
        testcases = (
            (datetime(2015, 1, 8), 'Happy New Year 2015'),
            (datetime(2015, 2, 14), "Happy Valentine's Day"),
            (datetime(2015, 2, 15, 10, 00), 'Have a good weekend'),
            # Sunday night end of weekend
            (datetime(2016, 7, 10, 19, 30), 'Have a good night'),
            (datetime(2015, 2, 16, 6,  00), 'Have a good morning'),
            (datetime(2015, 2, 16, 10, 00), 'Have a good day'),
            (datetime(2015, 2, 16, 18, 00), 'Have a good night'),
            (datetime(2015, 3, 29), 'Happy Easter'),
            (datetime(2015, 10, 31), 'Happy Halloween'),
            (datetime(2015, 12, 15), 'Merry Christmas'),
            (datetime(2015, 12, 27), 'Merry Christmas'),
            (datetime(2016, 1, 1), 'Happy New Year 2016'),
        )
        for dt, greetings in testcases:
            self.assertEqual(greeting.timely_greeting(dt), greetings)
