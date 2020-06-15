NEW_LINE = '\n'
RETURN = '\r'
TAB = '\t'
WHITESPACE = ' '


# Flag set to false to not include the newline character
def add_newline_tabs(tab_count, flag=True):
    tabs = TAB * max(tab_count, 0)
    return "\n"+tabs if flag else tabs


def unescape_manual(query):
    return query.replace('\\\\', '\\').replace('\\\"', '\"')


def is_opening(bracket):
    return True if bracket == '(' or bracket == '[' or bracket == '{' else False


def is_closing(bracket):
    return True if bracket == ')' or bracket == ']' or bracket == '}' else False


def is_spacing_character(ch):
    return True if ch == WHITESPACE or ch == TAB or ch == NEW_LINE or ch == RETURN else False


def is_comma_or_colon(ch):
    return True if ch == ',' or ch == ':' else False


def remove_multiple_spaces(query, is_quoted):
    query_new = ""
    in_phrase = False
    idx = 0
    while idx < len(query):
        query_new += query[idx]
        if query[idx] == '\"':
            # toggle in_phrase whenever ' " ' is encountered
            in_phrase = 1 ^ in_phrase
            idx += 1
            continue

        if in_phrase:
            # handling escape character
            if query[idx] == '\\' and is_quoted and idx < (len(query)-1):
                query_new += query[idx+1]
                idx += 1
            idx += 1
            continue

        # 'query_new=query_new[:-1]' is used to remove complete
        # space sequence when found around a comma(,) or colon(:)
        if is_spacing_character(query[idx]):
            if idx >= 1 and is_comma_or_colon(query[idx-1]):
                query_new = query_new[:-1]

            while idx < len(query) and is_spacing_character(query[idx]):
                idx += 1

            if idx < len(query) and is_comma_or_colon(query[idx]):
                query_new = query_new[:-1]
            idx -= 1
        idx += 1

    return query_new.strip()
