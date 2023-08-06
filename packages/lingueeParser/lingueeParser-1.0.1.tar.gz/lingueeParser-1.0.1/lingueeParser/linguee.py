from lxml import html
import requests
from requests.exceptions import HTTPError


class Linguee:
    _linguee_url = r'https://www.linguee.com'
    _linguee_audio_url = _linguee_url + r'/mp3/'
    _languages = ['english', 'german']
    _session = requests.Session()
    _cookies = None
    _timeout = 3
    _response = ""
    _response_element = None
    _dictionary = {}

    _x_paths = {
        'main_term': '//div[@class="isMainTerm"]',
        'foreign_term': '//div[@class="isForeignTerm"]',

        'lemma': '//div[@class="exact"]',
        'main_tag': './/span[@class="tag_lemma"]/a[contains(@class, "dictLink")]',
        'main_pos': './/span[@class="tag_lemma"]/span[@class="tag_wordtype"]',
        'main_pron': './/span[@class="tag_lemma"]/a[@class="audio"]',

        'trans_lines': './/div[@class="translation_lines"]',
        'trans_tag': './/span[@class="tag_trans"]/a[contains(@class, "dictLink")]',
        'trans_pron': './/span[@class="tag_trans"]/a[@class="audio"]',
        'trans_example': './/div[contains(@class, "example_lines")]',
        'trans_example_s': './/span[contains(@class, "tag_s")]',
        'trans_example_t': './/span[contains(@class, "tag_t")]'}

    # Properties

    def get_dictionary(self):
        return self._dictionary

    def get_languages(self):
        return self._languages

    def get_response(self):
        return self._response

    def __init__(self, languages):
        self._languages = languages
        self._root_url = r'{0}/{1[0]}-{1[1]}/'.format(self._linguee_url, languages)

    def change_language(self, languages):
        self._languages = languages
        self._root_url = r'{0}/{1[0]}-{1[1]}/'.format(self._linguee_url, languages)
        self._dictionary = {}

    # Site Parsing

    def fetch_site(self, term):
        """
        f = open('linguee.html', 'rb')
        f = html.fromstring(f.read())
        self._response_element = f
        return f
        """
        linguee_search_url = self._root_url + 'search'
        params = {'source': 'auto', 'query': term}
        try:
            self._response = self._session.get(linguee_search_url,
                                               params=params,
                                               cookies=self._cookies,
                                               timeout=self._timeout)
            self._cookies = self._response.cookies
            self._response.raise_for_status()
        except HTTPError as http_err:
            print("error")
            raise http_err
        else:
            self._response_element = html.fromstring(self._response.content)
            return self._response

    # ETree Parsing

    @staticmethod
    def parse_classes(element):
        return element.attrib.get('class', '').split(' ')

    @staticmethod
    def parse_tags(element):
        tags = []
        for i in element.itertext():
            tags.append(i)
        return tags

    def parse_pronunciation(self, element):
        pron_temp = element.attrib.get('onclick', '')
        pron_temp = pron_temp[15:-2].replace('"', "").split(',')
        return list(zip([self._linguee_audio_url + x for x in pron_temp[::2]], pron_temp[1::2]))

    def parse_translation(self, line):

        trans_tag = (self.parse_tags(line.xpath(self._x_paths['trans_tag'])[0]))

        tran_pron = line.xpath(self._x_paths['trans_pron'])
        tran_pron = self.parse_pronunciation(tran_pron[0]) if tran_pron else ""

        trans_examples = []
        trans_example_elem = line.xpath(self._x_paths['trans_example'])
        for element in trans_example_elem[0] if trans_example_elem else '':
            if 'example' in self.parse_classes(element):
                tag_s = element.xpath(self._x_paths['trans_example_s'])[0].text
                tag_t = element.xpath(self._x_paths['trans_example_t'])[0].text
                trans_examples.append((tag_s, tag_t))

        trans_featured = 'featured' in self.parse_classes(line)
        return {'tag': trans_tag,
                'pronunciation': tran_pron,
                'featured': trans_featured,
                'examples': trans_examples}

    def parse_term_lemma(self, lemma):
        main_tag = self.parse_tags(lemma.xpath(self._x_paths['main_tag'])[0])

        main_pos = lemma.xpath(self._x_paths['main_pos'])
        main_pos = main_pos[0].text if main_pos else ""

        main_pron = lemma.xpath(self._x_paths['main_pron'])
        main_pron = self.parse_pronunciation(main_pron[0]) if main_pron else ""

        translations = []
        trans_lines = lemma.xpath(self._x_paths['trans_lines'])
        for line in trans_lines[0].iter():
            if 'translation' in self.parse_classes(line):
                translations.append(self.parse_translation(line))

        main_featured = 'featured' in self.parse_classes(lemma)

        return {'tag': main_tag,
                'part_of_speech': main_pos,
                'translation': translations,
                'pronunciation': main_pron,
                'featured': main_featured}

    def parse_term(self, term):
        result = []
        lemmas = term[0].xpath(self._x_paths['lemma'])
        for lemma in lemmas[0] if lemmas else "":
            if type(lemma) == html.HtmlElement and "lemma" in self.parse_classes(lemma):
                result.append(self.parse_term_lemma(lemma))
        return result

    def parse_elements(self, element, term):
        main_term = element.xpath(self._x_paths['main_term'])
        foreign_term = element.xpath(self._x_paths['foreign_term'])

        d = {term: {
            'source': self._languages[0],
            'destination': self._languages[1],
            'main_term': [],
            'foreign_term': []
        }}

        d[term]['main_term'] = self.parse_term(main_term) if main_term else None
        d[term]['foreign_term'] = self.parse_term(foreign_term) if foreign_term else None

        return d

    def get_element(self, term):
        self.fetch_site(term)
        self._dictionary.update(self.parse_elements(self._response_element, term))

    def search(self, term):
        if term not in self._dictionary:
            self.get_element(term)
        return self._dictionary[term]
