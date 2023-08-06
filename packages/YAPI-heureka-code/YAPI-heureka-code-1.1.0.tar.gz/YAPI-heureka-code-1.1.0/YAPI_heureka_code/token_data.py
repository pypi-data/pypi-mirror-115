class TokenOrGroup:
    def __init__(self):
        self.parents: list[Token] = []
        pass
    pass


class TokenGroup(TokenOrGroup):
    def __init__(self, name, children: list[TokenOrGroup]):
        super(TokenGroup, self).__init__()

        self.token: Token = Token(name)
        self.children: list[TokenOrGroup] = [c.__copy__() for c in children]

        pass

    def fill(self, opt_list: list = None):
        """Ergaenzt alle Parents"""

        # Sorgt dafuer, dass der optionale Parameter eine Liste ist
        if isinstance(opt_list, list) is False:
            opt_list = []

        # Durchlaeuft alle untergeordneten Tokens
        for c in self.children:
            # Fuegt das eigene Token in die Parents des untergeordneten hinzu
            c.parents.append(self.token.intern_name)

            # Durchlaeuft die restlichen Parents
            for i in opt_list + self.parents:
                c.parents.append(i)

            # Falls das untergeordnete Token eine Gruppe ist, wird dafuer das selbe aufgerufen.
            if isinstance(c, TokenGroup):
                c.fill(self.parents)
        pass

    def __getitem__(self, item):
        return self.children[item]

    def __str__(self):
        return f"<TokenGroup {self.token.intern_name}>"

    def __copy__(self):
        return TokenGroup(self.token.intern_name, [c.__copy__() for c in self.children])
    pass


class YAPIGroup(TokenGroup):
    def __init__(self, keywords: list["Token"], operators: list["Token"], other: list[TokenOrGroup]):
        self.keywords = TokenGroup("Keyword", keywords)
        self.operators = TokenGroup("Operator", operators)
        self.others = TokenGroup("Other", other)
        super(YAPIGroup, self).__init__(Token("Token"), [self.keywords, self.operators, self.others])
        pass
    pass


class Token(TokenOrGroup):
    def __init__(self, intern_name, extern_value=None):
        super(Token, self).__init__()
        self.__intern = intern_name
        self.__extern = extern_value if extern_value else intern_name
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__.split('.')[-1]} {self.intern_name}>"

    def __str__(self):
        return self.extern_value

    def __copy__(self):
        t = Token(self.intern_name, self.extern_value)
        t.parents = self.parents
        return t

    def __eq__(self, other: "Token"):
        try:
            return self.extern_value == other.extern_value and self.intern_name == other.intern_name
        except AttributeError:
            return None

    def __ne__(self, other: "Token"):
        return (self == other) is False

    @classmethod
    def from_copy(cls, o: "Token"):
        c = cls(o.intern_name, o.extern_value)
        c.parents = o.parents
        return c

    @property
    def intern_name(self):
        return self.__intern

    @property
    def extern_value(self):
        return self.__extern

    def is_child_of(self, parent: str) -> bool:
        return str(parent) in self.parents
    pass


class STRING(Token):
    def __init__(self, value):
        super(STRING, self).__init__(str(value))
        pass

    def __copy__(self):
        return STRING(self.extern_value)
    pass


class LEER(Token):
    def __init__(self):
        super(LEER, self).__init__(" ")

    def __repr__(self):
        return "<LEER>"

    def __copy__(self):
        return LEER()
    pass
