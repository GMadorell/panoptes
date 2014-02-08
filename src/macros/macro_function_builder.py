import unittest
from src.regex.built_regexes import match_number_in_brackets


class MacroFunctionBuilder(object):

    def build(self, macro_text):
        """
        Returns a function with signature
            def function(arguments):
        That takes a map arguments->value and applies them
        into the macro text, implementing them into the template.
        """
        macro_text = self.__remove_indentation(macro_text)

        def macro_function(arguments_dict):
            built_macro = macro_text
            for index, value in arguments_dict.items():
                built_macro = built_macro.replace(index, str(value))
            return built_macro

        return macro_function

    def __remove_indentation(self, macro_text):
        indentation_less_text = ""
        split_parts = macro_text.split("\n")
        for i, code_line in enumerate(macro_text.split("\n")):
            indentation_less_text += code_line.lstrip(r" \n")
            if i != len(split_parts) - 1:
                indentation_less_text += "\n"
        return indentation_less_text


class MacroFunctionBuilderTest(unittest.TestCase):

    def setUp(self):
        self.__builder = MacroFunctionBuilder()

    def test_no_parameters_single_line(self):
        macro = "print('Hello World!')"
        expected_built = macro

        self.__assert_correctness(macro, expected_built)

    def test_no_parameters_multiple_lines(self):
        macro = "sum = 0\n" \
                "for i in list:\n" \
                "   sum += i\n" \
                "   if sum > 0:\n" \
                "       return True"

        expected = \
                "sum = 0\n" \
                "for i in list:\n" \
                "sum += i\n" \
                "if sum > 0:\n" \
                "return True"

        self.__assert_correctness(macro, expected)

    def __assert_correctness(self, macro, expected_built, args={}):
        macro_function = self.__builder.build(macro)
        built_macro = macro_function(args)
        self.assertEqual(expected_built, built_macro)