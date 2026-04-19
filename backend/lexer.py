# =========================
# 🔹 KEYWORDS
# =========================
KEYWORDS = {
    "Ghilli": "START",
    "Headmaster": "VAR",
    "ImWaiting": "PRINT",
    "Mudivu": "IF",
    "Illati": "ELSE",
    "Vattam": "LOOP",
    "Solu": "INPUT"
}

KEYWORD_LIST = list(KEYWORDS.keys())


# =========================
# 🔹 INDENT
# =========================
def get_indent(line):
    return len(line) - len(line.lstrip(" \t"))


# =========================
# 🔹 REMOVE INLINE COMMENT
# =========================
def remove_inline_comment(line):
    in_string = False
    result = []

    i = 0
    while i < len(line):
        c = line[i]

        if c == '"':
            in_string = not in_string
            result.append(c)

        elif not in_string and (
            c == "#" or
            (c == "/" and i + 1 < len(line) and line[i + 1] == "/")
        ):
            break

        else:
            result.append(c)

        i += 1

    return "".join(result).strip()


# =========================
# 🔹 REMOVE MULTILINE COMMENT
# =========================
def remove_multiline_comments(code):
    res = []
    i = 0
    in_comment = False

    while i < len(code):
        if not in_comment and code[i:i+2] == "/*":
            in_comment = True
            i += 2
            continue

        if in_comment and code[i:i+2] == "*/":
            in_comment = False
            i += 2
            continue

        if not in_comment:
            res.append(code[i])

        i += 1

    return "".join(res)


# =========================
# 🔥 SAFE KEYWORD CHECK (FIXED)
# =========================
def starts_with_keyword(line, i):
    for kw in KEYWORD_LIST:
        if line.startswith(kw, i):
            before = line[i-1] if i > 0 else " "
            end = i + len(kw)

            if (
                (i == 0 or not before.isalnum()) and
                (end == len(line) or not line[end].isalnum())
            ):
                return kw
    return None


# =========================
# 🔥 SAFE ASSIGN CHECK (FIXED)
# =========================
def is_assignment(stmt):
    in_string = False

    for i in range(len(stmt)):
        c = stmt[i]

        if c == '"':
            in_string = not in_string

        if not in_string:
            if stmt[i:i+2] in ["==", "!=", ">=", "<="]:
                continue

            if c == "=":
                return not stmt.strip().startswith("Headmaster")

    return False


# =========================
# 🔥 SPLIT STATEMENTS
# =========================
def split_statements(line):
    parts = []
    current = []
    in_string = False

    i = 0
    while i < len(line):
        c = line[i]

        if c == '"':
            in_string = not in_string
            current.append(c)
            i += 1
            continue

        # BLOCKS
        if not in_string and c in "{}":
            if "".join(current).strip():
                parts.append("".join(current).strip())
                current = []
            parts.append(c)
            i += 1
            continue

        # KEYWORD SPLIT
        if not in_string:
            kw = starts_with_keyword(line, i)
            if kw and "".join(current).strip():
                parts.append("".join(current).strip())
                current = []
                continue

        current.append(c)
        i += 1

    if "".join(current).strip():
        parts.append("".join(current).strip())

    return parts


# =========================
# 🔥 TOKENIZER
# =========================
def tokenize(code):
    tokens = []

    code = remove_multiline_comments(code)
    lines = code.split("\n")

    for line_no, raw in enumerate(lines, 1):

        if not raw.strip():
            continue

        line = remove_inline_comment(raw.strip())
        if not line:
            continue

        # 🔥 STRING VALIDATION
        if line.count('"') % 2 != 0:
            raise Exception(f"Unclosed string at line {line_no}")

        indent = get_indent(raw)

        parts = split_statements(line)

        for stmt in parts:
            stmt = stmt.strip()
            if not stmt:
                continue

            # BLOCK START
            if stmt == "{":
                tokens.append({
                    "type": "BLOCK_START",
                    "value": "{",
                    "line": line_no,
                    "indent": indent
                })
                continue

            # BLOCK END
            if stmt == "}":
                tokens.append({
                    "type": "BLOCK_END",
                    "value": "}",
                    "line": line_no,
                    "indent": indent
                })
                continue

            # ASSIGN (FIXED)
            if is_assignment(stmt):
                tokens.append({
                    "type": "ASSIGN",
                    "value": stmt,
                    "line": line_no,
                    "indent": indent
                })
                continue

            # NORMAL TOKEN
            word = stmt.split()[0]
            token_type = KEYWORDS.get(word, "UNKNOWN")

            tokens.append({
                "type": token_type,
                "value": stmt,
                "line": line_no,
                "indent": indent
            })

    return tokens