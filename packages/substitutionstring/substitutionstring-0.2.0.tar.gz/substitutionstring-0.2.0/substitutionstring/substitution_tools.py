#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Some methods that manipulate Substitution objects. These methods are all implemented (with quite similar names) as methods of the Substitution object. See its documentation for more details.
"""

from .substitution import Substitution

def substitute_and_revert(string, start, end, substitution_string):
    """Substitute the substitution_string in the string from position start to position end. That is, the resulting string will be string[:start]+substitution_string+string[end:]. In the same time, one constructs the Substitution object that can be fed to `apply_substitution` in order to revert the substitution."""
    if start > len(string): start = len(string)
    if end > len(string): end = start
    substitution = Substitution(start = start,
                                end = start+len(substitution_string),
                                string = string[start:end])
    new_string = string[:start] + substitution_string + string[end:]
    return new_string, substitution

def apply_substitution(string, substitution):
    """Apply the process of a substitution (being a Substitution instance), by injecting a Substitution instance along a string."""
    new_string, new_substitution = substitute_and_revert(string, 
                                                         substitution.start,
                                                         substitution.end,
                                                         substitution.string)
    return new_string, new_substitution

def apply_substitution_string(string, substitution):
    """Apply the substitution (being a Substitution instance), and returns the substituted string."""
    new_string = string[:substitution.start] + substitution.string \
        + string[substitution.end:]
    return new_string

def shift_start_end(start, end, substitution):
    """Find the new position start and end (seen as the index of string) once substitution is applied."""
    if substitution.end <= start:
        start += abs(substitution)
    elif substitution.start <= start <= substitution.end:
        start = substitution.start
    if substitution.end <= end:
        end += abs(substitution)
    elif substitution.start < end <= substitution.end:
        end = substitution.start + len(substitution)  
    return start, end



