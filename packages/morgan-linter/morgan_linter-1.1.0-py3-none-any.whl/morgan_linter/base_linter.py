import ast
import os
from typing import NamedTuple

class Violation(NamedTuple):
    """
    Every rule violation contains a node that breaks the rule,
    and a message that will be shown to the user.
    """

    node: ast.AST
    message: str
    
class Checker(ast.NodeVisitor):
    """
    A Checker is a Visitor that defines a lint rule, and stores all the
    nodes that violate that lint rule.
    """
    
    def __init__(self, issue_code):
        self.issue_code = issue_code
        self.violations: set[Violation] = set()
        

class Linter:
    """Holds all list rules, and runs them against a source file."""

    def __init__(self):
        self.checkers: set[Checker] = set()
        self.len_violations = 0
        self.len_functions_analyzed = 0
        self.evaluation = 0
        self.min_value = 10
        self.violations: set[Checker] = set()

    @staticmethod        
    def count_functions(tree):
        """
        Count the number of functions in a Python module.
        
        Args:
          
          - tree (ast): The AST of the module
        
        Returns:
          
          The number of functions in the module.
        """        
        #Get all functions in the module
        functions = [_function for _function in ast.walk(tree) if isinstance(_function, ast.FunctionDef)]

        return len(functions)
    
    def calculate_results(self):
        """
        Takes the minimum value and the number of violations and divides
        them by the number of functions analyzed.
        """
        try:
            if self.len_functions_analyzed == 0:
                self.len_functions_analyzed = 1
            evaluation = self.min_value - self.len_violations/self.len_functions_analyzed
            assert evaluation == 10
            print(f"Score: {evaluation}/10.  Min value: {self.min_value}. It's ok!")
        except AssertionError:
            raise SystemExit(f"Your score is {evaluation}. The minimum value is {self.min_value}.")

    def _count_functions_analized(self, tree):
        """
        This function counts the number of functions in a file and adds it to the total number of
        functions in the project.
        
        Args:
          
          - tree: the AST of the file
        """
        len_functions_analyzed = self.count_functions(tree)
        self.len_functions_analyzed += len_functions_analyzed
        
    def _print_violations(self, checker: Checker, file_name: str):
        """
        It prints the violations found by the checker.
        
        Args:
            
            - checker: The checker object that is running the check
            - file_name: The name of the file being checked
        """
        for node, message in checker.violations:
            print(
                f"{file_name}:{node.lineno}:{node.col_offset}: "
                f"{checker.issue_code}: {message}"
            )
            self.len_violations += 1

    def run(self, source_path, is_testing):
        """Runs all lints on a source file."""
        file_name = os.path.basename(source_path)
        
        with open(source_path) as source_file:
            source_code = source_file.read()

        tree = ast.parse(source_code)

        if "__init__.py" not in file_name and len(tree.body) > 0:                
            for checker in self.checkers:
                checker.violations = set()
                checker.visit(tree)
                self._print_violations(checker, file_name)
            
            if not is_testing:
                self._count_functions_analized(tree)
