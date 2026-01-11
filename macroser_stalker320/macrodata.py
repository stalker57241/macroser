from typing import Literal
from pathlib import Path
from typing import Literal
from enum import Enum, auto

class MacroData:
    name: str

    def __init__(self, _name: str):
        self.name = _name

    def apply(self, *args: str) -> str:
        return ""

class MacroDataConst(MacroData):
    value: str | Literal[""]
    def __init__(self, _name: str, _value: str | Literal[""] = ""):
        super().__init__(_name)
        self.value = _value
    
    def has_value(self) -> bool:
        return self.value != ""

    def apply(self, *args: str) -> str:
        return self.value

class MacroDataExpr(MacroData):
    class Arg:
        name: str
        def __init__(self, _name: str):
            self.name = _name
        
        def __str__(self) -> str:
            return f"<Arg '{self.name}'>"

        def __repr__(self) -> str:
            return f"<Arg({super().__repr__()}) {self.name}>"
        
        def get(self) -> str:
            return self.name

    class ArgVadiadic(Arg):
        def __init__(self, _name: str):
            super().__init__(_name)

        def __str__(self) -> str:
            return f"<ArgVariadic '{self.name}'>"

        def __repr__(self) -> str:
            return f"<ArgVariadic({super(MacroDataExpr.Arg, self).__repr__()}) {self.name}>"

    args: list[Arg]
    lines: list[str]
    def __init__(self, _name: str, _args: list[str] | list[Arg], _lines: list[str]):
        super().__init__(_name)
        if len(_args) == 0:
            raise ValueError("Empty arguments")
        self.args = self.parse(_args)
        self.lines = _lines
    
    def apply(self, *args: str) -> str:
        lines = "\n".join(self.lines)
        for arg_idx in range(len(self.args)):
            arg = self.args[arg_idx]
            print(f"arg: {arg} {args[arg_idx]}")
            if isinstance(arg, MacroDataExpr.ArgVadiadic):
                match arg_idx:
                    case idx if idx == len(self.args) - 1:
                        next_args = args[idx:]
                        lines = lines.replace(f"@{arg.get()}", ", ".join(next_args))
                    case idx:
                        args_left = len(self.args) - idx + 1
                        next_args = args[idx:-args_left]
                        lines = lines.replace(f"@{arg.get()}", ", ".join(next_args))

            else:
                lines = lines.replace(f"@{arg.get()}", args[arg_idx])
        return lines

    def parse(self, _args: list[str] | list[Arg]) -> list[Arg]:
        if any(isinstance(item, str) for item in _args):
            a: list[MacroDataExpr.Arg] = []
            for arg in _args: # type: ignore
                if isinstance(arg, MacroDataExpr.Arg):
                    a.append(arg)
                if not isinstance(arg, str): continue
                if arg.endswith("..."):
                    a.append(MacroDataExpr.ArgVadiadic(arg.removesuffix("...")))
                else:
                    a.append(MacroDataExpr.Arg(arg))
            print(f"a: {str(a)}")
            return a
        else:
            if all(isinstance(item, MacroDataExpr.Arg) for item in _args):
                return _args # type: ignore
        print(f"{type(_args) is list[str]}, {type(_args) is list[MacroDataExpr.Arg]}")
        raise ValueError("Failed to parse")

def include(path: str | Path) -> list[str]:
    file = open(path, 'rt')
    macros = file.readlines()
    return macros

def includefile(path: str | Path) -> list[str]:
    lines: list[str] = include(path)
    return collect_macros(lines)

class PrefixType(Enum):
    DEFINE = auto()
    ENDDEFINE = auto()
    INCLUDE = auto()
    CONTENT = auto()
# DEFINE: 0
# ENDDEFINE: 1
# INCLUDE: 2
# CONT: 3
def parse_prefix(line: str) -> tuple[PrefixType, str]:
    match line.strip().lower():
        case line if line.startswith("define "):
            if len(line) > 7:
                return (PrefixType.DEFINE, line.removeprefix("define "))
            else:
                raise ValueError("Nothing more after prefix")
        case line if line.startswith("enddefine ") or line == "enddefine":
            return (PrefixType.ENDDEFINE, "")
            
        case line if line.startswith("include "):
            if len(line) > 8:
                return (PrefixType.INCLUDE, line.removeprefix("include "))
            else:
                raise ValueError("Nothing more after prefix")
        case line:
            return (PrefixType.CONTENT, line)


def parse_macro(macro: list[str]) -> MacroData | None:
    print(f"macro: {macro}")
    header, *lines = macro
    header_data: dict[str, str | Literal["EXPR", "CONST"] | list[str]] = {
        "name": "",
        "type": "CONST"
    } 
    if header.find("(") > 0 or header.find(")") > 0:
        if header.find("(") > 0 and header.find(")") > 0:
            header_data["type"] = "EXPR"
            header_data["name"] = header[:header.find("(")]
        else:
            raise ValueError(f"Syntax error at {header}")
    elif header.find(" ") > 0:
        header_data["type"], header_data["name"], *header_data["value"] = "CONST", *header.split(" ")
        header_data["value"] = " ".join(header_data["value"])
    elif header.find(" ") == 0:
        raise ValueError(f"Syntax error at {header}")
    else:
        header_data["type"], header_data["name"] = "CONST", header
    match header_data:
        case {"name": _name as name, "type": "EXPR"}:
            args = header[header.find("(")+1:header.find(")")]
            args_ = list(map(lambda arg: arg.strip(), args.split(",")))
            header_data["args"] = args_
            print(f"[{name}] {args_}")
            if isinstance(name, str):
                return MacroDataExpr(name, args_, lines)
            else:
                raise ValueError("Name is not str")
        case {"name": name, "type": "CONST"}:
            pass
        case _:
            print("unimplimented")
    print(f"{header_data=}")
    return None

def collect_macros(lines: list[str]) -> list[str]:
    macro_codes: list[str] = []
    macro_code: list[str] = []
    for line in lines:
        match parse_prefix(line):
            case PrefixType.DEFINE, line:
                print(0, end="")
                if len(macro_code) > 0:
                    raise ValueError("Already macro")
                print(f"line: {line.strip()}")
                macro_code.append(line.strip())
            case PrefixType.ENDDEFINE, line:
                print(1, end="")
                print(f"enddefine: '{line}'")
                print("mcode:","\n".join(macro_code))
                if len(macro_code) > 0:
                    macro_codes.append("\n".join(macro_code))
                    macro_code.clear()
                else:
                    raise ValueError("No opening DEFINE")

            case PrefixType.INCLUDE, line:
                print(2, end="")
                if len(macro_code) > 0:
                    raise ValueError("Already macro")
                includefile(line.strip().lstrip("<").rstrip(">"))
            case PrefixType.CONTENT, line:
                print(3, line)
                if len(macro_code) > 0:
                    macro_code.append(line.strip())
            
    print()
    if len(macro_code) > 0:
        macro_codes.append("\n".join(macro_code))
    print("macros: ", "\nMACRO:\n\t".join(macro_codes))
    return macro_codes
