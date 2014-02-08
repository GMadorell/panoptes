

class MacroFileParser(object):
    def parse_file(self, path):
        """
        Parses a file, returning a MacroCollection instance collecting all the macros inside that file.
        """
        content = self.__read_file_content(path)

    def __read_file_content(self, path):
        with open(path, "r") as read_file:
            content = read_file.read()
        return content