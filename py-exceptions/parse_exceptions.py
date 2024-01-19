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
        self.propagated_exceptions = set()  # Exceptions that are caught but not handled (re-raised)

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.functions[self.current_function] = set()
        self.propagated_exceptions = set()  # Reset for each function
        self.generic_visit(node)
        self.functions[self.current_function].update(self.propagated_exceptions)
        self.current_function = None

    def visit_Raise(self, node):
        if self.current_function:
            if isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name):
                exception_name = node.exc.func.id
                self.functions[self.current_function].add(exception_name)
                if exception_name in known_exceptions:
                    self.functions[self.current_function].update(known_exceptions[exception_name])
            elif isinstance(node.exc, ast.Name):
                self.functions[self.current_function].add(node.exc.id)
            # If there's no specific exception being raised, it might be a re-raise
            elif node.exc is None:
                self.functions[self.current_function].update(self.propagated_exceptions)
        self.generic_visit(node)

    def visit_Call(self, node):
        if self.current_function and isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in known_exceptions:
                self.functions[self.current_function].update(known_exceptions[func_name])
        self.generic_visit(node)

    def visit_Try(self, node):
        # Visit the body of the try block
        for item in node.body:
            self.visit(item)

        for handler in node.handlers:
            # If the handler is catching an exception but has no body, it's re-raising it
            if not handler.body:
                caught_exception = handler.name if handler.name else handler.type.id
                self.propagated_exceptions.add(caught_exception)
            else:
                self.generic_visit(handler)

        # Visit orelse part
        for item in node.orelse:
            self.visit(item)

        # Visit finalbody part
        for item in node.finalbody:
            self.visit(item)

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
