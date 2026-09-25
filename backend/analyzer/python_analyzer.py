import ast
from pathlib import Path
class PythonAnalyzer:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
    def calculate_complexity(self, function_node):
        complexity = 1
        for node in ast.walk(function_node):
            if isinstance(
                node,
                (
                    ast.If,
                    ast.For,
                    ast.While,
                    ast.ExceptHandler,
                    ast.IfExp
                )
            ):
                complexity += 1
            # Boolean conditions
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        return complexity
    def analyze(self):
        source_code = self.file_path.read_text(
            encoding="utf-8"
        )
        tree = ast.parse(source_code)
        functions = []
        classes = []
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self.calculate_complexity(node)
                function_length = (
                    node.end_lineno - node.lineno + 1
                )
                argument_count = len(node.args.args)
                if (
                    node.args.args
                    and node.args.args[0].arg == "self"
                ):
                    argument_count -= 1
                functions.append({
                    "name": node.name,
                    "arguments": argument_count,
                    "complexity": complexity,
                    "length": function_length
                })
            elif isinstance(node, ast.AsyncFunctionDef):
                complexity = self.calculate_complexity(node)
                function_length = (
                    node.end_lineno - node.lineno + 1
                )
                argument_count = len(node.args.args)
                if (
                    node.args.args
                    and node.args.args[0].arg == "self"
                ):
                    argument_count -= 1
                functions.append({
                    "name": node.name,
                    "arguments": argument_count,
                    "complexity": complexity,
                    "length": function_length
                })
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.Import):
                for name in node.names:
                    imports.append(name.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        lines_of_code = len(
            source_code.splitlines()
        )
        return {
            "file": self.file_path.name,
            "lines_of_code": lines_of_code,
            "functions": functions,
            "classes": classes,
            "imports": imports
        }