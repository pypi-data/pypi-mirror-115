import ast

class FoundFSTringException(Exception):
    pass

def parse(script: str):
    """
    Parses a python file and identifies logger.info/debug/warning/error/fatal
    statements and if they contain an f-string it raises FoundFSTringException
    """
    parsed = ast.parse(script)
    log_calls = []
    for node in ast.walk(parsed):
        if isinstance(node, ast.Expr):
            print(node)
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.Call):
                    func_name = child.func.attr
                    if func_name in ['info', 'debug', 'warning', 'error', 'exception']:
                        log_calls.append(child)
    for log_call in log_calls:
        if isinstance(log_calls[0].args[0], ast.JoinedStr):
            raise FoundFSTringException

    return 0
