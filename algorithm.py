from . import utils as UTILS

# this method is used to format the query
def format_lucene_query(query):
    result = ""
    tab_count = 0
    # indicates whether the entire input is quoted
    is_quoted = False
    # indicates whether we are traversing a quoted segment
    in_phrase = False
    # indicates whether the next character has to be escaped or not
    escape_on = False

    # unquote entire query
    if query[0] == '\"' and query[-1] == '\"' and len(query) >= 2:
        is_quoted = True
        query = query[1:-1]
        query = UTILS.unescape_manual(query)

    query = UTILS.remove_multiple_spaces(query, is_quoted)

    for idx in range(len(query)):
        if escape_on:
            escape_on = False
            continue

        if query[idx] == '\"':
            # toggle in_phrase when ' " ' is encountered
            in_phrase = 1 ^ in_phrase
            result += query[idx]

            # jump onto the next line after completing each quoted text segment
            if not in_phrase:
                # in case next character is neither comma(,) nor colon(:),
                # move onto the next line
                if idx >= (len(query)-1) or not UTILS.is_comma_or_colon(query[idx+1]):
                    result += UTILS.add_newline_tabs(tab_count)
            continue

        # quoted text should be printed as it is
        if in_phrase:
            result += query[idx]
            # in case quoted text contains newline character, pointer should
            # move onto the next line but should not change the current block
            if query[idx] == UTILS.NEW_LINE:
                result += UTILS.add_newline_tabs(tab_count, False)
            # escaping character
            elif query[idx] == '\\' and is_quoted and idx < (len(query)-1):
                result += query[idx+1]
                escape_on = True
            continue

        # remove exisiting spacing characters in the string
        if UTILS.is_spacing_character(query[idx]):
            if result[-1] == UTILS.TAB or result[-1] == UTILS.NEW_LINE:
                continue
            else:
                result += UTILS.add_newline_tabs(tab_count)
            continue

        # add space after colon(:)
        if query[idx] == ':':
            result += ": "
            continue

        if query[idx] == ',' or UTILS.is_opening(query[idx]):
            # add a new block when opening bracket is encountered
            tab_count += int(UTILS.is_opening(query[idx]))
            result += (query[idx] + UTILS.add_newline_tabs(tab_count))
            continue

        # end the current block whenever a closing bracket is encountered
        if UTILS.is_closing(query[idx]):
            # if the cursor has already moved onto the next line,
            # remove TAB from end as cursor needs to go back to the previous block
            # otherwise, move onto the next line, get onto the previous block
            result = result[:-1] if len(result) > 1 and result[-1] == UTILS.TAB else "{}{}".format(
                result, UTILS.add_newline_tabs(tab_count - 1))
            tab_count = max(tab_count - 1, 0)
            result += query[idx]

            if idx >= (len(query)-1) or not UTILS.is_comma_or_colon(query[idx+1]):
                result += UTILS.add_newline_tabs(tab_count)
            continue

        # in any other case, just print the character
        result += query[idx]
    return result
