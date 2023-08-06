from .token_data import TokenGroup, Token, TokenOrGroup, YAPIGroup


class TokenGruppen:
    def __init__(self, g: YAPIGroup):
        self.group = g.__copy__()
        self.group.fill()

        self.__all_end_tokens: list[Token] = []
        self.__walk(self.__all_end_tokens, self.group)
        pass

    def __walk(self, liste: list, gruppe: TokenOrGroup):
        if isinstance(gruppe, Token):
            liste.append(gruppe)
        if isinstance(gruppe, TokenGroup):
            for i in gruppe:
                self.__walk(liste, i)
        pass

    @property
    def end_tokens(self) -> list[Token]:
        return [a.__copy__() for a in self.__all_end_tokens]

    def end_tokens_for(self, parent: str) -> list[Token]:
        return [a.__copy__() for a in self.__all_end_tokens if a.is_child_of(parent)]

    def get_keywords(self):
        return self.end_tokens_for("Keyword")

    def get_operators(self):
        return self.end_tokens_for("Operator")

    def get_others(self):
        return self.end_tokens_for("Other")
    pass
