#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
`SubstitutionString` class allows modifying a string mainly using REGular EXpressions.
The main feature of this class is the possibility to revert the modifications
operations, or to restore the original text.

Since neither `Substitution` not `SubstitutionSequence` has a clear meaning without the application to a explicit string, one constructs the `SubstitutionString` as the association of `Substitution` and a string, in order to deal with explicit manipulation of a string.
"""

import re
from typing import List, Iterator, Union, Tuple

from .substitution import Substitution
from .substitution_sequence import SubstitutionSequence

class SubstitutionString():
    
    """
`SubstitutionString` class allows complete manipulation of a string in term of insertion, deletion, substitution, eventually via REGEX. This object is constructed on top of a string and a `SubstitutionSequence` (that can be thought as a list of `Substitution` instances).
        
    """
    
    def __init__(self,string: str=str(),
                 sequence: List[Substitution]=list()) -> None:
        """
Instantiate the attributes `string` (a string) and `sequence` (a list of `Substitution`). Both might be empty.

Parameters | Type | Details
-- | -- | --
`string` | string | The initial state of the string that will be modified later on.
`sequence` | list of `Substitution`, or a `SubstitutionSequence` object | The inverse of the `Substitution` that has been applied to the `string` up to now. Basic usage is to let this attribute empty.
        """
        self.string = str(string)
        self.sequence = SubstitutionSequence(sequence)
        return None
    
    def __repr__(self,) -> str:
        """Represent the instance with the number of `Substitution` inside"""
        return 'SubstitutionString({} Substitution.s)'.format(len(self))
    
    def __len__(self,) -> int:
        """Give the number of `Substitution` present in the sequence"""
        return len(self.sequence)
    
    def __getitem__(self, n: Union[int, slice]) -> Union[Substitution, 
                                                         SubstitutionSequence]:
        """Give item `n` of the attribute `SubstitutionString.sequence`. 
        
Returns  | depending on type | Details
-- | -- | --
`n` | integer | The `Substitution` item of the `SubstitutionString.sequence`
`n` | slice | The `SubstitutionSequence` that is part of the `SubstitutionString.sequence`
        """
        return self.sequence[n]
    
    def __str__(self,) -> str:
        """Give `self.string`, the actual state of the `SubstitutionString`."""
        return self.string
    
    def __reversed__(self,) -> Iterator[Substitution]:
        """
Reverses the sequence, such that one can apply the transformations to an other string if one wishes. Returns a generator of `Substitution`, with all the `Substitution` that has been performed to the initial string state.

Example: 
```python
string = "01234567891123456789"
sstring = SubstitutionString(string=string)
sstring.substitute(3,7,'abcde')
sstring.substitute(9,12,'AB')
sstring.string # returns '012abcde7AB123456789'

for subst in sstring:
    print(subst)
# returns the inverse Substitution
# Substitution(start=3, end=8, string=`3456`)
# Substitution(start=9, end=11, string=`891`)

for subst in reversed(sstring):
    print(subst)
# returns the original Substitution
# Substitution(start=3, end=7, string=`abcde`)
# Substitution(start=9, end=12, string=`AB`)
```

Note the application of `insert`, `delete`, `substitution` or `sub` appends the inverse `Substitution` to the `SubstitutionString.sequence`, whereas `reversed(SubstitutionString)` presents the original `Substitution` in their temporal order. Be warn that the nomenclature might be a bit confusing.
        """
        string = self.string
        reversed_sequence = list()
        for substitution in reversed(self.sequence):
            string, subst = substitution.apply_and_revert(string)
            reversed_sequence.append(subst)
        return reversed(reversed_sequence)
    
    @property
    def original_sequence(self,) -> SubstitutionSequence:
        """Since the `SubstitutionString.sequence` is constructed using inverse `Substitution`, the attribute `SubstitutionString.original_sequence` will return the `SubstitutionSequence` of all the `Substitution` performed to the initial state of `SubstitutionString`."""
        return SubstitutionSequence(list(reversed(self)))
    
    def __call__(self, string: str) -> str:
        """Apply the same substitutions as the actual string to an other string given as parameter. This method is quite useless !"""
        for substitution in reversed(self):
            string = substitution.apply(string)
        return string
    
    def apply_substitution(self, substitution: Substitution) -> str:
        """Apply the `Substitution` object to the actual string. Append the inverse `Substitution` to the sequence. Returns the `SubstitutionString.string` once the `Substitution` has been applied."""
        self.string, subst = substitution.apply_and_revert(self.string)
        # identical substitution: self.string is unchanged
        if not subst == substitution: 
            self.sequence.append(subst)
        return self.string
    
    def substitute(self, start: int, end: int, string: str) -> str:
        """
Substitute `string` to `self.string[start:end]`.

Parameters | Type | Details
-- | -- | --
`start` | int | The initial position of `SubstitutionString.string` that will be deleted.
`end` | int | The final position of `SubstitutionString.string` that will be deleted.
`string` | string | The string that will be inserted at the place of `SubstitutionString.string[start:end]`.

The method then appends the inverse `Substitution` to the `SubstitutionString.sequence`, and returns the final state of the string `SubstitutionString.string`, once `Substitution` is applied.
        """
        return self.apply_substitution(Substitution(start,end,string))
    
    def insert(self, position: int, string: str) -> str:
        """
Insert `string` at `self.string[start]`.

Parameters | Type | Details
-- | -- | --
`start` | int | The position of `SubstitutionString.string` where the insertion will take place.
`string` | string | The string that will be inserted at the place of `SubstitutionString.string[start:end]`.

The method then appends the inverse `Substitution` to the `SubstitutionString.sequence`, and returns the final state of the string `SubstitutionString.string`, once `Substitution` is applied.
        """
        return self.substitute(position,position,string)
    
    def delete(self, start: int, end: int) -> str:
        """
Delete `self.string[start:end]`.


Parameters | Type | Details
-- | -- | --
`start` | int | The initial position of `SubstitutionString.string` that will be deleted.
`end` | int | The final position of `SubstitutionString.string` that will be deleted.

The method then appends the inverse `Substitution` to the `SubstitutionString.sequence`, and returns the final state of the string `SubstitutionString.string`, once `Substitution` is applied.
        """
        return self.substitute(start,end,str())
    
    def apply_sequence(self, 
                       sequence: Union[SubstitutionSequence, 
                                       List[Substitution]]) -> str:
        """Apply the list of `Substitution` given as `sequence` to the actual state of `SubstitutionString.string`. Then append the inverse `Substitution` to the `SubstitutionString.sequence`. Be warn there is no verification of the `sequence` object before susbtitution."""
        for substitution in sequence:
            self.string = self.apply_substitution(substitution)
        return self.string
    
    def sort_sequence(self,) -> SubstitutionSequence:
        """
Sort the `SubstitutionString.sequence`. Returns a new `SubstitutionSequence that can be applied to the initial state of the `SubstitutionString` to come back to the final state of the `SubstitutionString`. Usually the returned `SubstitutionSequence` is shorter than the actual one. In addition, the `Substitution` in the `SubstitutionSequence` are sorted by their `start` attributes (hence the name of the method).

This is an heuristic method to compress the `SubstitutionSequence`.

Example:
```python
string = "01234567891123456789"
sstring = SubstitutionString(string=string)
sstring.substitute(8,9,'AB')
sstring.substitute(3,8,'abcde')
sstring.string # returns '012abcdeAB91123456789'
sorted_sequence = sstring.sort_sequence()

# initial sequence of Substitution (in original order):
for subst in reversed(sstring):
    print(subst)
# returns
# Substitution(start=8, end=9, string=`AB`)
# Substitution(start=3, end=8, string=`abcde`)

# sorted sequence of Substitution (in original order):
for subst in sorted_sequence:
    print(subst)
# returns 
# Substitution(start=3, end=9, string=`abcdeAB`)

# comparison of the strings
original_sequence = sstring.original_sequence
original_sequence.apply(string) == sorted_sequence.apply(string)
# returns True

```
        """
        return SubstitutionSequence(list(reversed(self))).sort()
    
    def sub(self, regex: str, string: str, flags: str=0) -> str:
        """
Apply the `re.sub(regex,string)` method to self.string, for all REGEX matching expression. Constructs the inverse `Substitution` objects for each substitution, and append them to the `SubstitutionString.sequence`. Returns the modified string, once all substitutions have been done.

Parameters | Type | Details
-- | -- | --
`regex` | REGEX in string | REGular EXpression, see https://docs.python.org/3/library/re.html for more details and introduction. The matched expression will be replaced by the parameter `string`.
`string` | string | A string that will replace the REGular EXpression in `regex`.
`flags` | re module flag | A list of flags that must be `re`-module objects, and eventually concatenated using the OR operator `|`. For instance `re.DOTALL|re.IGNORECASE` will treat lower and upper case letter in the same way, and make the character `.` to match any character. See https://docs.python.org/3/library/re.html for more details. By default, there is no flag (or `flags=0`)
        """
        k = 0
        for r in re.finditer(regex,self.string,flags):
            start, end = r.start(), r.end()
            self.string = self.substitute(start+k,end+k,string)
            k += len(string) + start - end
        return self.string
    
    def revert(self, times: int=1) -> str:
        """
Revert the last `times` times or steps of the `SubstitutionString.sequence`. To completely revert to the original string, ask for `SubstitutionString.revert(len(SubstitutionString))`. `SubstitutionString.revert` is an irreversible process: it changes the `SubstitutionString.sequence`.

Example:
```python
string = "01234567891123456789"
sstring = SubstitutionString(string=string)
sstring.substitute(8,9,'AB')
sstring.substitute(3,8,'abcde')
sstring.string # returns '012abcdeAB91123456789'

# initial sequence of Substitution (in original order):
for subst in reversed(sstring):
    print(subst)
# returns
# Substitution(start=8, end=9, string=`AB`)
# Substitution(start=3, end=8, string=`abcde`)

sstring.revert() # returns '01234567AB91123456789'
# after revert, one Substitution is missing
for subst in reversed(sstring):
    print(subst)
# returns
# Substitution(start=8, end=9, string=`AB`)

# applying again revert pull back the string to its initial state
sstring.revert() == string # returns True
```
        """
        for t in range(int(times)):
            try:
                substitution = self.sequence.pop(-1)
            except IndexError:
                mess = "Warning: No more modifications done"
                substitution = Substitution()
                print(mess)
            self.string = substitution.apply(self.string)
        return self.string
    
    def restore(self, start: int, end: int) -> Tuple[str,int,int]:
        """
Restore the initial string from position `start` to `end`. Positions are taken from the actual `SubstitutionString.string` attribute. Returns `string`, `start`, `end`, the initial string, and the positions `start` and `end` in the initial string.

Example: 
```python
string = "01234567891123456789"
sstring = SubstitutionString(string=string)
sstring.substitute(8,9,'AB')
sstring.substitute(3,8,'abcde')

string, start, end = sstring.restore(3,6)
string[start:end] # returns '34567'
```
        """
        start, end = int(start), int(end)
        if start > len(self.string): start = len(self.string)
        if end < start: end = start
        if end > len(self.string): end = len(self.string)
        string = self.string
        for substitution in reversed(self.sequence):
            start, end = substitution.shift_start_end(start, end)
            string = substitution.apply(string)
            end = min(end, len(string))        
        return string, start, end

