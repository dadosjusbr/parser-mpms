import json
import unittest

from google.protobuf.json_format import MessageToDict

from data import load
from parser import parse


class TestParser(unittest.TestCase):
    def test_parser(self):
        self.maxDiff = None
        # Json com a saida esperada
        '''with open('src/output_test/expected/expected_07_2019.json', 'r') as fp:
            expected = json.load(fp)'''

        files = ['src/output_test/sheets/membros-ativos-contracheque-05-2022.xlsx',
                 'src/output_test/sheets/membros-ativos-verbas-indenizatorias-05-2022.xlsx']

        try:
            dados = load(files, '2022', '05', 'src/output_test')
            result_data = parse(dados, 'mpms/05/2022', '05', '2022')
        except:
            assert False



if __name__ == '__main__':
    unittest.main()
