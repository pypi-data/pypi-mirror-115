from .token_gruppen import *
from .token_data import *


class Lexer:
    def __init__(self, group: TokenGruppen, statement: str):
        self.__group = group
        self.statement = statement
        self.tokens = []
        self.__make_tokens()
        pass

    def __make_tokens(self):
        aktueller_string = ""
        position = 0
        while position < len(self.statement):
            zeichen = self.statement[position]
            if zeichen not in [o.extern_value for o in self.__group.get_operators()]:

                set_new = True
                if zeichen != " ":
                    aktueller_string += zeichen
                    set_new = False

                elif aktueller_string in [k.extern_value for k in self.__group.get_keywords()]:
                    self.tokens.append([Token.from_copy(k) for k in self.__group.get_keywords()
                                        if k.extern_value == aktueller_string][0])

                elif aktueller_string in [k.extern_value for k in self.__group.get_others()]:
                    self.tokens.append([Token.from_copy(k) for k in self.__group.get_others()
                                        if k.extern_value == aktueller_string][0])

                elif aktueller_string != "":
                    self.tokens.append(STRING(aktueller_string))
                if set_new:
                    aktueller_string = ""

                if zeichen == " ":
                    self.tokens.append(LEER())

            else:
                if aktueller_string in [k.extern_value for k in self.__group.get_keywords()]:
                    self.tokens.append([Token.from_copy(k) for k in self.__group.get_keywords()
                                        if k.extern_value == aktueller_string][0])

                elif aktueller_string in [k.extern_value for k in self.__group.get_others()]:
                    self.tokens.append([Token.from_copy(k) for k in self.__group.get_others()
                                        if k.extern_value == aktueller_string][0])
                elif aktueller_string != "":
                    self.tokens.append(STRING(aktueller_string))

                self.tokens.append([Token.from_copy(k) for k in self.__group.get_operators()
                                    if k.extern_value == zeichen][0])

                aktueller_string = ""
            position += 1
        pass
