from coalib.bearlib.languages.Language import Language


@Language
class Ocaml:
    extensions = '.ml',
    comment_delimiters = {}
    multiline_comment_delimiters = {'(*': '*)'}
    string_delimiters = {'"': '"'}
    multiline_string_delimiters = {}
    indent_types = {'(': ')'}
    encapsulators = {'(': ')', '[': ']'}
    keywords = [
        'and', 'as', 'assert', 'asr', 'begin',
        'constraint', 'do', 'done', 'downto', 'else',
        'exception', 'external', 'false', 'for', 'fun',
        'functor', 'if', 'in', 'include', 'inherit',
        'land', 'lazy', 'let', 'lor', 'lsl',
        'lxor', 'match', 'method', 'mod', 'module',
        'new', 'nonrec', 'object', 'of', 'open',
        'private', 'rec', 'sig', 'struct', 'then',
        'true', 'try', 'type', 'val', 'virtual',
        'while', 'with'
    ]
    special_chars = list(r'+-*/.;\,()[]{}\=<>|&^~?%!')
    string_delimiter_escape = {'"': '\\"'}
