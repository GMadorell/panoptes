import unittest
from src.macros.macro import Macro
from src.macros.regex_declaration_builder import RegexDeclarationBuilder


class MacroParser(object):

    def parse(self, macro_str):
        """
        Parses a macro of the form:
            <start>
            f{0}
            for i in xrange({0}):
                pass
            <end>
        Returning a macro instance.
        (The <start> and <end> tags are optional).
        """
        macro_str = self.__remove_start_and_end_tags(macro_str)

        splitted = macro_str.split("\n")
        declaration = splitted[0]
        macro_text = ""
        for line in splitted[1:]:
            macro_text += line + "\n"
        self.__remove_last_line_endline(macro_text)

        return Macro(declaration, macro_text)

    def __remove_start_and_end_tags(self, macro_str):
        split_lines = macro_str.split("\n")
        if split_lines[0].lower() == "<start>":
            split_lines = split_lines[1:]
        if split_lines[-1].lower() == "<end>":
            split_lines = split_lines[0:-1]

        result = ""
        for line in split_lines:
            result += line + "\n"
        result = self.__remove_last_line_endline(result)
        return result

    def __remove_last_line_endline(self, macro_text):
        if macro_text[-1] == "\n":
            macro_text = macro_text[0:-1]
        return macro_text


class MacroParserTests(unittest.TestCase):
    def setUp(self):
        self.parser = MacroParser()

    def test_one_parameter_macro_no_tags(self):
        macro_str = \
            "f{0}\n" \
            "for i in xrange({0}):\n" \
            "   pass"

        macro = self.parser.parse(macro_str)

        self.assertTrue(macro.matches_declaration("f1"))



