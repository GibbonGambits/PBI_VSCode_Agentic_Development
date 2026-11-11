#!/usr/bin/env python3
"""A one-pass scanner for DAX and Power Query (M) formulas.

The checks in scripts/check_project.py never match a pattern against raw formula text. They read the
formula once, character by character, with this scanner, and then work on what it returns. The scanner
is always in exactly one of six states:

    code            everything else: functions, operators, numbers, keywords, unquoted names
    text            a text value in double quotes ("" is a quote inside the text)
    line comment    from // to the end of the line (in DAX also from --)
    block comment   from /* to */
    quoted name     DAX: a table name in single quotes ('' is a quote inside the name)
                    Power Query: a quoted identifier, #"..." ("" is a quote inside the name)
    bracket name    DAX: a column or measure name in square brackets (]] is a bracket inside the name)
                    Power Query: a field picked from a record or a row, such as [Amount]

The two languages have separate rules:

    DAX          --  starts a comment;  '...' is a table name;  every [ starts a name
    Power Query  --  is two minus signs;  ' is an ordinary character;  #"..." is a name;  a [ starts a
                 name only when it picks one field. A record ([A = 1]), a record type and a list of
                 fields ([[A], [B]]) stay code, because code can sit inside them.

Sources for the rules: Microsoft Learn, "DAX syntax" (https://learn.microsoft.com/dax/dax-syntax-reference)
and the Power Query M language specification, "Lexical structure"
(https://learn.microsoft.com/powerquery-m/m-spec-lexical-structure).

This is a scanner, not a parser: it knows where names, text and comments are, and how brackets nest.
It does not know what a formula means. Needs Python 3.8 or later. Uses the standard library only.
"""
import re
from collections import namedtuple

DAX = "dax"
M = "m"

CODE = "code"
TEXT = "text"
LINE_COMMENT = "line comment"
BLOCK_COMMENT = "block comment"
QUOTED_NAME = "quoted name"
BRACKET_NAME = "bracket name"
STATES = (CODE, TEXT, LINE_COMMENT, BLOCK_COMMENT, QUOTED_NAME, BRACKET_NAME)
COMMENTS = (LINE_COMMENT, BLOCK_COMMENT)

# kind: 'word', 'number', 'symbol', or one of the five states that are not code.
# value: for a name or a text, what it holds (quotes and brackets removed, doubled marks undone).
Token = namedtuple("Token", "kind value start end line")
Call = namedtuple("Call", "name at open close args")      # token positions; args: list of (first, last + 1)

# Power Query: a '[' that picks one field. It holds one name (plain or #"quoted") and nothing else.
_M_FIELD = re.compile(r'\[\s*(?:#"(?:[^"]|"")*"|[^\[\]"=,(){}\r\n]*[^\[\]"=,(){}\s])\s*\]')
_WORD = re.compile(r"#?[^\W\d][\w.]*")
_NUMBER = re.compile(r"(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?")
_TWO = ("&&", "||", "<>", "<=", ">=", "==", "=>", "..", "??", ":=")
_OPEN = "([{"
_CLOSE = ")]}"
# Words that can stand directly before '[Name]' without being a table.
DAX_KEYWORDS = frozenset(("RETURN", "VAR", "IN", "NOT", "AND", "OR", "DEFINE", "EVALUATE", "MEASURE", "COLUMN",
                          "TABLE", "ORDER", "BY", "ASC", "DESC", "START", "AT", "TRUE", "FALSE", "FUNCTION"))


def _end_of_quoted(text, start, mark):
    """Position after the closing mark of a value that starts at 'start' (just after its opening mark)."""
    position = start
    size = len(text)
    while position < size:
        if text[position] == mark:
            if text[position + 1:position + 2] == mark:
                position += 2
                continue
            return position + 1
        position += 1
    return size


def segments(text, language):
    """The whole formula as a list of (state, start, end), in order, with nothing left out."""
    out = []
    size = len(text)
    position = 0
    code_from = 0

    def close_code(upto):
        if upto > code_from:
            out.append((CODE, code_from, upto))

    while position < size:
        char = text[position]
        pair = text[position:position + 2]
        state = None
        begin = position
        if pair == "/*":
            end = text.find("*/", position + 2)
            end = size if end < 0 else end + 2
            state = BLOCK_COMMENT
        elif pair == "//" or (language == DAX and pair == "--"):
            end = position
            while end < size and text[end] not in "\r\n":
                end += 1
            state = LINE_COMMENT
        elif char == '"':
            end = _end_of_quoted(text, position + 1, '"')
            if language == M and position > code_from and text[position - 1] == "#":
                begin = position - 1
                state = QUOTED_NAME
            else:
                state = TEXT
        elif char == "'" and language == DAX:
            end = _end_of_quoted(text, position + 1, "'")
            state = QUOTED_NAME
        elif char == "[":
            if language == DAX:
                end = _end_of_quoted(text, position + 1, "]")
                state = BRACKET_NAME
            else:
                field = _M_FIELD.match(text, position)
                if field:
                    end = field.end()
                    state = BRACKET_NAME
        if state is None:
            position += 1
            continue
        close_code(begin)
        out.append((state, begin, end))
        position = code_from = end
    close_code(size)
    return out


def blank(text, language, keep=(CODE, QUOTED_NAME, BRACKET_NAME)):
    """The formula with every state that is not in 'keep' replaced by spaces. Length and line breaks stay."""
    parts = []
    for state, start, end in segments(text, language):
        piece = text[start:end]
        parts.append(piece if state in keep else re.sub(r"[^\r\n]", " ", piece))
    return "".join(parts)


def _name_value(text, state, language):
    if state == TEXT:
        body = text[1:-1] if len(text) >= 2 and text.endswith('"') else text[1:]
        return body.replace('""', '"')
    if state == QUOTED_NAME:
        if language == M:
            body = text[2:-1] if len(text) >= 3 and text.endswith('"') else text[2:]
            return body.replace('""', '"')
        body = text[1:-1] if len(text) >= 2 and text.endswith("'") else text[1:]
        return body.replace("''", "'")
    if state == BRACKET_NAME:
        body = text[1:-1] if text.endswith("]") and len(text) >= 2 else text[1:]
        if language == M:
            body = body.strip()
            if body.startswith('#"') and body.endswith('"') and len(body) >= 3:
                body = body[2:-1].replace('""', '"')
            return body
        return body.replace("]]", "]")
    return text


def tokens(text, language, comments=False):
    """The formula as a list of Token. Comments are left out unless comments is true."""
    out = []
    line = 1
    cursor = 0
    for state, start, end in segments(text, language):
        line += len(re.findall(r"\r\n|\r|\n", text[cursor:start]))
        cursor = start
        piece = text[start:end]
        if state != CODE:
            if comments or state not in COMMENTS:
                out.append(Token(state, _name_value(piece, state, language), start, end, line))
            continue
        position = 0
        size = len(piece)
        local_line = line
        while position < size:
            char = piece[position]
            if char in " \t\r\n\f\v ":
                if char == "\n" or (char == "\r" and piece[position + 1:position + 2] != "\n"):
                    local_line += 1
                position += 1
                continue
            match = _NUMBER.match(piece, position) if char.isdigit() or char == "." else None
            kind = "number"
            if match is None:
                match = _WORD.match(piece, position)
                kind = "word"
            if match is None or match.end() == position:
                kind = "symbol"
                width = 2 if piece[position:position + 2] in _TWO else 1
                value = piece[position:position + width]
            else:
                value = match.group(0)
                width = len(value)
            out.append(Token(kind, value, start + position, start + position + width, local_line))
            position += width
    return out


def is_symbol(token, value):
    return token is not None and token.kind == "symbol" and token.value == value


def match_close(stream, opener):
    """Position of the token that closes the bracket opened at 'opener'; len(stream) when it never closes."""
    depth = 0
    for position in range(opener, len(stream)):
        token = stream[position]
        if token.kind != "symbol":
            continue
        if token.value in _OPEN:
            depth += 1
        elif token.value in _CLOSE:
            depth -= 1
            if depth == 0:
                return position
    return len(stream)


def split_arguments(stream, opener, closer):
    """(first, last + 1) token positions of each argument between an opening bracket and its closing one."""
    args = []
    depth = 0
    first = opener + 1
    for position in range(opener + 1, closer):
        token = stream[position]
        if token.kind != "symbol":
            continue
        if token.value in _OPEN:
            depth += 1
        elif token.value in _CLOSE:
            depth -= 1
        elif token.value == "," and depth == 0:
            args.append((first, position))
            first = position + 1
    if closer > opener + 1 or args:
        args.append((first, closer))
    return args


def calls(stream):
    """Every function call in a token list: a word directly followed by '('. Names are returned in capitals."""
    out = []
    for position, token in enumerate(stream[:-1]):
        if token.kind == "word" and is_symbol(stream[position + 1], "("):
            closer = match_close(stream, position + 1)
            out.append(Call(token.value.upper(), position, position + 1, closer,
                            split_arguments(stream, position + 1, closer)))
    return out


def dax_variables(stream):
    """Names a DAX formula declares with VAR, in lower case."""
    return {stream[i + 1].value.lower() for i, token in enumerate(stream[:-1])
            if token.kind == "word" and token.value.upper() == "VAR" and stream[i + 1].kind == "word"}


def dax_references(stream):
    """Every [Name] of a DAX formula as (table or None, name, position of the bracket token).

    The table is the quoted name or the word that stands directly before the bracket, unless that word
    is a DAX keyword such as RETURN or a variable of this formula.
    """
    names = dax_variables(stream)
    out = []
    for position, token in enumerate(stream):
        if token.kind != BRACKET_NAME:
            continue
        before = stream[position - 1] if position else None
        table = None
        if before is not None and before.kind == QUOTED_NAME:
            table = before.value
        elif (before is not None and before.kind == "word" and before.value.upper() not in DAX_KEYWORDS
              and before.value.lower() not in names):
            table = before.value
        out.append((table, token.value, position))
    return out


def text_of(stream, first=0, last=None, source=None):
    """A canonical one-line text of a token range: used to compare two formulas or two parts of one."""
    parts = []
    for token in stream[first:last]:
        if token.kind == TEXT:
            parts.append('"%s"' % token.value.replace('"', '""'))
        elif token.kind == QUOTED_NAME:
            parts.append("'%s'" % token.value.lower())
        elif token.kind == BRACKET_NAME:
            parts.append("[%s]" % token.value.lower())
        elif token.kind == "word":
            parts.append(token.value.upper())
        elif token.kind not in COMMENTS:
            parts.append(token.value)
    return " ".join(parts)


def m_steps(text):
    """The steps of the outer 'let' of a Power Query query.

    Returns (steps, found): found is False when the query has no 'let'. Each step is a dict with
    name, line, described (a comment sits directly above it, or ends the line above) and on_let_line.
    """
    stream = tokens(text, M, comments=True)
    start = None
    for position, token in enumerate(stream):
        if token.kind == "word" and token.value == "let":
            start = position
            break
    if start is None:
        return [], False
    lines = re.split(r"\r\n|\r|\n", text)
    steps = []
    depth = 0
    inner = []                 # bracket depth at which each inner 'let' opened
    expect = True              # the next name at depth 0 starts a step
    let_line = stream[start].line
    comment_ends = {}          # line number -> a comment with words ends on that line
    for token in stream:
        if token.kind in COMMENTS:
            body = text[token.start:token.end]
            words = body[2:-2] if token.kind == BLOCK_COMMENT else body[2:]
            if words.strip():
                comment_ends[token.line + len(re.findall(r"\r\n|\r|\n", body))] = token
    position = start + 1
    while position < len(stream):
        token = stream[position]
        if token.kind in COMMENTS:
            position += 1
            continue
        if token.kind == "symbol":
            if token.value in _OPEN:
                depth += 1
            elif token.value in _CLOSE:
                depth = max(depth - 1, 0)
            elif token.value == "," and depth == 0 and not inner:
                expect = True
            position += 1
            continue
        if token.kind == "word" and token.value == "let":
            inner.append(depth)
            position += 1
            continue
        if token.kind == "word" and token.value == "in":
            if inner and inner[-1] == depth:
                inner.pop()
            elif depth == 0 and not inner:
                break
            position += 1
            continue
        following = stream[position + 1] if position + 1 < len(stream) else None
        after = position + 2
        while following is not None and following.kind in COMMENTS:
            following = stream[after] if after < len(stream) else None
            after += 1
        if (expect and depth == 0 and not inner and token.kind in ("word", QUOTED_NAME)
                and is_symbol(following, "=")):
            shown = text[token.start:token.end]
            above = token.line - 1
            described = False
            if above in comment_ends and above >= 1:
                comment = comment_ends[above]
                first_line = comment.line
                # the comment must stand alone on its line or lines: nothing but spaces before it
                before = lines[first_line - 1][:comment.start - _line_start(text, first_line)]
                described = not before.strip()
            steps.append({"name": shown, "line": token.line, "described": described,
                          "on_let_line": token.line == let_line})
            expect = False
        position += 1
    return steps, True


def _line_start(text, line):
    """Offset of the first character of a 1-based line number."""
    offset = 0
    for _ in range(line - 1):
        match = re.compile(r"\r\n|\r|\n").search(text, offset)
        if match is None:
            return len(text)
        offset = match.end()
    return offset
