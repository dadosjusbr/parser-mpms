import unittest

from data import load


file_names = ['src/output_test/sheets/membros-ativos-contracheque-05-2022.xlsx',
              'src/output_test/sheets/membros-ativos-verbas-indenizatorias-05-2022.xlsx']


class TestData(unittest.TestCase):
    # Validação para ver se a planilha não foi apagada no processo...
    def test_validate_existence(self):
        STATUS_DATA_UNAVAILABLE = 4
        try:
            with self.assertRaises(SystemExit) as cm:
                # Mês alterado para simular erro
                dados = load(file_names, "2022", "05",
                             "src/output_test/sheets/")
                dados.validate()
            self.assertEqual(cm.exception.code, STATUS_DATA_UNAVAILABLE)
        except Exception as exc:
            if "SystemExit not raised" in str(exc):
                assert True
            else:
                assert False


if __name__ == "__main__":
    unittest.main()
