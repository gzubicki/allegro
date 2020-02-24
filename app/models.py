import datetime


# TODO: Change to model
# Data cache is good idea
class GithubRepo(object):
    """Object to store and validate github repo information"""

    def __init__(self, fullName, description, cloneUrl, stars, createdAt):
        self.fullName = fullName
        self.description = description
        # We can validate cloneUrl but in my opinion it's to heavy.
        self.cloneUrl = cloneUrl
        self.stars = stars
        self.createdAt = createdAt

    @property
    def fullName(self):
        return self._fullName

    @fullName.setter
    def fullName(self, s):
        if not s : raise Exception("full name can't be empty")
        self._fullName = s

    @property
    def stars(self):
        return self._stars

    @stars.setter
    def stars(self, s):
        if not s or not isinstance(s, int): raise Exception("stars must be integer")
        if not (s > 0): raise Exception("stars must be greater than zero")
        self._stars = s

    @property
    def createdAt(self):
        return self._createdAt

    @createdAt.setter
    def createdAt(self, s):
        if not is_expected_datetime_format(s): raise Exception("Bad date format")
        self._createdAt = s

    @staticmethod
    def fromJson(mapping):
        """Parse GithubRepo object from json string with map, we use other variable names"""
        if mapping is None:
            return None

        # Null if is None
        return GithubRepo(
            mapping.get('full_name'),
            mapping.get('description'),
            mapping.get('clone_url'),
            mapping.get('stargazers_count'),
            mapping.get('created_at'),
        )


def is_expected_datetime_format(timestamp):
    """We allow only ISO 8601 time format"""

    format_string = '%Y-%m-%dT%H:%M:%SZ'
    try:
        colon = timestamp[-4]
        if not colon == ':':
            return False
        datetime.datetime.strptime(timestamp, format_string)
        return True
    except ValueError:
        return False
