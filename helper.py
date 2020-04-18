# codes inspired from CS253 video lectures

# open libraries
import html

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

def rot13_conversion(input):
    out = ""
    for char in html.unescape(input):
        if (char.isalpha() and char.islower()):
            index = ord(char) - ord('a')
            index = index + 13
            if index > 25:
                index = index - 26
            out = out + chr(index + ord('a'))
        elif char.isalpha():
            index = ord(char) - ord('A')
            index = index + 13
            if index > 25:
                index = index - 26
            out = out + chr(index + ord('A'))
        else:
            out = out + char
    return out