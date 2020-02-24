import operator
import datetime


# Data cache is good idea
class GithubRepo(object):

    def __init__(self, fullName, description, cloneUrl, stars, createdAt):
        self.fullName = fullName
        self.description = description
        # We can validate cloneUrl but in my opinion it's to heavy.
        self.cloneUrl = cloneUrl
        self.stars = stars
        self.createdAt = createdAt

    stars = property(operator.attrgetter('_stars'))

    @stars.setter
    def stars(self, s):
        if not int(s): raise Exception("stars must be integer")
        if not (s > 0): raise Exception("stars must be greater than zero")
        self._stars = s

    createdAt = property(operator.attrgetter('_createdAt'))

    @createdAt.setter
    def createdAt(self, s):
        if not is_expected_datetime_format(s): raise Exception("Bad date format")
        self._createdAt = s

    @staticmethod
    def fromJson(mapping):
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
    format_string = '%Y-%m-%dT%H:%M:%SZ'
    try:
        colon = timestamp[-4]
        if not colon == ':':
            return False
        datetime.datetime.strptime(timestamp, format_string)
        return True
    except ValueError:
        return False
