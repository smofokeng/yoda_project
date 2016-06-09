"""
South Africa-specific Form helpers
"""
from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.forms.fields import Field, RegexField
from django.utils.checksums import luhn
from django.utils.translation import gettext as _
import re  # regular expression operations https://docs.python.org/2/library/re.html
from datetime import date, datetime


"""
{YYMMDD} {G} {SSS} {C} {X} {Z}

{YYMMDD} is the date of birth
{G} is gender. 0-4 is female and 5-9 is male
{SSS} is a sequence number
{C} is citizenship. 0 for South Africans and 1 for other citizens
{X} is usually 8 or 9 – not clear what this is
{Z} is a check digit calculated from the other digits

Example
So for the ID number 8909025012083 we know certain things about the person:

Born on September 2nd, 1989
Male
12th male born on that date to get an ID number
South African citizen
"""


id_re = re.compile(r'^(?P<yy>\d\d)(?P<mm>\d\d)(?P<dd>\d\d)(?P<mid>\d{4})(?P<end>\d{3})')


class ZAIDField(Field):
    """A form field for South African ID numbers -- the checksum is validated
    using the Luhn checksum, and uses a simlistic (read: not entirely accurate)
    check for the birthdate
    """
    default_error_messages = {
        'invalid': _(u'Enter a valid South African ID number'),
    }

    def clean(self, value):

        super(ZAIDField, self).clean(value)

        if value in EMPTY_VALUES:
            return u''

        if len(value) < 13:
            raise ValidationError(self.error_messages['invalid'])

        # strip spaces and dashes
        value = value.strip().replace(' ', '').replace('-', '')
        match = re.match(id_re, value)

        if not match:
            raise ValidationError(self.error_messages['invalid'])

        g = match.groupdict()


        try:
            # The year 2000 is conveniently a leapyear.
            # This algorithm will break in xx00 years which aren't leap years
            # There is no way to guess the century of a ZA ID number
            d = date(int(g['yy']), int(g['mm']), int(g['dd']))
            dob = datetime.datetime.strptime(d,'%y-%m-%d').strftime('%Y-%m-%d')  # {YYMMDD} is the date of birth

        except ValueError:
            raise ValidationError(self.error_messages['invalid'])
        if not luhn(value):
            raise ValidationError(self.error_messages['invalid'])
        return value

        # 0 for South Africans and 1 for other citizens
        c = int(g['end'][0])
        if c = 0:
            return 'South African'
        elif c = 1:
            return 'Foreign'
        else:
            return 'unknown'

        # 0-4 is female and 5-9 is male
        gd = int(g['mid'][0])
        if gd < 5:
            return 'female'
        else:
            return 'male'

class ZAPostCodeField(RegexField):
    default_error_messages = {
        'invalid': _(u'Enter a valid South African postal code'),
    }

    def __init__(self, *args, **kwargs):
        super(ZAPostCodeField, self).__init__(r'^\d{4}$',
            max_length=None, min_length=None, *args, **kwargs)