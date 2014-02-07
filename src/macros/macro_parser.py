import unittest
from src.macros.regex_declaration_builder import RegexDeclarationBuilder


class MacroParser(object):
    def __init__(self):
        self.__regex_declaration_builder = RegexDeclarationBuilder()


    def parse(self, macro_str):
        """
        Parses a macro of the form:
            f{0}
            for i in xrange({0}):
                pass
        Returning a macro instance.
        """
        splitted = macro_str.split("\n")
        declaration, macro = splitted[0], splitted[1:]
        print declaration
        print macro


class MacroParserTests(unittest.TestCase):
    def setUp(self):
        self.parser = MacroParser()

    def test_one_parameter_macro(self):
        macro_str = \
            "f{0}\n" \
            "for i in xrange({0}):\n" \
            "   pass"

        macro = self.parser.parse(macro_str)



