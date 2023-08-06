# YAPI-heureka-code

## Tokens angeben

Beispiel MuNa

```python
group = YAPIGroup(
    keywords=[
        Token("SET"),
        Token("TO"),
        Token("COUNTER"),
        Token("ITERATOR")
    ],
    operators=[
        Token("SLASH", "/"),
        Token("PIPE", "|"),
        Token("DOPPELPUNKT", ":"),
        Token("KLEINER", "<"),
        Token("GROESSER", ">")
    ],
    other=[
        TokenGroup("CharsetDefinition", [
            Token("DIGITS"),
            Token("LETTERS"),
            Token("UPPER"),
            Token("LOWER")
        ])
    ]
)
```

Hierdurch werden die Keywords, die Operatoren und andere Tokens der Sprache festgelegt. 
Hier muss dann allerdings auf Groß- und Kleinschreibung geachtet werden.
Hier wird alles großgeschrieben.

## YAPI definieren

```python
yapi = YAPI(group)
print(yapi.execute("SET <?DIGITS|2|gross?> TO <?gross?>"))
```

Über das Instanziieren der Klasse YAPI können Statements ausgeführt werden.
