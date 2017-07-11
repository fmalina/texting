from datetime import time, datetime, timedelta
from dateutil.easter import easter

def seasons_greeting(now=datetime.now()):
    yyyy = int(now.strftime('%Y'))
    
    def easter_season(yyyy):
        """Easter Sunday falls on different day every year"""
        esun = datetime.combine(easter(yyyy), datetime.min.time())
        return esun-timedelta(days=7), esun+timedelta(days=7)

    def season(start, end):
        dt = lambda ddmm,hrs: datetime.combine(
            datetime.strptime('%s.%s' % (ddmm, yyyy), '%d.%m.%Y'),
            hrs)
        term = dt(start, datetime.min.time()),\
               dt(end,   datetime.max.time())
        return term
    
    def is_season(now, season):
        begin, end = season
        if begin <= now <= end:
            return True
        return False
    
    seasons = (
        (season('15.12', '27.12'), 'Merry Christmas'),
        (season('01.01', '12.01'), 'Happy New Year %d' % yyyy),
        (easter_season(yyyy)     , 'Happy Easter'),
        (season('28.10', '02.11'), 'Happy Halloween'),
        (season('14.02', '14.02'), 'Happy Valentine\'s Day')
    )
    
    for term, greeting in seasons:
        if is_season(now, term):
            return greeting
    return False

def timely_greeting(now=datetime.now()):
    dt = (['morning', time( 0, 0)],
          ['day',     time( 8,30)],
          ['night',   time(16,45)])
    day_num = now.isoweekday()
    daytime = [x for x, t in dt if now.time() >= t][-1]
    weektime = 'week'+('end' if now.isoweekday() in [6, 7] else 'day')

    t = daytime
    # Say "have a good weekend" at the weekend and Friday night
    if weektime == 'weekend' or (day_num == 5 and daytime == 'night'):
        t = 'weekend'
    # but not on a Sunday night
    if day_num == 7 and daytime == 'night':
        t = 'night'

    greeting = 'Have a good '+t

    seasonal = seasons_greeting(now)
    if seasonal:
        return seasonal
    return greeting

from django.test import TestCase

class GreetingTestCase(TestCase):
    def test_greeting(self):
        """Greetings timely to current date and time."""
        testcases = (
            (datetime(2015, 1,  8         ), 'Happy New Year 2015'),
            (datetime(2015, 2,  14        ), "Happy Valentine's Day"),
            (datetime(2015, 2,  15, 10, 00), 'Have a good weekend'),
            # Sunday night end of weekend
            (datetime(2016, 7,  10, 19, 30), 'Have a good night'),
            (datetime(2015, 2,  16, 6,  00), 'Have a good morning'),
            (datetime(2015, 2,  16, 10, 00), 'Have a good day'),
            (datetime(2015, 2,  16, 18, 00), 'Have a good night'),
            (datetime(2015, 3,  29        ), 'Happy Easter'),
            (datetime(2015, 10, 31        ), 'Happy Halloween'),
            (datetime(2015, 12, 15        ), 'Merry Christmas'),
            (datetime(2015, 12, 27        ), 'Merry Christmas'),
            (datetime(2016, 1,  1         ), 'Happy New Year 2016'),
        )
        for dt, greeting in testcases:
            self.assertEqual(timely_greeting(dt), greeting)
