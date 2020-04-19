# codes inspired from CS253 video lectures

# open libraries
import html
import re

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
'''
checks if a password is valid; not containing "^.{3,20}$"
'''
def IsValidPassword(password):
    regex = re.compile(r'^.{3,20}$')
    return password and regex.match(password)
'''
checks if an username is valid; not containing ^[a-zA-Z0-9_-]{3,20}$
'''
def IsValidUsername(username):
    regex = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
    return username and regex.match(username)
'''
checks if an email is valid; not containing ^[\S]+@[\S]+\.[\S]+$
'''
def IsValidEmail(email):
    regex = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
    return not email or regex.match(email)
'''
checks if password and verify_password matches
'''
def IsMatchingPassword(password, verify_password):
    return password == verify_password