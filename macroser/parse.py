from macroser.macrodata import *
from macroser.marker import *
from macroser.macro import *
from macroser.include import find_file

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
        arglist: list[str] = list(map(lambda x: x.strip(), args.split(",")))
        match query_name:
            case "include":
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
                # for macro in macros:
                #     if not isinstance(macro, str): continue
                #     macro = parse_macro(macro)
                #     if macro is not None:
                #         push_macro(macro)
                return ""
            case "foreach":
                print("[foreach] args: ", args)
                query_name, args = args.split(",", 1)
                macro: MacroData | None = get_macro(query_name.lower())
                if macro is None:
                    raise ValueError("Macro not found")
                result: list[str] = []
                for arg in args.strip().split(","):
                    value = macro.apply(arg.strip())
                    result.append(value)
                return ",\n".join(result)
            case "optional":
                print("[optional] args: ", args)
                args = list(filter(lambda x: x != "", map(lambda x: x.strip(), args.split(","))))
                return args[0]
            case query_name:
                macro: MacroData | None = get_macro(query_name.lower())
                if macro is None:
                    raise ValueError("Macro not found")
                value = macro.apply(*arglist)
                print(f"processed: {value}")
                return value

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
