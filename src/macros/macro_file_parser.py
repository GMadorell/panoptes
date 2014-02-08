
import unittest
import StringIO
from src.macros.macro_collection import MacroCollection
from src.macros.macro_parser import MacroParser
from src.regex.built_regexes import match_macro_definitions


class MacroFileParser(object):
    def parse_file(self, file_object):
        """
        Parses a file, returning a MacroCollection instance collecting all the macros inside that file.
        """
        content = self.__read_file_content(file_object)
        macro_texts = self.__get_all_macros(content)
        macro_collection = self.__create_collection_from_macro_texts(macro_texts)
        return macro_collection

    def __read_file_content(self, file_object):
        content = file_object.read()
        return content

    def __get_all_macros(self, content):
        split = content.split("<end>")
        removed_of_start_tags = map(lambda string: string.replace("<start>", ""), split)
        trimmed_of_newlines = map(lambda string: string.strip("\n"), removed_of_start_tags)
        removed_of_empty_strings = filter(lambda string: len(string) != 0, trimmed_of_newlines)
        return removed_of_empty_strings

    def __create_collection_from_macro_texts(self, macro_texts):
        collection = MacroCollection()
        macro_parser = MacroParser()
        for macro_text in macro_texts:
            macro = macro_parser.parse(macro_text)
            collection.add(macro)
        return collection


class MacroFileParserTest(unittest.TestCase):
    def setUp(self):
        self.__parser = MacroFileParser()

    def test_file_single_macro(self):
        file_text = \
            "<start>\n" \
            "f{0}\n" \
            "for i in range({0}):\n" \
            "   pass\n" \
            "<end>"

        string_io = StringIO.StringIO(file_text)

        macro_collection = self.__parser.parse_file(string_io)

        self.assertIsNotNone(macro_collection.match("f1"))
        self.assertIsNone(macro_collection.match("f{name}"))

        string_io.close()

    def test_file_multiple_macros(self):
        file_text = \
            "<start>\n" \
            "f{0}\n" \
            "for i in range({0}):\n" \
            "   pass\n" \
            "<end>\n" \
            "<start>\n" \
            "f{0},f{1}\n" \
            "print {0} + {1}\n" \
            "<end>\n" \
            "<start>\n" \
            "f{0},f{1},f{2}\n" \
            "print {0},{1},{2}\n" \
            "<end>"

        string_io = StringIO.StringIO(file_text)

        macro_collection = self.__parser.parse_file(string_io)

        self.assertIsNotNone(macro_collection.match("f1"))
        self.assertIsNotNone(macro_collection.match("f1,f2"))
        self.assertIsNotNone(macro_collection.match("f1,f2,f3"))
        self.assertIsNone(macro_collection.match("f{name}"))

        string_io.close()

