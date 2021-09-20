import requests
from bs4 import BeautifulSoup
from json import loads
from urllib.parse import unquote
from html import unescape



class Song:
    def __init__(self, author, name, album, urlApple, urlDeezer):
        self.author = author
        self.name = name
        self.album = album
        self.urlApple = urlApple
        self.urlDeezer = urlDeezer
        self.links = dict() # {'appl':'link-apple-music', 'deez':'link_to deezer'}

    def __str__(self):
        return str(self.author) + ' ' + str(self.name)

    def return_name(self):
        return str(self.author) + str(self.name) + str(self.album) + str(self.urlApple) + str(self.urlDeezer)


class Album:
    def __init__(self, author, name):
        self.author = author
        self.name = name

    def __str__(self):
        return str(self.author) + str(self.name)

    def return_name(self):
        return str(self.author) + str(self.name)


class AppleMusic:
    def __init__(self):
        self._BASE_SEARCH_URL = 'https://itunes.apple.com/search'
        self.params = {'en': 'ru',
                      'entity': 'musicTrack'}

    def _find_song_name(self, link):
        """Поиск навазния трека по ссылке"""
        page = BeautifulSoup(requests.get(link).text, 'html.parser')
        track_name = unquote(link).split('/')
        author = page.find(class_='dt-link-to').string.strip()
        album = page.find(class_='album-header-metadata').find(class_='clamp-4').getText().strip()
        return Song(unescape(author), unescape(track_name[5].replace('-',' ')), unescape(album), link, '')

    def _link_to_album(self, link):
         """Поиск навазния Альбома по ссылке"""
        page = BeautifulSoup(requests.get(link).text, 'html.parser')
        album_schema = page.find('script', type='application/ld+json')
        page_info = loads(album_schema.string)
        return unescape(page_info['name'], unescape(page_info['byArtist']['name']))

    def _find_song_link(self, query):
         """Поиск ссылки на трек по названию"""
        self.params['term']=query
        results = requests.get(self._BASE_SEARCH_URL, params=self.params)
        res_json = results.json()
        try: song_link = res_json['results'][0]['trackViewUrl']
        except IndexError:
            print(res_json)
        return Song('', '', '', song_link, '')


class Deezer:
    def __init__(self):
        self.deezer_api_link = 'https://api.deezer.com/search'
        self._BASE_SEARCH_URL = 'https://api.deezer.com/search'

    def _find_song_name(self,link):
         """Поиск навазния трека по ссылке"""
        page = BeautifulSoup(requests.get(link).text, 'html.parser')
        track_name = page.find(class_='heading-1').find('span').string.strip()
        author = page.find_all('a')[1].find('span').string.strip()
        return Song(unescape(author), unescape(track_name), '', '', link)

    def _link_to_album(self, link):
        """Поиск навазния Альбома по ссылке"""
        pass

    def _find_song_link(self, query):
         """Поиск ссылки на трек по названию"""
        params = {'q': query}
        link = self.deezer_api_link
        results = requests.get(self.deezer_api_link, params=params)
        res_json = results.json()
        return Song('', '', '', '', res_json['data'][0]['link'])


class YandexMusic:
    def __init__(self):
        pass


def return_value(link):
    """тестовая фунция работает только с Deezer и Apple Music"""
    input_link = unquote(link).split('/')

    try:
        if input_link[2] == 'music.apple.com':
            input_song = AppleMusic()._find_song_name(link)
            return_song = Deezer()._find_song_link(Song.__str__(input_song))
            ret = Song.return_name(return_song)
        elif input_link[2] == 'www.deezer.com':
            input_song = Deezer()._find_song_name(link)
            return_song= AppleMusic()._find_song_link(Song.__str__(input_song))
            ret = Song.return_name(return_song)
    except: ret = 'Oops! We have some troubles... Unsupported link type.'

    return str(ret)


# Тесты
print(return_value('https://www.deezer.com/track/928871872'))
print(return_value('https://music.apple.com/ru/album/plains/793928184?i=793928286&l=en'))
print(return_value('https://www.deezer.com/us/track/75559487'))
print(return_value('https://music.apple.com/us/album/%D0%BC%D0%B0%D0%BB%D0%BE-%D0%BD%D0%B0%D0%BC/1507137236?i=1507137407&uo=4'))
