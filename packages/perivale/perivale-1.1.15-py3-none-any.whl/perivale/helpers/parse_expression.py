from perivale import Buffer, ParseError

from .parse_escape_code import parse_escape_code


def parse_expression(buffer: Buffer, 
        tokens: tuple, 
        errors: list, 
        permit_newlines: bool = False, 
        escape_codes: dict = {},
        escape_tokens: bool = True) -> str:
    
    """ Parses an expression between start/end tokens

    Allows for parsing tokens with a regularly formatted start/end character,
    such as strings, html tags, and the like

    Arguments
    ---------
    buffer: Buffer
        text buffer containing an expression
    tokens: tuple
        a tuple of (start, end) tokens
    errors: list
        for error reporting
    permit_newlines: bool
        if True, allows newlines in the expression
    escape_codes: dict
        a map of permitted escape codes
    escape_tokens: bool
        if True, escapes the (start, end) tokens themselves with backslashes
    
    Returns
    -------
    expression: str
        the parsed expression
    
    Raises
    ------
    missing_token: ValueError
        if the start token isn't found
    """
    
    start_token, end_token = tokens
    if escape_tokens:
        escape_codes[f"\\{end_token}"] = end_token

    if not buffer.match(start_token, consume=True):
        raise ValueError(f"expected '{start_token}'")
    
    stack = 1
    value = start_token
    while True:

        # Check buffer not finished
        if buffer.finished() or (not permit_newlines and buffer.match("\n")):
            error = ParseError()
            error.add_excerpt(f"expected '{end_token}'", buffer.excerpt())
            errors.append(error)
            return None
        
        # Handle escape codes
        elif buffer.match("\\"):
            code = parse_escape_code(buffer, escape_codes, errors, consume=True)
            if code is None:
                return None
            value += code
    
        # Check for end token
        elif buffer.match(end_token, consume=True):
            value += end_token
            stack -= 1
            if not stack:
                break
        
        # Check for start token
        elif buffer.match(start_token, consume=True):
            value += start_token
            stack += 1
        
        # Otherwise, add to value
        else:
            value += buffer.read(consume=True)

    return value