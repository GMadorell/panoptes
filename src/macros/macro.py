import unittest
from src.macros.macro_function_builder import MacroFunctionBuilder
from src.macros.regex_declaration_builder import RegexDeclarationBuilder
from src.regex.built_regexes import match_number_in_brackets, match_alphanumerical_in_brackets


class Macro(object):
    def __init__(self, declaration, macro_text):
        regex_declaration_builder = RegexDeclarationBuilder()
        macro_function_builder = MacroFunctionBuilder()

        self.__validate(declaration, macro_text)

        self.__declaration = declaration
        self.__declaration_regex = regex_declaration_builder.build(declaration)

        macro_text = self.__preprocess_macro_text(macro_text)

        self.__macro_text = macro_text
        self.__macro_function = macro_function_builder.build(macro_text)
        self.__arg_count = len(match_alphanumerical_in_brackets.findall(declaration))

    def matches_declaration(self, declaration):
        return self.__declaration_regex.search(declaration) is not None

    def apply_arguments(self, arguments):
        """
        @param arguments: Map (dic) argument->value,
        """
        assert len(arguments) == self.__arg_count, \
            "Number of arguments given: %d. Expected: %d" % (len(arguments), self.__arg_count)
        return self.__macro_function(arguments)

    def __validate(self, declaration, macro_text):
        declaration_arguments = match_alphanumerical_in_brackets.findall(declaration)
        macro_text_arguments = match_alphanumerical_in_brackets.findall(macro_text)

        for argument in declaration_arguments:
            assert argument in macro_text_arguments, \
                "Macro argument mismatch. Declaration arguments were: %s, whereas macro_text arguments were: %s" \
                % (str(declaration_arguments), str(macro_text_arguments))

    def __preprocess_macro_text(self, macro_text):
        macro_text = macro_text.rstrip("\n")
        return macro_text


class MacroTests(unittest.TestCase):
    def test_no_params_declaration_should_match(self):
        macro = Macro("declaration", "macro_text")
        self.assertTrue(macro.matches_declaration("declaration"))

    def test_params_declaration_should_match(self):
        macro = Macro("f{0},{1},{name}", "some_macro_text_which_doesnt_matter{0}{1}{name}")
        self.assertTrue(macro.matches_declaration("f1,2,{hi}"))
        self.assertTrue(macro.matches_declaration("f1000,2000,{hi}"))
        self.assertFalse(macro.matches_declaration("f10002000hi"))

    def test_apply_arguments_complex(self):
        declaration = "f{0},{name}"
        macro_text = \
            "sum = 0\n" \
            "for i in range({0})\n" \
            "  sum += {name}[i]\n" \
            "return sum\n"

        arguments = {
            "{0}": 10,
            "{name}": "numbers",
        }

        expected_macro_text = \
            "sum = 0\n" \
            "for i in range(10)\n" \
            "sum += numbers[i]\n" \
            "return sum"

        macro = Macro(declaration, macro_text)

        built_text = macro.apply_arguments(arguments)

        self.assertEqual(built_text, expected_macro_text)



