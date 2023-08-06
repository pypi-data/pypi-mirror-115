from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer


import numberize.map_text as map_text

from numberize.analyze import Analyzer, Checker


class Numberizer:
    _languages = ('ru', 'uk', 'en')

    def __init__(self, lang: str = 'ru'):
        """
        :param lang: 'ru' - russian, 'uk' - ukrainian, 'en' - english
        """
        if lang in Numberizer._languages:
            self._analyzer = Analyzer(lang)
            self._checker = Checker(lang)
        else:
            raise Exception(
                f'{lang} is not supported language.\
                 Try one of these: {Numberizer._languages}'
            )

    @classmethod
    def supported_languages(cls):
        return cls._languages

    def _replace_by_map(self, replacement_map, text) -> str:
        if hasattr(self._analyzer, '_lang'):
            new_text = []
            text = word_tokenize(text)
            prev_end = 0
            for item in replacement_map:
                new_text += text[prev_end:item.start] + [str(item.number)]
                prev_end = item.end
            return TreebankWordDetokenizer().detokenize(
                new_text + text[prev_end:]
            )

        new_text = ''
        prev_end = 0
        for item in replacement_map:
            new_text += text[prev_end:item.start] + str(item.number)
            prev_end = item.end

        return new_text + text[prev_end:]

    def replace_numerals(self, text: str) -> str:
        mapper = map_text.Mapper(self._analyzer, self._checker)
        replacement_map = mapper.get_replacement_map(text)
        return self._replace_by_map(replacement_map, text)
