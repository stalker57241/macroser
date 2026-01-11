from typing import Callable
from macroser.macrodata import *
from macroser.marker import *
from macroser.macro import *
from macroser.include import find_file



parsers: dict[str, Callable[[str], str]] = {}
last_keyword: str = ""

def register_parser(keyword: str = "") -> Callable[[Callable[[str], str]], Callable[[str], str]]:
    def decorator(fn: Callable[[str], str]) -> Callable[[str], str]:
        parsers[keyword] = fn
        return fn
    return decorator

@register_parser()
def parse_any(args: str) -> str:
    arglist: list[str] = list(map(lambda x: x.strip(), args.split(",")))
    macro: MacroData | None = get_macro(last_keyword.lower())
    if macro is None:
        raise ValueError("Macro not found")
    value: str = apply_indents(macro.apply(*arglist))
    print(f"processed: {value}")
    return value

@register_parser("include")
def parse_include(args: str) -> str:
    print("[include] args: ", args)
    macros: list[str] = []
    match args.strip().split():
        case ["/", *arg]:
            macros = includefile("".join(arg))
        case arg:
            macros = includefile(find_file("".join(arg)))
    for macro_str in macros:
        macro = parse_macro(macro_str.splitlines())
        if macro is not None:
            push_macro(macro)
    return ""

@register_parser("foreach")
def parse_foreach(args: str) -> str:
    print("[foreach] args: ", args)
    separator, args = args.split(" ", 1)
    _is_separator_specified = separator.find("[") >= 0
    _is_separator_closed = separator.find("]") >= 0
    separator_chars: str = ""
    if _is_separator_specified:
        if _is_separator_closed:
            separator_chars = apply_indents(separator[
                separator.find("[") + 1:
                separator.find("]")])
            print("sep_chars: ", separator_chars)
        else:
            raise ValueError("Bracket not closed")
    query_name, args = args.split(",", 1)
    macro: MacroData | None = get_macro(query_name.lower())
    if macro is None:
        raise ValueError("Macro not found")
    result: list[str] = []
    for arg in args.strip().split(","):
        value = apply_indents(macro.apply(arg.strip()))
        result.append(value)
    return separator_chars.join(result)

@register_parser("first")
def parse_first(args: str) -> str:
    print("[first] args: ", args)
    _args = list(filter(lambda x: x != "", map(lambda x: x.strip(), args.split(","))))
    return _args[0]

class Parse:
    text: str = ""
    def __init__(self, _text: str):
        self.text = _text
        if self.has_macro():
            print(self.text)
        else:
            print("No macros")

    def find_macro(self, _name: str) -> int:
        if not self.has_macro(): return -1
        return self.text.find(f"{get_marker()}{_name}")

    def has_macro(self) -> bool:
        return self.text.count(get_marker()) > 0

    @staticmethod
    def process_expr(expr: str) -> str:
        query_name, args = expr.split(" ", 1)
        print(f"expr: {expr}")
        if query_name in parsers.keys():
            return parsers[query_name](args)
        global last_keyword
        last_keyword = query_name
        return parsers[""](args)
    def process(self) -> str:
        code = self.text
        macro_idx: int = code.find(get_marker())
        while macro_idx >= 0:
            macro_idx = code.find(get_marker(), macro_idx)
            next_idx = macro_idx + 1
            # print("left: ", code[next_idx:])
            match code[next_idx]:
                case '(':
                    close_bracket: int = code.find(")", next_idx)
                    _replacement = Parse.process_expr(code[next_idx + 1:close_bracket])
                    code = code.replace(f"@{code[next_idx:close_bracket + 1]}", _replacement)
                    print(f"{code=}")
                    macro_idx = code.find(_replacement, macro_idx) + len(_replacement) - 1
                case _chr:
                    # raise ValueError(f"Unexcepted {chr} occured")
                    pass
        else:
            return code
