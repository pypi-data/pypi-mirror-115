import pymorphy2

from numberize.numeric_dict import nums


class Analyzer:
    def __init__(self, lang: str):
        if lang == 'en':
            self._lang = 'en'
        else:
            self._morph = pymorphy2.MorphAnalyzer(lang=lang)

    def _get_lang(self):
        return self._lang

    def parse(self, word: str):
        return self._morph.parse(word)


class Checker:
    def __init__(self, lang: str):
        self._lang = lang

    def is_cyrillic(self, char) -> bool:
        alphabet = {
            'ru': 'абвгдеэёжзийклмнопрстуфхцшчщюяыьъ',
            'uk': 'йцукенгшщзхїєждлорпавіфячсмитьбюґ\''
        }
        return char.lower() in alphabet[self._lang]

    def _ru_get_parsed(self, parsed: list):
        possible = parsed[0]
        part_of_speech, normal_form = possible.tag.POS, possible.normal_form
        if part_of_speech == 'NUMR' or normal_form == 'сто' \
            or normal_form == 'один' \
                or normal_form in nums[self._lang].millenniums:
            return possible

    def _uk_get_parsed(self, parsed: list):
        for possible in parsed:
            if possible.tag.POS == 'NUMR' \
                    or possible.normal_form in nums[self._lang].millenniums:
                return possible

    def get_parsed(self, parsed: list):
        languages = {
            'ru': self._ru_get_parsed,
            'uk': self._uk_get_parsed
        }
        return languages[self._lang](parsed)

    def get_num(self, normal_form: str):
        return nums[self._lang].all_num[normal_form]
