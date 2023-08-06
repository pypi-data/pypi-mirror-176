"""
This module contains auxiliar functions.
"""
import ast
import os
from typing import NamedTuple

def get_docstrings(node):
    """
    It takes a node and returns the docstring of the function.
    
    Args:
      
      - node (ast): The node to get the docstring for
    
    Returns:

      The docstring of the function
    """
    #Get the function metadata
    function_metadata = [_function for _function in ast.walk(node)]

    #Get docstrings
    function_docs = ast.get_docstring(function_metadata[0])
    
    return function_docs

def jaccard_similarity(x, y):
    """
    It takes two lists and returns the Jaccard similarity between them.
    
    Args:
      
      - x (list): list 1
      - y (list): the list of labels (ground truth)
    
    Returns:
      
      The jaccard similarity between two sets
    """
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))

    return intersection_cardinality / float(union_cardinality)

def at_least_n_words(text: str, min_words: int):
    """
    If the number of words in the text is less than the minimum number of words, return False,
    otherwise return True.
    
    Args:
      
      - text (str): the text to be checked
      - min_words (int): The minimum number of words that the text must have
    
    Returns:

      A boolean value.
    """
    text_splitted = text.split(" ")
    if len(text_splitted) < min_words:
        return False
    return True

def check_bad_words_score(text: str, threshold: float):
    """
    It takes a text and a threshold as input, and returns True if the text contains any of the bad words
    in the list, and False otherwise.
    
    Args:

      - text (str): the text to be checked
      - threshold (float): the minimum score for a text to be considered as a bad text
    
    Returns:

      A boolean value.
    """
    bad_words_list = ["__summary__", "__description__"]
    bad_words_processed = [sentence.lower().split(" ") for sentence in bad_words_list]
    text_list = text.lower().split(" ")
    text_list = [txt.replace("\n", "") for txt in text_list]
    
    for words_list in bad_words_processed:            
        score = jaccard_similarity(words_list, text_list)
        if score >= threshold:
            return True
    
    return False