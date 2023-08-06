from nltk.tokenize import word_tokenize
from collections import namedtuple


from numberize.analyze import Analyzer, Checker

import numberize.dict_en as dict_en

ReplacedNumeral = namedtuple('ReplacedNumeral', ['number', 'start', 'end'])


def calculate_a_num(numbers) -> int:
    res, group = 0, 0
    for num in numbers:
        if num < 1E3:
            group += num
            continue
        if group != 0:
            res += group*num
            group = 0
            continue
        res += num
    else:
        res += group
    return int(res)


def calculate_a_num_eng(numbers) -> int:
    res, h_group, m_group = 0, 0, 0
    for num in numbers:
        if num == 100:
            if h_group != 0:
                m_group += h_group*num
                h_group = 0
                continue
            m_group += num
        if num in (1000, 1000000, 1000000000):
            if h_group and m_group:
                res += (h_group+m_group)*num
                h_group, m_group = 0, 0
            elif h_group:
                res += h_group*num
                h_group = 0
            elif m_group:
                res += m_group*num
                m_group = 0
            else:
                res += num
            continue
        h_group += num
    else:
        res += m_group + h_group
    return int(res)


def eng_numeral(tok: str) -> bool:
    if not tok.isalpha():
        if '-' in tok:
            two_parts = tok.split('-')
            if len(two_parts) != 2:
                return False
            if two_parts[0] in dict_en.all_num \
                    and two_parts[1] in dict_en.all_num:
                return True
        return False
    if tok in dict_en.all_num:
        return True


class Mapper:
    def __init__(self, analyzer: 'Analyzer', checker: 'Checker'):
        self._replacement_map = []
        self._current_word = ''
        self._current_numeral = []
        self._start_of_numeral, self._end_of_numeral = None, None

        self._morph = analyzer
        self._check = checker

    def _clear(self):
        self._replacement_map = []
        self._current_word = ''
        self._current_numeral = []
        self._start_of_numeral, self._end_of_numeral = None, None

    def _update_word(self, char: str, start: int) -> None:
        if not self._current_word:
            self._start_of_numeral = start
        self._current_word += char

    def _update_replacement_map(self) -> None:
        if self._current_numeral:
            num_start = self._current_numeral[0].start
            num_end = self._current_numeral[-1].end
            num = calculate_a_num(
                (x.number for x in self._current_numeral)
            )
            self._replacement_map.append(
                ReplacedNumeral(num, num_start, num_end)
            )
            self._current_numeral = []

    def _update_numeral(self, end: int) -> None:
        self._end_of_numeral = end
        parsed = self._check.get_parsed(self._morph.parse(self._current_word))
        if parsed:
            self._current_numeral.append(
                ReplacedNumeral(
                    self._check.get_num(parsed.normal_form),
                    self._start_of_numeral,
                    self._end_of_numeral
                )
            )
        else:
            self._update_replacement_map()
        self._current_word = ''

    @staticmethod
    def _eng_replacement_map(text: str) -> list:
        numeral, replacement_map = [], []
        for i, tok in enumerate(word_tokenize(text)):
            if eng_numeral(tok):
                if '-' not in tok:
                    numeral.append(
                        ReplacedNumeral(
                            dict_en.all_num[tok],
                            i,
                            i + 1
                        )
                    )
                    continue
                l, r = tuple(tok.split('-'))
                numeral.append(
                    ReplacedNumeral(
                        dict_en.all_num[l]+dict_en.all_num[r],
                        i,
                        i + 1
                    )
                )
                continue
            if numeral:
                replacement_map.append(
                    ReplacedNumeral(
                        calculate_a_num_eng([x.number for x in numeral]),
                        numeral[0].start,
                        numeral[-1].end
                    )
                )
                numeral = []
        else:
            if numeral:
                replacement_map.append(
                    ReplacedNumeral(
                        calculate_a_num(x.number for x in numeral),
                        numeral[0].start,
                        numeral[-1].end
                    )
                )
        return replacement_map

    def get_replacement_map(self, text: str) -> list:
        self._clear()

        if hasattr(self._morph, '_lang'):
            return self._eng_replacement_map(text)

        for current_position, char in enumerate(text):
            if self._check.is_cyrillic(char):
                self._update_word(char, start=current_position)
            elif self._current_word:
                if char.isspace():
                    self._update_numeral(end=current_position)
                    continue
                self._update_numeral(end=current_position)
                self._update_replacement_map()
            elif not char.isspace():
                self._update_replacement_map()
        else:
            if self._current_word:
                self._update_numeral(end=len(text))
                self._update_replacement_map()
            if self._current_numeral:
                self._update_replacement_map()
        return self._replacement_map


