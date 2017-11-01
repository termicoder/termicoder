import datetime


def get_date_time(epoch):
    return (get_date(epoch), get_time(epoch))


def get_date(epoch):
    return datetime.datetime.fromtimestamp(int(epoch)).strftime('%d %h %y')


def get_time(epoch):
    return datetime.datetime.fromtimestamp(int(epoch)).strftime('%I:%M %p')
