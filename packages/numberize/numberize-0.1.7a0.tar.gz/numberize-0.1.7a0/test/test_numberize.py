from dataclasses import dataclass

from numberize import Numberizer
from numberize.map_text import ReplacedNumeral


@dataclass
class QuestionMapAnswer:
    text: str
    map: list
    out: str


def test_replace_by_map():
    data_set = [
        QuestionMapAnswer(
            'аодопддп', [ReplacedNumeral('_', 0, 5)], '_ддп'
        ),
        QuestionMapAnswer(
            'аодопддп',
            [ReplacedNumeral('_', 0, 5), ReplacedNumeral(5, 6, 7)],
            '_д5п'
        ),
    ]
    numba = Numberizer('ru')
    for item in data_set:
        ans = numba._replace_by_map(item.map, item.text)
        assert ans == item.out, ans


def test_replace_numerals_ru():
    text_replaced = {
        'девять-восемь, тремя миллионами, шестьсот тысяч и трёх людей':
        '9-8, 3000000, 600000 и 3 людей',
        '"сто" - слово очень простое, состоит из трёх букв':
        '"100" - слово очень простое, состоит из 3 букв',

        'двадцать пять': '25',
        'двадцать пять и семь': '25 и 7',
        'двадцать пять тысяч и Вася': '25000 и Вася'
    }
    numba = Numberizer('ru')
    for text in text_replaced:
        ans = numba.replace_numerals(text)
        assert ans == text_replaced[text], ans


def test_replace_numerals_uk():
    text_replaced = {
        """дев'ять-вісім, трьома мільйонами, шістсот тисяч та трьох людей""":
        '9-8, 3000000, 600000 та 3 людей',
        """
        "сто" - слово наївне, складається з трьох букв'
        """:
        """
        "100" - слово наївне, складається з 3 букв'
        """,

        """двадцять п'ять""": """25""",
        """двадцять п'ять та сім""": '25 та 7',
        """двадцять п'ять тисяч та Василь""": '25000 та Василь'
    }
    numba = Numberizer('uk')
    for text in text_replaced:
        ans = numba.replace_numerals(text)
        assert ans == text_replaced[text], ans


def test_replace_numerals_en():
    text_replaced = {
        """In American English, the conjunction "and" is generally not used before tens or ones: one hundred twenty-three (123); four hundred seven (407); three thousand five hundred thirty-eight (3,538); seventy-three thousand five (73,005); two million six hundred twenty-five thousand three hundred ten (2,625,310); five million three hundred thousand fifty (5,300,050).""":
        """In American English, the conjunction "and" is generally not used before tens or ones: 123 (123); 407 (407); 3538 (3,538); 73005 (73,005); 2625310 (2,625,310); 5300050 (5,300,050).""",

        """twenty-five""": '25',
        """twenty-seven and seven""": '27 and 7',
        """twenty-five thousand and Vasya""": '25000 and Vasya'
    }
    numba = Numberizer('en')
    for text in text_replaced:
        ans = numba.replace_numerals(text)
        assert ans == text_replaced[text], ans


test_replace_numerals_en()

