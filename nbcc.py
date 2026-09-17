# Archivo: nbcc.py
import os
import re

def compile_nova(code, output="output.py"):
    try:
        with open(code, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: El archivo '{code}' no existe.")
        return

    consts_name = []
    lista_variables = []

    py_code = [
        "import os",
        "import sys",
        "def _nova_clear(lineas=None):",
        "    if lineas is None:",
        "        os.system('cls' if os.name == 'nt' else 'clear')",
        "    else:",
        "        for _ in range(lineas):",
        "            sys.stdout.write('\\033[A\\033[K')",
        "        sys.stdout.flush()",
        "",
        "class _NovaMath:",
        "    def pow(self, b, e): return _math_real.pow(b, e)",
        "    def sqrt(self, n): return _math_real.sqrt(n)",
        "    def pi(self): return _math_real.pi",
        "math = _NovaMath()",
        "",
        "class _NovaSystem:",
        "    def exit(self): sys.exit()",
        "    def name(self): return os.name",
        "system = _NovaSystem()",
        "",
        "class _NovaColor:",
        "    def red(self, t): return f'\\033[91m{t}\\033[0m'",
        "    def green(self, t): return f'\\033[92m{t}\\033[0m'",
        "    def blue(self, t): return f'\\033[94m{t}\\033[0m'",
        "    def yellow(self, t): return f'\\033[93m{t}\\033[0m'",
        "color = _NovaColor()"
    ]
    
    level_id = 0
    comment_block = False

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()

        if comment_block:
            if "*/" in line:
                comment_block = False
            continue

        if line.startswith("/*"):
            if "*/" not in line:
                comment_block = True
            continue

        if not line or line.startswith("//"):
            continue

        if line == '}':
            level_id -= 1
            continue

        for c in consts_name:
            line = re.sub(rf'\b{c.lower()}\b', c, line)

        if line.startswith("with ") or " as " in line:
            raise SyntaxError(f"Linea {line_number}: This ain't Python bro. No 'with' allowed.")
            #This is supposed to be secret. Whatever

        spaces = "    " * level_id

        line = line.replace("userget()", "input()").replace("userget", "input()")
        line = line.replace("rand.num(", "rand.randint(")
        line = line.replace("custom ", "def ")
        line = line.replace("clear(", "_nova_clear(")
        line = line.replace("clear()", "_nova_clear()")
        line = line.replace("||", "or")
        line = line.replace("&&", "and")

        if "shout.nl(" in line:
            line = line.replace("shout.nl(", "print(")
        elif "shout(" in line:
            temporal_line = line.replace("shout(", "print(")
            if temporal_line.endswith(")"):
                line = temporal_line[:-1] + ', end="")'

        if line.startswith("#use "):
            parts = line.split(" ")
            module = parts[1]

            libraries = {
                "rand" : "random as rand",
                "sys" : "sys",
                "clock" : "time as clock"
            }

            if module in libraries:
                translated_line = f"import {libraries[module]}"
            else:
                posible_archivo_nova = f"{module}.nova"
                if os.path.exists(posible_archivo_nova):
                    compile_nova(posible_archivo_nova, f"{module}.py")
                    translated_line = f"import {module}"
                else:
                    raise ModuleNotFoundError(f"Linea {line_number}: Invalid Nova Module or File '{module}'")

        elif line == "else {":
            level_id -= 1
            else_spaces = "    " * level_id
            py_code.append(else_spaces + "else:")
            level_id += 1
            continue

        elif line.startswith("const "):
            sub_line = line.split()
            const_name = sub_line[1].upper()
            consts_name.append(const_name)

            sub_line[1] = const_name
            sub_line.pop(0)
            line = " ".join(sub_line)
            translated_line = line

        elif line.startswith("let "):
            partes = line.split("=")
            nombre_var = partes[0].replace("let ", "").strip()
            
            if nombre_var.upper() in consts_name:
                raise SyntaxError(f"Line {line_number}: '{nombre_var}' is a constant.")
                
            lista_variables.append(nombre_var)
            line = line.replace("let ", "", 1)
            translated_line = line

        elif line.endswith("{"):
            translated_line = line.replace("{", ":")
            py_code.append(spaces + translated_line)
            level_id += 1
            continue
            
        else:
            translated_line = line

        py_code.append(spaces + translated_line)
        
    with open(output, "w", encoding="utf-8") as f:
        f.write("\n".join(py_code))
        