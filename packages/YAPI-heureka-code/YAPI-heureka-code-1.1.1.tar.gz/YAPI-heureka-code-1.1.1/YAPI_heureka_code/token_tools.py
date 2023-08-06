from .token_data import Token


def find_inner(klasse, left: Token, tokens: list[Token], right: Token = None):
    if right is None:
        right = left.__copy__()

    groups: list[list[Token]] = []
    group: list[Token] = []

    opened = False

    for token in tokens:
        if token == left and (left != right or opened is False):
            groups.append([r.__copy__() for r in group])
            group = []
            opened = True
        elif token == right:
            groups.append(klasse([r.__copy__() for r in group]))
            group = []
            opened = False
        else:
            group.append(token)

    if len(group) > 0:
        groups.append([r.__copy__() for r in group])

    return groups


def split_by(splitter: Token, tokens: list[Token]):

    groups: list[list[Token]] = []
    group: list[Token] = []

    for token in tokens:
        if splitter == token:
            groups.append([r.__copy__() for r in group])
            group = []
        else:
            group.append(token)

    if len(group) > 0:
        groups.append([r.__copy__() for r in group])

    return groups
