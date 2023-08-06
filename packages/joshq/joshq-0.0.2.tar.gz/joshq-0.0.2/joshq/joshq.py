import ast
import logging


logger = logging.getLogger()
logger.debug(f'this')

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
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.Call):
                    try:
                        func_name = child.func.attr
                    except AttributeError:
                        continue
                    if func_name in ['info', 'debug', 'warning', 'error', 'exception']:
                        log_calls.append(child)
    for log_call in log_calls:
        if isinstance(log_call.args[0], ast.JoinedStr):
            raise FoundFSTringException

    return 0
