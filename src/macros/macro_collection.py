from src.macros.macro import Macro


class MacroCollection(object):
    def __init__(self):
        self.__macros = []

    def add(self, macro):
        assert isinstance(macro, Macro)
        self.__macros.append(macro)

    def match(self, declaration):
        """
        Tries to match the given declaration to all the macros inside the collection.
        Returns the matched macro if found or None if no macro is found.
        """
        for macro in self.__macros:
            if macro.matches_declaration(declaration):
                return macro
        return None