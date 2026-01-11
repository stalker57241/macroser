from macroser.macrodata import MacroData
__macros: list[MacroData] = []

def push_macro(macro: MacroData):
    global __macros
    __macros.append(macro)

def get_macro(name: str) -> MacroData | None:
    for macro in __macros:
        if macro.name == name:
            return macro
    return None