#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

While two `Substitution` objects do not commute in general, it is possible to manipulate several `Substitution` when they are supposed to apply in a sequence.
"""
from typing import TypeVar, Type, List, Iterator, Union, Tuple

from .substitution import Substitution
SS = TypeVar('SubstitutionSequence', bound='SubstitutionSequence')

class SubstitutionSequence():

    """
`SubstitutionSequence` is a class that consists in a sequence of `Substitution` objects, and handles some basic manipulation of these `Substitution` inside the full sequence. 

For instance, `SubstitutionSequence` is able to combine several `Substitution` objects, provided they overlap among each other (vie the `displace(start,stop)` method). In addition, it has some properties of a sequence, like the possibility to concatenate several `SubstitutionSequence` into a bigger one (append, extend and + methods).
    """
    
    def __init__(self,sequence: List[Substitution]=list()):
        """Take as entry a list of `Substitution` objects."""
        self.sequence = []
        for substitution in sequence:
            self.__check_substitution(substitution)
            self.sequence.append(substitution)
        return None
    
    def __repr__(self,) -> str:
        """Display the number of `Substitution` objects present into the `SubstitutionSequence`."""
        mess = "SubstitutionSequence({} Substitutions)".format(len(self))
        return mess
    
    def __reversed__(self,) -> Iterator[Substitution]:
        """Generate the `Substitution` inside the `SubstitutionSequence`, in the reverse order."""
        for substitution in self.sequence[::-1]:
            yield substitution
        return None
    
    def __eq__(self, sequence: Type[SS]):
        """Returns True if all `Substitution` in the given sequence are the same as in this one. Otherwise returns False."""
        bools = [subst0==subst1 for subst0,subst1 in zip(self,sequence)]
        bools.append(len(sequence)==len(self))
        return all(bools)
    
    def __check_substitution(self, substitution):
        """Raises a TypeError in case the object that one pass to this method is not a valid `Substitution` object."""
        bools = [hasattr(substitution,'start'),
                 hasattr(substitution,'end'),
                 hasattr(substitution,'string')]
        if not all(bools):
            mess = "SubstitutionSquence must contain only Substitution objects"
            raise TypeError(mess)
        return None
    
    def __len__(self,):
        """Returns the number of `Substitution` contained inside the `SubstitutionSequence`."""
        return len(self.sequence)
    
    def __getitem__(self,n: Union[int, slice]) -> Union[Type[SS],Substitution]:
        """Returns the element (a `Substitution`) or a slice (a `SubstitutionSequence`), like a list."""
        if isinstance(n,slice):
            return SubstitutionSequence(sequence=self.sequence[n])
        # in case n is an integer, return a Substitution which is not iterable
        elif isinstance(n,int): 
            return self.sequence[n]
        return None
    
    def apply(self, string: str) -> str:
        """Apply the complete sequence of Substitution to the given string. Raises an IndexError in case one of the Substitution can not be applied to the string during the process. Returns a string with all Substitution performed."""
        for substitution in self.sequence:
            string = substitution.apply(string)
        return string
    
    def append(self, substitution: Substitution) -> None:
        """Append a Substitution to the actual `SubstitutionSequence`. Returns None. Raises a TypeError in case the object one tries to extend is not a correct Substitution."""
        self.__check_substitution(substitution)
        self.sequence.append(substitution)
        return None
    
    def extend(self, sequence: Type[SS]) -> None:
        """Extend the `SubstitutionSequence` by the new one, in place. Returns None. Raises a TypeError in case the object one tries to extend is not a correct `SubstitutionSequence`."""
        for substitution in sequence:
            self.sequence.append(substitution)
        return None
    
    def pop(self, n: int) -> None:
        """Extract the element n from the `SubstitutionSequence`, and erase it from the sequence"""
        return self.sequence.pop(n)
    
    def __add__(self, sequence: Type[SS]) -> Type[SS]:
        """Allows to concatenated several `SubstitutionSequence` into one bigger one. Returns a `SubstitutionSequence`."""
        new_sequence = SubstitutionSequence(self.sequence)
        new_sequence.extend(sequence)
        return new_sequence
    
    def are_overlapping(self,p: int,q: int) -> bool:
        """
If the `Substitution` at position `p` and position `q` overlap, returns True. Otherwise returns False.

Raises a ValueError in case `p` and `q` are not contiguous.
        """
        if abs(p-q)!=1:
            mess = "p and q must be contiguous indices"
            raise ValueError(mess)
        p,q = (p,q) if p<q else (q,p)
        return not(self[p] < self[q] or self[p] > self[q])

    def _permute_non_overlapping(self,p: int,q: int) -> Tuple[Substitution,Substitution]:
        """Permute two `Substitution` objects when they do not overlap. Raises an IndexError in case the two substitutions overlap, in which case they should not be permuted, but might be combined."""
        Sp, Sq = self[p], self[q]
        shift1 = bool(Sp<Sq)*abs(Sp)
        shift2 = bool(Sp>Sq)*abs(Sq)
        start1, end1 = Sq.start - shift1, Sq.end - shift1
        start2, end2 = Sp.start + shift2, Sp.end + shift2
        substitution1_ = Substitution(start=start1, end=end1, string=Sq.string)
        substitution2_ = Substitution(start=start2, end=end2, string=Sp.string)
        return substitution1_, substitution2_

    def _combine_overlapping(self,p: int,q: int) -> Substitution:
        """Combine overlapping `Substitution` objects in a single `Substitution` object. Returns a single `Substitution` object. Raises an IndexError in case the two `Substitution` objects are not overlapping."""
        Sp, Sq = self[p], self[q]
        # Sp is always applied before Sq
        # so only the attributes of Sp are changed
        start1, end1, string1 = Sp.start, Sp.start + len(Sp), Sp.string
        start2, end2, string2 = Sq.start, Sq.end, Sq.string
        start = min(start1, start2)
        end = max(end1, end2) - abs(Sp)
        string = string1[:max(start2-start1,0)] + string2 \
            + string1[min(end2-start1,len(Sp)):]
        return Substitution(start=start, end=end, string=string)
    
    def displace(self,start: int, end: int) -> Type[SS]:
        """Displace Substitution at position start in the `SubstitutionSequence` to position end in the `SubstitutionSequence`. While doing so, if two Substitution overlap, they will be combined. Returns a `SubstitutionSequence`"""
        bools = [start<0, end>len(self)-1, start>len(self)-1, end<0]
        if any(bools):
            mess = "start and end must be compatible with the `SubstitutionSequence`:"
            mess += "got start={}, end={} for a `SubstitutionSequence`".format(start, end)
            mess += " of length {}".format(len(self))
            raise IndexError(mess)
        direction = +1 if end >= start else -1
        # one needs [:i] + [i+2:] for direction>0
        # and [:i-1] + [i+1:] for direction<0 (see SubSeq = ... 
        # in the while loop)
        shift = (direction-1)//2
        i = start
        SubSeq = SubstitutionSequence(self.sequence)
        while i != end:
            p1,p2 = (i,i+1) if direction>0 else (i-1,i)
            if SubSeq.are_overlapping(p1,p2):
                subst_ = SubSeq._combine_overlapping(p1,p2)
                substitution = SubstitutionSequence([subst_,])
                # one Substitution of the sequence disapears
                end -= direction if abs(end-i)>1 else 0
            else:
                s1, s2 = SubSeq._permute_non_overlapping(p1,p2)
                substitution = SubstitutionSequence([s1,s2])
            SubSeq = SubSeq[:i+shift] + substitution + SubSeq[i+shift+2:]
            i += direction  
        return SubSeq
    
    def leftmost_index(self,) -> int:
        """Find the minimum of the sequence, that is, the Substitution that starts at the lowest start position. Returns its index in the `SubstitutionSequence`."""
        min_ = min(zip(self,range(len(self))), key=lambda x: x[0].start)
        return min_[1]
    
    def sort(self,) -> Type[SS]:
        """Try to order the `SubstitutionSequence` with left-most Substitution (defined as the one with the smallest start value) on the left, and in increasing order of the start value of the different Substitution inside the sequence. Due to permutation between non-overlapping Substitution, there might be some remaining element. Then the sort method applies recursively to avoid such situation. Returns an ordered `SubstitutionSequence`."""
        reordered_sequence = SubstitutionSequence()
        SubSeq = self
        while len(SubSeq):
            leftmost_index = SubSeq.leftmost_index()
            new_sequence = SubSeq.displace(leftmost_index, 0)
            reordered_sequence.append(new_sequence[0])
            SubSeq = new_sequence[1:]
        # in case it remains un-ordered Substitution
        unordered = [subst1.start > subst2.start 
                     for subst1, subst2 in zip(reordered_sequence[:-1],
                                               reordered_sequence[1:])]
        if any(unordered):
            return reordered_sequence.sort()
        # in case it remains two Substitutions with equal start value
        equal_starts = [(i,i+1) for i, subst1, subst2 
                        in zip(range(len(reordered_sequence)),
                               reordered_sequence[:-1],
                               reordered_sequence[1:])
                        if subst1.start == subst2.start]
        if equal_starts:
            p,q = equal_starts[-1]
            sequence = reordered_sequence.displace(p,q)
            return sequence.sort()
        # in case there are still overlapping Substitution
        overlapping = [(p,p+1) for p in range(len(reordered_sequence)-1)
                       if reordered_sequence.are_overlapping(p,p+1)]
        if overlapping:
            p,q = overlapping[-1]
            sequence = reordered_sequence.displace(p,q)
            return sequence.sort()
        return reordered_sequence
    
    def _remove_empty_on_string(self, string: str=str()) -> Type[SS]:
        """Apply the `SubstitutionSequence` to the given string, and if a `Substitution` equals its inverse, we drop this `Substitution` from the `SubstitutionSequence`. Recall that a `Substitution` equals its inverse when it does nothing. """
        temp_sequence = self
        new_sequence = SubstitutionSequence()
        sub_string = string
        for subst in temp_sequence:
            sub_string, subst_ = subst.apply_and_revert(sub_string)
            if not subst_ == subst:
                new_sequence.append(subst)     
        return new_sequence
        
    
    def remove_empty(self,string: str=str()) -> Type[SS]:
        """Remove empty Substitution inside the `SubstitutionSequence`. If a string is given, remove also the `Substitution` which are their own inverse. Return a new `SubstitutionSequence`. """
        new_sequence = SubstitutionSequence(subst for subst in self
                                            if not (subst.start==subst.end 
                                                    and not len(subst)))
        if string:
            new_sequence = new_sequence._remove_empty_on_string(string=string)
        return new_sequence
        