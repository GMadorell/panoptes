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
        self.__arg_count = len(match_alphanumerical_in_brackets.findall(declaration))
        self.__arguments = match_alphanumerical_in_brackets.findall(declaration)

        macro_text = self.__preprocess_macro_text(macro_text)

        self.__macro_text = macro_text
        self.__macro_function = macro_function_builder.build(macro_text)

    def matches_declaration(self, declaration):
        return self.__declaration_regex.search(declaration) is not None

    def apply_declaration(self, declaration):
        assert self.matches_declaration(declaration), \
            "The given declaration(%s) doesn't match the macros declaration (%s)." % (declaration, self.__declaration)

        arguments_map = {}
        overload = 0
        for argument in self.__arguments:
            index = self.__declaration.index(argument)
            starting_value_index = index + overload
            arg_value = ""
            if index + len(argument) < len(self.__declaration):  # If the argument has a character following it.
                next_symbol = self.__declaration[index + len(argument)]
                iterating_value_index = starting_value_index
                while declaration[iterating_value_index] != next_symbol:
                    arg_value += declaration[iterating_value_index]
                    iterating_value_index += 1
                overload += (iterating_value_index - starting_value_index) - (len(argument))
            else:
                arg_value = declaration[starting_value_index:]
            arguments_map[argument] = arg_value

        #Remove brackets from the named parameters.
        for key in arguments_map.keys():
            arguments_map[key] = arguments_map[key].strip("{").strip("}")
        return self.apply_arguments(arguments_map)

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

    def test_apply_declaration_no_parameters(self):
        declaration = "hello_world"
        macro_text = \
            "print('Hello World!')"

        expected_macro_text = macro_text

        macro = Macro(declaration, macro_text)

        built_text = macro.apply_declaration("hello_world")

        self.assertEqual(built_text, expected_macro_text)

    def test_apply_declaration_one_numeric_parameter(self):
        template_declaration = "p{1}"
        template_macro_text = \
            "print(str({1}))"

        actual_declaration = "p50"
        expected_macro_text = \
            "print(str(50))"

        macro = Macro(template_declaration, template_macro_text)

        built_text = macro.apply_declaration(actual_declaration)

        self.assertEqual(built_text, expected_macro_text)

    def test_apply_declaration_two_numeric_parameters_multiple_length(self):
        template_declaration = "p{10},{200}"
        template_macro_text = \
            "print(str({10} + {200}))"

        actual_declaration = "p500,1000"
        expected_macro_text = \
            "print(str(500 + 1000))"

        macro = Macro(template_declaration, template_macro_text)

        built_text = macro.apply_declaration(actual_declaration)

        self.assertEqual(built_text, expected_macro_text)

    def test_apply_declaration_two_named_parameters(self):
        template_declaration = "p{name},{potato}"
        template_macro_text = \
            "print(str({name} + {potato}))"

        actual_declaration = "p{hi},{hello}"
        expected_macro_text = \
            "print(str(hi + hello))"

        macro = Macro(template_declaration, template_macro_text)

        built_text = macro.apply_declaration(actual_declaration)

        self.assertEqual(built_text, expected_macro_text)

    def test_apply_named_and_numeric_parameters(self):
        template_declaration = "p{name},{potato},{0},{1}"
        template_macro_text = \
            "print(str({name} + {potato} + {0} + {1}))"

        actual_declaration = "p{hi},{hello},5000000,100000"
        expected_macro_text = \
            "print(str(hi + hello + 5000000 + 100000))"

        macro = Macro(template_declaration, template_macro_text)

        built_text = macro.apply_declaration(actual_declaration)

        self.assertEqual(built_text, expected_macro_text)




