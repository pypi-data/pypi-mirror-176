import sys
from typing import Sequence

try:
  from base_linter import Linter
  from google_checks import SectionChecker, UpToDateArgumentsChecker, ContentChecker
except ModuleNotFoundError:
  from morgan_linter.base_linter import Linter
  from morgan_linter.google_checks import SectionChecker, UpToDateArgumentsChecker, ContentChecker

def cli(argv: Sequence[str] = sys.argv, is_testing=False):
    """
    It takes a list of paths to source files, and runs
    the linter on each of the source files.
    
    Args:
      
      - argv (Sequence[str]): Sequence[str] = sys.argv
      - is_testing (Bool): True if you want to test the library
    """
    source_paths = argv[1:]
    linter = Linter()
    linter.checkers.add(SectionChecker(issue_code = "DOCS-001"))
    linter.checkers.add(UpToDateArgumentsChecker(issue_code = "DOCS-002"))
    linter.checkers.add(ContentChecker(issue_code = "DOCS-003"))
    
    for source_path in source_paths:
      linter.run(source_path, is_testing)

    if not is_testing:    
      linter.calculate_results()

if __name__ == "__main__":
    cli()
    
