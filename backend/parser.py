def parse(tokens):
    ast = []
    i = 0
    n = len(tokens)

    # =========================
    # 🔥 SAFE BLOCK COLLECTOR
    # =========================
    def collect_block(start_index):
        body = []
        depth = 1
        i = start_index

        while i < n:
            t = tokens[i]

            if t["type"] == "BLOCK_START":
                depth += 1
            elif t["type"] == "BLOCK_END":
                depth -= 1

            if depth == 0:
                return body, i

            body.append(t)
            i += 1

        raise Exception("Missing closing '}'")

    # =========================
    # 🔥 MAIN LOOP
    # =========================
    while i < n:
        token = tokens[i]
        t_type = token["type"]
        value = token["value"].strip()
        line = token["line"]

        try:
            # =========================
            # START
            # =========================
            if t_type == "START":
                ast.append({"type": "START", "line": line})

            # =========================
            # VAR
            # =========================
            elif t_type == "VAR":
                content = value.replace("Headmaster", "", 1).strip()

                if "=" not in content:
                    raise Exception("Invalid variable syntax")

                name, expr = content.split("=", 1)

                name = name.strip()
                expr = expr.strip()

                if not name:
                    raise Exception("Missing variable name")
                if not expr:
                    raise Exception("Missing value")

                ast.append({
                    "type": "VAR",
                    "name": name,
                    "expr": expr,
                    "line": line
                })

            # =========================
            # ASSIGN
            # =========================
            elif t_type == "ASSIGN":
                if "=" not in value:
                    raise Exception("Invalid assignment")

                name, expr = value.split("=", 1)

                name = name.strip()
                expr = expr.strip()

                if not name:
                    raise Exception("Missing variable name")
                if not expr:
                    raise Exception("Missing value")

                ast.append({
                    "type": "ASSIGN",
                    "name": name,
                    "expr": expr,
                    "line": line
                })

            # =========================
            # PRINT
            # =========================
            elif t_type == "PRINT":
                expr = value.replace("ImWaiting", "", 1).strip()

                if not expr:
                    raise Exception("Print requires expression")

                ast.append({
                    "type": "PRINT",
                    "expr": expr,
                    "line": line
                })

            # =========================
            # INPUT
            # =========================
            elif t_type == "INPUT":
                content = value.replace("Solu", "", 1).strip()

                if not content:
                    raise Exception("Invalid input syntax")

                prompt = None
                name = None

                if content.startswith('"'):
                    parts = []
                    in_string = True
                    buffer = ""

                    for c in content:
                        buffer += c
                        if c == '"':
                            if in_string:
                                parts.append(buffer.strip())
                                buffer = ""
                                in_string = False
                                continue
                            else:
                                in_string = True

                    remaining = content[len(parts[0]):].strip() if parts else content
                    prompt = parts[0] if parts else None

                    if remaining:
                        name = remaining.split()[-1]
                else:
                    name = content.split()[-1]

                if not name:
                    raise Exception("Missing variable name")

                ast.append({
                    "type": "INPUT",
                    "name": name.strip(),
                    "prompt": prompt,
                    "line": line
                })

            # =========================
            # IF + ELSE
            # =========================
            elif t_type == "IF":
                condition = value.replace("Mudivu", "", 1).strip()

                if not condition:
                    raise Exception("Missing IF condition")

                if i + 1 >= n or tokens[i + 1]["type"] != "BLOCK_START":
                    raise Exception("Expected '{' after IF")

                body_tokens, end_index = collect_block(i + 2)

                else_body = None
                next_i = end_index + 1

                if next_i < n and tokens[next_i]["type"] == "ELSE":
                    if next_i + 1 >= n or tokens[next_i + 1]["type"] != "BLOCK_START":
                        raise Exception("Expected '{' after ELSE")

                    else_tokens, else_end = collect_block(next_i + 2)
                    else_body = parse(else_tokens)
                    next_i = else_end + 1

                ast.append({
                    "type": "IF",
                    "condition": condition,
                    "body": parse(body_tokens),
                    "else": else_body,
                    "line": line
                })

                i = next_i
                continue

            # =========================
            # LOOP
            # =========================
            elif t_type == "LOOP":
                count = value.replace("Vattam", "", 1).strip()

                if not count:
                    raise Exception("Missing loop count")

                if i + 1 >= n or tokens[i + 1]["type"] != "BLOCK_START":
                    raise Exception("Expected '{' after LOOP")

                body_tokens, end_index = collect_block(i + 2)

                ast.append({
                    "type": "LOOP",
                    "count": count,
                    "body": parse(body_tokens),
                    "line": line
                })

                i = end_index + 1
                continue

            # =========================
            # IGNORE BLOCK TOKENS
            # =========================
            elif t_type in ("BLOCK_START", "BLOCK_END"):
                pass

            # =========================
            # UNKNOWN
            # =========================
            else:
                raise Exception(f"Unknown command '{value}'")

        except Exception as e:
            ast.append({
                "type": "ERROR",
                "message": f"Bayam ⚠️ [Line {line}]: {str(e)}",
                "line": line
            })

        i += 1

    return ast