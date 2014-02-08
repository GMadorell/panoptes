import unittest
import re
from src.collection_utilities.boolean_tests import is_there_any_duplicate
from src.regex.built_regexes import match_number_in_brackets, match_any_text, match_word_in_brackets, \
    match_alphanumerical_in_brackets


class RegexDeclarationBuilder(object):

    def build(self, declaration):
        """
        Parses macro declarations of the form:
            f{0}{1}..{n}
        Returning a compiled regex that matches it.
        """
        numeric_bracket_parts = self.get_numeric_bracket_parts(declaration)
        text_bracket_parts = self.get_text_bracket_parts(declaration)
        text_parts = self.get_text_parts(declaration)

        self.__validate_numeric_bracket_parts(declaration, numeric_bracket_parts)
        self.__validate_text_bracket_parts(declaration, text_bracket_parts)
        self.__validate_declaration(declaration)

        declaration_regex = declaration

        for result in set(text_parts):
            declaration_regex = declaration_regex.replace(result, r"%s" % result)

        for result in text_bracket_parts:
            declaration_regex = declaration_regex.replace(result, r"\{\w+\}")

        for result in numeric_bracket_parts:
            declaration_regex = declaration_regex.replace(result, r"\d+")

        declaration_regex = r"^" + declaration_regex + r"$"
        return re.compile(declaration_regex)

    def get_bracket_parts(self, declaration):
        return match_alphanumerical_in_brackets.findall(declaration)

    def get_numeric_bracket_parts(self, declaration):
        return match_number_in_brackets.findall(declaration)

    def get_text_parts(self, declaration):
        return match_any_text.findall(declaration)

    def get_text_bracket_parts(self, declaration):
        return match_word_in_brackets.findall(declaration)

    def __validate_numeric_bracket_parts(self, declaration, all_results):
        if is_there_any_duplicate(all_results):
            raise AssertionError("Macro declaration has repetitions.")
        if not self.__are_there_separations_between_results(declaration, all_results):
            raise AssertionError("Macro declaration needs separation between results.")

    def __are_there_separations_between_results(self, declaration, all_results):
        amount_results = len(all_results)
        for i, result in enumerate(all_results):
            if i != 0:
                if not self.__is_there_separation(declaration, all_results[i-1], result):
                    return False
            if i < amount_results - 1:
                if not self.__is_there_separation(declaration, all_results[i+1], result):
                    return False
        return True

    def __is_there_separation(self, declaration, first_element, second_element):
        index_first = min(declaration.index(first_element), declaration.index(second_element))
        index_second = max(declaration.index(first_element), declaration.index(second_element))

        if index_first != declaration.index(first_element):
            first_element, second_element = second_element, first_element

        return index_second - index_first > len(first_element)

    def __validate_text_bracket_parts(self, declaration, text_bracket_parts):
        if is_there_any_duplicate(text_bracket_parts):
            raise AssertionError("No repetitions in text bracket parts allowed.")

    def __validate_declaration(self, declaration):
        if self.__is_there_any_space(declaration):
            raise AssertionError("Macro declaration cannot have any space.")
        if self.__is_there_any_alphanumerical_bracket_part(declaration):
            raise AssertionError("Macro declaration can't have alphanumerical argument.")

    def __is_there_any_space(self, declaration):
        return " " in declaration

    def __is_there_any_alphanumerical_bracket_part(self, declaration):
        numeric_parts = self.get_numeric_bracket_parts(declaration)
        text_bracket_parts = self.get_text_bracket_parts(declaration)

        for part in self.get_bracket_parts(declaration):
            if part not in numeric_parts and part not in text_bracket_parts:
                return True
        return False


class RegexDeclarationBuilderTest(unittest.TestCase):
    def setUp(self):
        self.__builder = RegexDeclarationBuilder()

    def test_repeated_parameters_not_allowed(self):
        declaration = "f{0},{0}"
        with self.assertRaises(AssertionError):
            self.__builder.build(declaration)

    def test_separation_needed_between_parameters(self):
        declaration = "{0}{1}"
        with self.assertRaises(AssertionError):
            self.__builder.build(declaration)

    def test_no_alphanumerical_arguments_allowed(self):
        declaration = "{alphanumerical1}"
        with self.assertRaises(AssertionError):
            self.__builder.build(declaration)

    def test_no_spaces_allowed_here(self):
        declaration = "{0} {1}"
        with self.assertRaises(AssertionError):
            self.__builder.build(declaration)

    def test_no_parameters_single_letter(self):
        declaration = "f"
        should_match = ["f"]
        shouldnt_match = ["", " ", "fa", "f ", " f", "f1", "f100", "f1,2"]

        self.__assert_declaration_correctness(declaration, should_match, shouldnt_match)

    def test_no_parameters_complex_construct(self):
        declaration = "this,is,a,complex,construct"
        should_match = ["this,is,a,complex,construct"]
        shouldnt_match = ["this", " this,is,a,complex,construct", "this,is,a,complex,construct ",
                          " this", "this,is,a,complex,construc", "this,,,complex,construct"]

        self.__assert_declaration_correctness(declaration, should_match, shouldnt_match)

    def test_two_numerical_parameters_single_letter(self):
        declaration = "f{0},{1}"
        should_match = ["f1,2", "f10000,200000", "f0,0"]
        shouldnt_match = ["", " ", "fa", "f ", " f", "fz,0", "f0,aa0"]

        self.__assert_declaration_correctness(declaration, should_match, shouldnt_match)

    def test_two_text_parameter(self):
        declaration = "f{word},{haha}"
        should_match = ["f{something},{testing}", "f{a},{b}", "f{asdasdad},{asdasdasdadd}"]
        shouldnt_match = ["", " ", "fa,a", "f ", " f", "f{},{a}", "f{},{}", "f{a},{}"]

        self.__assert_declaration_correctness(declaration, should_match, shouldnt_match)

    def test_all_types_together(self):
        declaration = "f{word},test,{0},{1},{test}"
        should_match = ["f{hi},test,2,3,{hi}", "f{test},test,2222,3333,{very_long_word}"]
        shouldnt_match = [" f{hi},test,2,3,{hi}", "f{hi},test,2,3,{hi} ", "f{hi}, test,2,3,{hi}",
                          "f{hi},test,2,3,{h i}", "f{test},,test,2222,3333,{very_long_word}"]

        self.__assert_declaration_correctness(declaration, should_match, shouldnt_match)


    def __assert_declaration_correctness(self, declaration, should_match, shouldnt_match):
        compiled_regex = self.__builder.build(declaration)

        for match in should_match:
            self.assertTrue(compiled_regex.search(match) is not None)

        for match in shouldnt_match:
            self.assertFalse(compiled_regex.search(match) is not None)