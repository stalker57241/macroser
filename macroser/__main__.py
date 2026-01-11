import sys
from macroser.marker import *
from macroser.parse import *
from macroser.macrodata import *
from macroser.include import *

output_file: str | None = None

def process_arg(arg: str):
    if arg.startswith("-"):
        match arg:
            case path if path.startswith("-I"):
                include_folder(path[2:])
                return
            case macromarker if macromarker.startswith("-M"):
                global marker
                marker = macromarker[2:]
            case output if output.startswith("-o"):
                global output_file
                output_file = output[2:]
            case _:
                raise ValueError("Unknown option")

def main(argv: list[str]) -> int:
    for arg in argv[1:]:
        process_arg(arg)
    args = list(filter(lambda x: not x.startswith("-"), argv[1:]))
    print(args)
    arg = args[len(args) - 1]
    code = ""
    with open(arg, "rt+") as file:
        code = "".join(file.readlines())
    parsing = Parse(code)
    if not parsing.has_macro():
        return 0
    while parsing.has_macro():
        parsing = Parse(parsing.process())
    else:
        file = open(arg.removesuffix(".in") if output_file is None else output_file, "w")
        file.write(parsing.text.strip())
        file.close()
    return 0

if __name__ == "__main__":
    status = 0
    try:
        status = main(sys.argv)
    except Exception as e:
        print(e)
        status = 1
    finally:
        exit(status)