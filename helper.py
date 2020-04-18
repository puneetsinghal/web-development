months = ['January',
'February',
'March',
'April',
'May',
'June',
'July',
'August',
'September',
'October',
'November',
'December'
]

month_dict = dict((month[:3].lower(), month) for month in months)

def valid_month(month):
    if month:
        short_month = month[:3].lower()
        return month_dict.get(short_month)

def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if day > 0 and day <= 31:
            return day

def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year > 1900 and year < 2021:
            return year