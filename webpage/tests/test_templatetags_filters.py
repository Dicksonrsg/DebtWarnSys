import unittest

from webpage.templatetags.filters import format_cnpj, format_cpf


class TemplatetagsFiltersTests(unittest.TestCase):
    def test_format_cpf(self):
        cpf = "74843500011"
        formatted_cpf = format_cpf(cpf)
        self.assertEqual(formatted_cpf, "748.435.000-11")

    def test_format_cnpj(self):
        cnpj = "23741365000172"
        formatted_cnpj = format_cnpj(cnpj)
        self.assertEqual(formatted_cnpj, "23.741.365/0001-72")

    def test_format_cpf_with_empty(self):
        cpf = ""
        formatted_cpf = format_cpf(cpf)
        self.assertEqual(formatted_cpf, "000.000.000-00")

    def test_format_cnpj_with_empty(self):
        cnpj = ""
        formatted_cnpj = format_cnpj(cnpj)
        self.assertEqual(formatted_cnpj, "00.000.000/0000-00.")

    def test_format_cpf_raise_exception(self):
        self.assertRaises(Exception, format_cpf())

    def test_format_cnpj_raise_exception(self):
        self.assertRaises(Exception, format_cnpj)
