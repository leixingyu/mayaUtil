
class Asset(object):

    def __init__(self, *args, **kwargs):
        self._src = kwargs.get('src')
        self._img = kwargs.get('img')
        self._url = kwargs.get('url')
        self._id = kwargs.get('id')
