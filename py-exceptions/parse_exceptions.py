import ast
import sys
from pathlib import Path

_ME = Path(sys.argv[0] if __name__ =="__main__" else __file__).resolve().name

# Manually curated list of functions and the exceptions they might raise
known_exceptions = {
    'open': {'FileNotFoundError', 'PermissionError'},
    # Add more functions and their exceptions here
    # 'function_name': {'Exception1', 'Exception2', ...},
}

class ExceptionFinder(ast.NodeVisitor):
    def __init__(self):
        self.current_function = None
        self.functions = {}

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.functions[self.current_function] = set()
        self.generic_visit(node)
        self.current_function = None

    def visit_Raise(self, node):
        if self.current_function:
            if isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name):
                exception_name = node.exc.func.id
                self.functions[self.current_function].add(exception_name)
                # Check if this exception is in the known_exceptions list
                if exception_name in known_exceptions:
                    self.functions[self.current_function].update(known_exceptions[exception_name])
            elif isinstance(node.exc, ast.Name):
                self.functions[self.current_function].add(node.exc.id)
        self.generic_visit(node)

    def visit_Call(self, node):
        if self.current_function and isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in known_exceptions:
                self.functions[self.current_function].update(known_exceptions[func_name])
        self.generic_visit(node)

    def report(self):
        for function, exceptions in self.functions.items():
            print(f"Function '{function}' may raise the following exceptions: {', '.join(exceptions) or 'None'}")

def analyze_exceptions(filename):
    with open(filename, 'r') as file:
        node = ast.parse(file.read())
    finder = ExceptionFinder()
    finder.visit(node)
    finder.report()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {_ME} <filename.py>")
    else:
        analyze_exceptions(sys.argv[1])
