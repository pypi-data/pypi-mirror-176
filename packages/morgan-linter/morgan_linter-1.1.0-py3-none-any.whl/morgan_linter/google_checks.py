import ast
import re

try:
    from base_linter import Checker, Violation
    from utils import check_bad_words_score, at_least_n_words, get_docstrings
except ModuleNotFoundError:
    from morgan_linter.base_linter import Checker, Violation
    from morgan_linter.utils import check_bad_words_score, at_least_n_words, get_docstrings

class GoogleAuxiliar():
    """Auxiliar class to operate with google formats and sections."""
    def __init__(self):        
        self.docstring = None
    
    def _check_section(self, section):
        """
        This function checks if a specific section exist in the documentation.
        
        Args:
          
          - section: The section of the documentation to check
        
        Returns:
          
          A boolean value
        """
        if self.docstring is None:
            return False

        #Check if a specific section exist in the documentation.
        if not section in self.docstring:        
            return False
        
        return True
    
    def _get_return_section(self):
        """
        Return the "Returns" section in a google docstrings format.
        
        Returns:
          
          The return section of the docstring.
        """
        return_section = self.docstring.split("Returns")[1]

        return return_section

    def _get_description_section(self):
        """
        Return the "description" section in a google docstrings format.
        
        Returns:
          
          The description section of the docstring.
        """
        description_section = self.docstring.split("Args:")[0]

        return description_section

    def _get_args_section(self, is_return_section):
        """
        This function returns the section of the docstring that contains the arguments.
        
        Args:
          
          - is_return_section (bool): if True, split docstring to ommit the "returns" section
        
        Returns:
          
          The arguments section of the docstring.
        """
        args_section = self.docstring.split("Args:")[1]
                
        if is_return_section:
            args_section = args_section.split("Returns:")[0]

        return args_section


class SectionChecker(Checker, GoogleAuxiliar):
    """DOCS-001: bad section format (it is not found Args or return section)"""
    def __init__(self, issue_code):
        super().__init__(issue_code)
        self.docstring = None    
    
    def check_sections(self, node):
        """
        This function checks if the docstring of a function has the required sections.
        
        Args:
          
          - node (ast): The node that is being checked.
        """
        #Get arguments into the function
        node_args = node.args.args
        is_args_section = None
        is_return_section = None
        
        #If there are arguments...
        if len(node_args) > 0:
            arguments = [argument.arg for argument in node_args]
            if arguments[0] != "self":
                #Check if Args section exist
                is_args_section = self._check_section(section = 'Args:')
                if not is_args_section:
                    violation = Violation(
                        node =  node,
                        message = 'The "arguments" section in the docstrings must have an "Args:" title.'
                    )
                    self.violations.add(violation)
                
        
        #Check if the function returns something
        if isinstance(node.body[-1], ast.Return):
            #Check if Returns section exist
            is_return_section = self._check_section(section = 'Returns:')
            if not is_return_section:
                violation = Violation(
                    node =  node,
                    message = 'The "return" section in the docstrings must have a "Returns:" title.'
                )
                self.violations.add(violation)
    
    def visit_FunctionDef(self, node):
        """
        It checks the docstring of a function and checks if it is in the google format.
        
        Args:
          
          - node (ast): The node that is being visited.
        """
        self.docstring = get_docstrings(node)
        self.check_sections(node)
        super().generic_visit(node)
    
    
class UpToDateArgumentsChecker(Checker, GoogleAuxiliar):
    """DOCS-002: outdated documentation"""
    def __init__(self, issue_code):
        super().__init__(issue_code)
        self.docstring = None

    def _check_arguments(self, node, docstrings):
        """
        It checks if the arguments in the function are found in the docstrings.
        
        Args:
          
          - node (ast): The node that is being checked.
          - docstrings (str): The docstrings of the function.
        """
        node_args = node.args.args
        args_list = re.findall('^(.*?:)', docstrings, re.MULTILINE)
        
        if len(node_args) > 0:
            for argument in node_args:
                exist_argument = sum((1 for substring in args_list if argument.arg in substring)) > 0
                
                if not exist_argument and "self" not in argument.arg:
                    violation = Violation(
                        node= node,
                        message=f'The argument called "{argument.arg}" is not found in the docstrings.'
                    )
                    self.violations.add(violation)
    
    def check_arguments(self, node):
        """
        The function checks if the documentation about the arguments is up to date.
        
        Args:
          
          - node (ast): the node of the function
        """
        is_args_section = self._check_section(section = "Args:")
        is_return_section = self._check_section(section = "Returns:")

        if is_args_section:            
            args_section = self._get_args_section(is_return_section = is_return_section)
                                    
            #Check if the documentation about the arguments is up to date
            self._check_arguments(node, args_section)
    
    def visit_FunctionDef(self, node):
        """
        It checks the docstring of a function and checks if it is in the google format.
        
        Args:
          
          - node (ast): The node that is being visited.
        """
        self.docstring = get_docstrings(node)
        self.check_arguments(node)
        super().generic_visit(node)

class ContentChecker(Checker, GoogleAuxiliar):
    """DOCS-003: inappropiate documentation"""

    def __init__(self, issue_code=None):
        super().__init__(issue_code)
        self.docstring = None
    
    def check_content(self, node):
        """
        This function checks if the docstrings have a good content.
        
        Args:
          
            - node (ast): the node that is being checked
        """
        #Get arguments into the function
        is_args_section = self._check_section(section = "Args:")
        is_return_section = self._check_section(section = "Returns:")
        sections = {}
        
        if is_args_section:            
            sections['args'] = self._get_args_section(is_return_section)
            sections ['description'] = self._get_description_section()
                    
        if is_return_section:
            sections ['returns'] = self._get_return_section()
        
        #Check content of the sections (description, args, return)
        for section, content in sections.items():
            
            #Check amount of words in the section and bad words            
            is_enough_values = at_least_n_words(text = content, min_words = 3)
            is_bad_words = check_bad_words_score(content, 0.1)
            
            if not is_enough_values or is_bad_words:
                violation = Violation(
                    node =  node,
                    message = f'The docstrings must be more specific in the "{section}" section.'
                )
                self.violations.add(violation)
                   
    def visit_FunctionDef(self, node):
        """
        It checks the docstring of a function and checks if it is in the google format.
        
        Args:
          
          - node (ast): The node that is being visited.
        """
        self.docstring = get_docstrings(node)
        self.check_content(node)
        super().generic_visit(node)
