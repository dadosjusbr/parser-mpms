import json
import unittest

from google.protobuf.json_format import MessageToDict

from data import load
from parser import parse


class TestParser(unittest.TestCase):
    def test_jul_2019(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_07_2019.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheque-07-2019.xlsx',
                 'src/output_test/sheets/membros-ativos-verbas-indenizatorias-07-2019.xlsx']
        dados = load(files, '2019', '07', 'src/output_test')
        result_data = parse(dados, 'mpms/07/2019', '07', '2019')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)

        self.assertEqual(expected, result_to_dict)

    def test_jun_2019(self):
        self.maxDiff = None
        # # Json com a saida esperada
        with open('src/output_test/expected/expected_06_2019.json', 'r') as fp:
            expected = json.load(fp)

        files = [
            'src/output_test/sheets/membros-ativos-contracheque-06-2019.xlsx']
        dados = load(files, '2019', '06', 'src/output_test')
        result_data = parse(dados, 'mpms/06/2019', '06', '2019')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)

        self.assertEqual(expected, result_to_dict)


if __name__ == '__main__':
    unittest.main()
