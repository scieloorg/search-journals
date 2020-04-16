# coding=utf-8
from datetime import datetime


# Date composed by more than four digits
DATE_ERROR_LEVEL_SIZE = 1

# Date composed by invalid chars
DATE_ERROR_LEVEL_CHAR = 2

# Year out of interval [1000, 2020]
DATE_ERROR_LEVEL_VALUE = 3

# Empty date
DATE_ERROR_LEVEL_EMPTY = 4

# Author's name composed by invalid char
AUTHOR_ERROR_LEVEL_CHAR = 1

# A initial version of a list of invalid chars (for checking author's fullname)
INVALID_CHARS = [u'@', u'≈', u'≠', u'‼', u'∗', u'¾', u'²', u'}', u'=', u'‰', u'¶', u'±', u'³', u'©', u'¼', u'[', u']',
                 u'#', u'?', u')', '(', u'{', u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'!', u'¡',
                 u'¿', u'«', u'»', u'*', u'/', u'\\', u'&', u'%', u'‖', u'§', u'®', u'¹', u'½']


class SanityChecker(object):

    @staticmethod
    def check_date(date):
        if not date:
            return DATE_ERROR_LEVEL_EMPTY

        # Get the first four elements of the date
        if len(date) > 4:
            date = date[:4]

        if len(date) < 4:
            return DATE_ERROR_LEVEL_SIZE
        elif not date.isdigit():
            return DATE_ERROR_LEVEL_CHAR
        elif int(date) < 1000 or int(date) > datetime.now().year:
            return DATE_ERROR_LEVEL_VALUE

    @staticmethod
    def check_author_name(text):
        for c in text:
            if c in INVALID_CHARS:
                return AUTHOR_ERROR_LEVEL_CHAR
