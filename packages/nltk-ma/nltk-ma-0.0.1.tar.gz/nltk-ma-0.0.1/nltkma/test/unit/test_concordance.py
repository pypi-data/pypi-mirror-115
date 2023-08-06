import unittest
from io import StringIO
from nltkma.text import find_concordance


class TestConcordance(unittest.TestCase):
    """Text constructed using: http://www.nltk.org/book/ch01.html"""

    def test_concordance_list_1(self):
        corpus_token = ['Traditionally', ',', 'black', 'Black', 'Asians', 'Blacks', 'blacks', 'bame', 'a', 'text', 'is',
                        'BAME', 'Asian', 'BAME', 'Asian', 'BAME', 'Asian', 'BAME', 'Asian', 'understood', 'minority',
                        ',', 'asian', 'to', 'be', 'a', ',' 'piece', 'of', 'written', 'or', 'spoken', 'material', '.',
                        'in', 'its', 'primary', 'form', '(', 'as', 'opposed', 'to', 'a', 'paraphrase', 'or']
        corpus_token_cleaned = ['Traditionally', 'black', 'Black', 'Asians', 'Blacks', 'blacks', 'bame', 'a', 'text',
                                'is',
                                'BAME', 'Asian', 'BAME', 'Asian', 'BAME', 'Asian', 'BAME', 'Asian', 'understood',
                                'minority',
                                'asian', 'to', 'be', 'a', 'piece', 'of', 'written', 'or', 'spoken', 'material', 'in',
                                'its',
                                'primary', 'form', '(', 'as', 'opposed', 'to', 'a', 'paraphrase', 'or']

        pivot_token = ['minority']
        target_token = ['asian']
        result = find_concordance(pivot_token, target_token, (3, 3), (1, 10), corpus_token, corpus_token_cleaned, True,
                                  True)

        expected_line = 'Asian BAME Asian understood minority , asian to be a ,piece of written or spoken material .'
        expected_left_line = 'BAME Asian understood'
        expected_left_context = 'Asian'
        expected_right_line = ', asian to be'
        expected_right_context = 'a ,piece of written or spoken material .'
        expected_query = 'minority'
        assert expected_line == result[0].line
        assert expected_left_context == result[0].left_context
        assert expected_left_line == result[0].left_span
        assert expected_query == result[0].query
        assert expected_right_line == result[0].right_span
        assert expected_right_context == result[0].right_context

    def test_concordance_list_2(self):
        corpus_token = ['Traditionally', ',', 'black', 'Black', 'Asians', 'Blacks', 'blacks', 'bame', 'a', 'text',
                        'is',
                        'BAME', 'Asian', 'BAME', 'Asian', 'BAME', 'Asian', 'BAME', 'Asian', 'understood',
                        'minority',
                        ',', 'asian', 'to', 'be', 'a', ',' 'piece', 'of', 'written', 'or', 'spoken', 'material',
                        '.',
                        'in', 'its', 'primary', 'form', '(', 'as', 'opposed', 'to', 'a', 'paraphrase', 'or']
        corpus_token_cleaned = ['Traditionally', 'black', 'Black', 'Asians', 'Blacks', 'blacks', 'bame', 'a',
                                'text',
                                'is',
                                'BAME', 'Asian', 'BAME', 'Asian', 'BAME', 'Asian', 'BAME', 'Asian', 'understood',
                                'minority',
                                'asian', 'to', 'be', 'a', 'piece', 'of', 'written', 'or', 'spoken', 'material',
                                'in',
                                'its',
                                'primary', 'form', '(', 'as', 'opposed', 'to', 'a', 'paraphrase', 'or']

        pivot_token = ['minority']
        target_token = ['asian']
        result = find_concordance(pivot_token, target_token, (3, 3), (1, 10), corpus_token, corpus_token_cleaned,
                                  True,
                                  False)

        expected_line = 'Asian BAME Asian understood minority , asian to be a ,piece of written or spoken material . ' \
                        'in its primary'
        expected_left_line = 'BAME Asian understood'
        expected_left_context = 'Asian'
        expected_right_line = ', asian to be'
        expected_right_context = 'a ,piece of written or spoken material . in its primary'
        expected_query = 'minority'
        assert expected_line == result[0].line
        assert expected_left_context == result[0].left_context
        assert expected_left_line == result[0].left_span
        assert expected_query == result[0].query
        assert expected_right_line == result[0].right_span
        assert expected_right_context == result[0].right_context

    def test_concordance_list_3(self):
        corpus_token = ['Traditionally', ',', 'black', 'Black', 'Asians', 'Blacks', 'blacks', 'bame', 'a', 'text',
                        'is',
                        'BAME', 'Asian', 'BAME', 'Asian', 'BAME', 'Asian', 'BAME', 'Asian', 'understood',
                        'minority',
                        ',', 'asian', 'to', 'be', 'a', ',' 'piece', 'of', 'written', 'or', 'spoken', 'material',
                        '.',
                        'in', 'its', 'primary', 'form', '(', 'as', 'opposed', 'to', 'a', 'paraphrase', 'or']
        corpus_token_cleaned = ['Traditionally', 'black', 'Black', 'Asians', 'Blacks', 'blacks', 'bame', 'a',
                                'text',
                                'is',
                                'BAME', 'Asian', 'BAME', 'Asian', 'BAME', 'Asian', 'BAME', 'Asian', 'understood',
                                'minority',
                                'asian', 'to', 'be', 'a', 'piece', 'of', 'written', 'or', 'spoken', 'material',
                                'in',
                                'its',
                                'primary', 'form', '(', 'as', 'opposed', 'to', 'a', 'paraphrase', 'or']

        pivot_token = []
        target_token = []
        result = find_concordance(pivot_token, target_token, (3, 3), (1, 10), corpus_token, corpus_token_cleaned,
                                  True,
                                  False)

        expected = []

        assert expected == result

    def test_concordance_list_4(self):
        corpus_token = ['Traditionally', ',', 'black', 'Black', 'Asians', 'Blacks', 'blacks', 'bame', 'a', 'text',
                        'is',
                        'BAME', 'Asian', 'BAME', 'Asian', 'BAME', 'Asian', 'BAME', 'Asian', 'understood',
                        'minority',
                        ',', 'asian', 'to', 'be', 'a', ',' 'piece', 'of', 'written', 'or', 'spoken', 'material',
                        '.',
                        'in', 'its', 'primary', 'form', '(', 'as', 'opposed', 'to', 'a', 'paraphrase', 'or']
        corpus_token_cleaned = ['Traditionally', 'black', 'Black', 'Asians', 'Blacks', 'blacks', 'bame', 'a',
                                'text',
                                'is',
                                'BAME', 'Asian', 'BAME', 'Asian', 'BAME', 'Asian', 'BAME', 'Asian', 'understood',
                                'minority',
                                'asian', 'to', 'be', 'a', 'piece', 'of', 'written', 'or', 'spoken', 'material',
                                'in',
                                'its',
                                'primary', 'form', '(', 'as', 'opposed', 'to', 'a', 'paraphrase', 'or']

        pivot_token = ['minority']
        target_token = ['Asian']
        actual = find_concordance(pivot_token, target_token, (1, 1), (1, 10), corpus_token, corpus_token_cleaned,
                                  True,
                                  False)

        expected=[]
        assert expected == actual

