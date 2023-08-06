import datetime
from MyDateTimeLib import myfunction


def test():
    assert myfunction.date_find("10-12-1995") == {'Date:0': datetime.datetime(1995, 10, 12, 0, 0)}
