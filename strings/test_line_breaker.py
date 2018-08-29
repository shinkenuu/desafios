from unittest import TestCase

from line_breaker import break_into_line

"""
Não fiz teste unitário por falta de tempo, ficou apenas os de "integração" que engloba os unitários
"""


class LineBreakerTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.maxDiff = None

        self.text = ['In the beginning God created the heavens',
                     'and the earth. Now the earth was',
                     'formless and empty, darkness was over',
                     'the surface of the deep, and the Spirit',
                     'of God was hovering over the waters.',
                     '\nAnd God said, "Let there be light," and',
                     'there was light. God saw that the light',
                     'was good, and he separated the light',
                     'from the darkness. God called the light',
                     '"day," and the darkness he called',
                     '"night." And there was evening, and',
                     'there was morning - the first day.']

        self.limit = 40

    def test_no_line_has_broken_words_and_uses_entire_character_limit(self):
        expected_text = '\n'.join(self.text)
        actual_text = break_into_line(' '.join(self.text), limit=self.limit)

        self.assertEqual(expected_text, actual_text)

    def test_justification_whitespaces_distribution(self):
        expected_text = '\n'.join(['In the beginning God created the heavens',
                                   'and   the  earth.   Now  the  earth  was',
                                   'formless  and empty,  darkness was  over',
                                   'the  surface of the deep, and the Spirit',
                                   'of  God was  hovering over  the  waters.']) + '\n\n'
        expected_text += '\n'.join(['And  God said, "Let there be light," and',
                                    'there  was light. God saw that the light',
                                    'was  good, and  he separated  the  light',
                                    'from  the darkness. God called the light',
                                    '"day,"   and  the   darkness  he  called',
                                    '"night."  And  there  was  evening,  and',
                                    'there  was  morning  -  the  first  day.'])

        actual_text = break_into_line(' '.join(self.text), limit=self.limit, justify=True)

        self.assertEqual(expected_text, actual_text)
