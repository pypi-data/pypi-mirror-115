from .Lexer import Lexer
from .token_gruppen import YAPIGroup, TokenGruppen
from .token_data import Token


class YAPI:
    def __init__(self, group: YAPIGroup):
        self.__group: TokenGruppen = TokenGruppen(group)
        pass

    def execute(self, statement) -> list[Token]:
        lexer = Lexer(self.__group, statement)
        return lexer.tokens
    pass
