import datetime
from dateutil.relativedelta import relativedelta


class Time(object):

    # 获取当前日期时间，返回datetime类型，格式为 %Y-%m-%d %H:%M:%S
    def getNowDatetime(self):
        now = datetime.datetime.now()
        now_str = datetime.datetime.strftime(now,"%Y-%m-%d %H:%M:%S")
        return datetime.datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S")

    # 获取当前日期，返回date类型，格式为 %Y-%m-%d
    def getNowDate(self):
        now = datetime.date.today()
        return now

    # 获取前一秒钟日期时间
    def getLastSecond(self, time):
        return time - datetime.timedelta(seconds=1)

    # 返回指定日期时间+n秒钟
    def addSecond(self, time, n):
        return time + datetime.timedelta(seconds=n)

    # 获取前一分钟日期时间
    def getLastMinute(self, time):
        return time - datetime.timedelta(minutes=1)

    # 返回指定日期时间+n分钟
    def addMinute(self, time, n):
        return time + datetime.timedelta(minutes=n)

    # 获取前一小时日期时间
    def getLastHour(self, time):
        return time - datetime.timedelta(hours=1)

    # 返回指定日期时间+n小时
    def addHour(self, time, n):
        return time + datetime.timedelta(hours=n)

    # 获取前一天日期时间
    def getLastDay(self, time):
        return time - datetime.timedelta(days=1)

    # 返回指定日期时间+n天
    def addDay(self, time, n):
        return time + datetime.timedelta(days=n)

    # 获取前一周日期时间
    def getLastWeek(self, time):
        return time - datetime.timedelta(weeks=1)

    # 返回指定日期时间+n周
    def addWeek(self, time, n):
        return time + datetime.timedelta(weeks=n)

    # 获取前一月日期时间
    def getLastMonth(self, time):
        return time - relativedelta(months=1)

    # 返回指定日期时间+n月
    def addMonth(self, time, n):
        return time + relativedelta(months=n)

    # 获取前一年日期时间
    def getLastYear(self, time):
        return time - relativedelta(years=1)

    # 返回指定日期时间+n年
    def addYear(self, time, n):
        return time + relativedelta(years=n)

    # 获取两个时间的时间差，返回timedelta，前-后
    def getDulartion(self, time1, time2):
        return time1 - time2

    # 获取两个时间的时间差的字符串描述：*年*天*小时*分*秒，若相等，返回'0'
    def getDulartionStr(self, time1, time2):
        second_str = ''
        minute_str = ''
        hour_str = ''
        day_str = ''
        year_str = ''
        dulartion = time1 - time2
        total = int(dulartion.total_seconds())
        second = total % 60
        if second != 0:
            second_str = str(second) + '秒'
        total = int(total / 60)
        minute = total % 60
        if minute != 0:
            minute_str = str(minute) + '分'
        total = int(total / 60)
        hour = total % 24
        if hour != 0:
            hour_str = str(hour) + '小时'
        total = int(total / 24)
        day = total % 365
        if day != 0:
            day_str = str(day) + '天'
        year = int(total / 365)
        if year != 0:
            year_str = str(year) + '年'
        dulartion_str = year_str + day_str + hour_str + minute_str + second_str
        if dulartion_str == '':
            dulartion_str = '0'
        return dulartion_str


    # 获取两个时间的时间差（秒级），返回int
    def getDulartionSeconds(self, time1, time2):
        dulartion = time1 - time2
        return int(dulartion.total_seconds())

    # 获取两个时间的时间差（分钟级），返回int
    def getDulartionMinutes(self, time1, time2):
        dulartion = time1 - time2
        seconds = int(dulartion.total_seconds())
        return int(seconds/60)

    # 获取两个时间的时间差（小时级），返回int
    def getDulartionHours(self, time1, time2):
        dulartion = time1 - time2
        seconds = int(dulartion.total_seconds())
        return int(seconds/60/60)

    # 获取两个时间的时间差（天级），返回int
    def getDulartionDays(self, time1, time2):
        dulartion = time1 - time2
        seconds = int(dulartion.total_seconds())
        return int(seconds/60/60/24)

    # 比较两个时间大小，前>后，返回1，前<后，返回-1，前=后，返回0
    def compare(self, time1, time2):
        dulartion = time1 - time2
        seconds = int(dulartion.total_seconds())
        if seconds > 0:
            return 1
        elif seconds < 0:
            return -1
        else:
            return 0

    # datetime 转 str
    def datetimeToStr(self, time):
        return datetime.datetime.strftime(time, "%Y-%m-%d %H:%M:%S")

    # str 转 datetime
    def strToDatetime(self, time_str):
        return datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

    # date 转 str
    def dateToStr(self, time):
        return datetime.datetime.strftime(time, "%Y-%m-%d")

    # str 转 date
    def strToDate(self, time_str):
        return datetime.datetime.strptime(time_str, "%Y-%m-%d")

    # datetime 转 date
    def datetimeToDate(self, time):
        return time.date()

    # date 转 datetime
    def dateToDatetime(self, time):
        time_str = datetime.datetime.strftime(time, "%Y-%m-%d") + " 00:00:00"
        return datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")



if __name__=='__main__':
    a = Time()
    b = a.getNowDate()
    print(b)
    print(type(b))
    c = a.dateToDatetime(b)
    print(c)
    print(type(c))