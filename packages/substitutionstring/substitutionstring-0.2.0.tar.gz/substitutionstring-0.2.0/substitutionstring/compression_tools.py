#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tools and algorithms that allows the compression of a sequence of Substitution objects.

All these methods are reported to the object SubstitutionSequence

"""

from .substitution import Substitution

def permute_non_overlapping(substitution1, substitution2):
    """Permute two Substitution objects when they do not overlap. substitution1 and substitution2 must be in a sequence in that order, that is, substitution1 must be applied before substitution2 is performed. Then this function will flip these two substitutions in a sequence. Raises a ValueError in case the two substitutions overlap, in which case they should not be permuted, but might be combined."""
    if substitution1.start + len(substitution1) < substitution2.start:
        start1 = substitution2.start - abs(substitution1)
        end1 = substitution2.end - abs(substitution1)
        start2 = substitution1.start
        end2 = substitution1.end
    # substitution2 applied before substitution1 is not possible
    elif substitution1.start > substitution2.end:
        start1 = substitution2.start
        end1 = substitution2.end
        start2 = substitution1.start + abs(substitution2)
        end2 = substitution1.end + abs(substitution2)
    else:
        mess = "Unfaithfull permutation: overlapping Substitution objects"
        # mess += ": got\n{} and\n{}".format(substitution1,substitution2)
        raise ValueError(mess)
    substitution1_ = Substitution(start=start1, end=end1,
                                  string=substitution2.string)
    substitution2_ = Substitution(start=start2, end=end2,
                                  string=substitution1.string)
    return substitution1_, substitution2_

def combine_overlapping(substitution1, substitution2):
    """Combine overlapping Substitution objects in a single Substitution object. The two Substitution objects substitution1 and substitution2 (the parameters) must be applied in that order, that is, substitution1 is applied (see apply_substitution function above) before substitutio2 is peformed. Returns a single Substitution object. Raises a ValueError in case the two Substitution objects are not overlapping."""
    # S1: substitution1
    # S2: substitution2
    start1 = substitution1.start
    # S1 is always applied before S2
    end1 = substitution1.start + len(substitution1)
    start2 = substitution2.start
    end2 = substitution2.end
    if start2 < start1:
        if end1 < end2: # complete overlapping: S2 over S1
            start = start2
            end = end2 - abs(substitution1)
            string = substitution2.string
        elif start1 <= end2 <= end1: # partial overlapping: S2 left to S1
            start = start2
            end = end1 - abs(substitution1) # this is substitution1.end
            string = substitution2.string+substitution1.string[end2-start1:]
        else:
            mess = "Impossible combination: non-overlapping Substitution objects"
            # mess += ": got\n{} and\n{}".format(substitution1,substitution2)
            raise ValueError(mess)
    elif start1 <= start2: 
        if end2 < end1: # complete overlapping: S2 completely inside S1
            start = start1
            end = end1 - abs(substitution1) # this is substitution1.end
            string = substitution1.string[:start2-start1]+substitution2.string\
                + substitution1.string[end2-start1:]
        elif start2 <= end1 <= end2: # partial overlapping: S2 right to S1
            start = start1
            end = end2 - abs(substitution1)
            string = substitution1.string[:start2-start1]+substitution2.string
        else:
            mess = "Imposible combination: non-overlapping Substitution objects"
            # mess += ": got\n{} and\n{}".format(substitution1,substitution2)
            raise ValueError(mess)
    return Substitution(start=start, end=end, string=string)

def displace_substitution_in_sequence(sequence, start, end):
    """Displace the Substitution object from positio start in the sequence to the position end in the sequence. If in the way one can combine two substitutions, one does this combination"""
    bools = [start<0, end>len(sequence)-1, start>len(sequence)-1, end<0]
    if any(bools):
        mess = "start and end must be compatible with the sequence:"
        mess += "got start={}, end={} for a sequence".format(start, end)
        mess += " of length {}".format(len(sequence))
        raise IndexError(mess)
    direction = +1 if end >= start else -1
    i = start
    while i != end:
        p1,p2 = (sequence[i],sequence[i+1]) if direction>0 \
            else (sequence[i-1],sequence[i])
        try:
            substitution = [combine_overlapping(p1, p2),]
            end -= direction if abs(end-i)>1 else 0
        except ValueError:
            s1, s2 = permute_non_overlapping(p1, p2)
            substitution = [s1, s2]
        shift = (direction-1)//2
        sequence = sequence[:i+shift] + substitution + sequence[i+shift+2:]
        i += direction
    return sequence

def select_minimal_displacement(sequence,already_displaced=list()):
    """From a sequence, try all the combinations of displacements of Substitution objects, and returns the best displacement, that is, the displacement that produces the minimum memory size that the Substitution objects inside the sequence would represent. 

    To allow (artificially) memory to the Substitution objects we suppose that each character of the string is encoded in one digit, and each integer (start and end attributes) are also encoded in one digit. So we count the number of digits of each Substitution object, and we optimize locally the best displacement (with combination in case there is overlapping among different Substitution objects) while doing this displacement.
    
    Parameters :
        - sequence: a list of Substitution objects
        - already_displaced: a list of tuples that one would prefer to remove from the combinations of displacements that this method generates during the computation. Recall that a displacement (see displace_substitution_in_sequence) consists in displacing the Substitution at the start position in the sequence to the end position inside the sequence.
    
    Returns : 
        a tuple of integers that consists in 
        - the minimal size of cumulated strings that the sequence would produce
        - the start position of the Substitution object in the sequence
        - the end position of the Substitution object in the sequence
    """
    # generate all combinations of displacement inside the sequence
    combinations = [(i,j) 
                    for i in range(len(sequence)) 
                    for j in range(len(sequence))
                    if i!=j and (i,j) not in already_displaced]
    combinations.append((0,0))
    # calculate the associated size of the total string that should be stored
    # in case this sequence is selected, plus 2 digits for the two integers
    # (this allows to reduce the number of Substitution objects in case
    # the strings have same length)
    sizes = [sum(len(subst)+2 for subst 
                 in displace_substitution_in_sequence(sequence,start,end))
             for start,end in combinations]
    # find the minimal size of total stored string
    min_ = min(zip(sizes,range(len(sizes))), key=lambda x:x[0])
    return min_[0], combinations[min_[1]][0], combinations[min_[1]][1]

def compress_sequence(sequence):
    """Compress the sequence so that the resulting one will have less Substitution objects inside, and the associated strings will be smaller than the actual ones."""
    size = sum(len(subst)+2 for subst in sequence)
    size_min, start, end = select_minimal_displacement(sequence)
    sequence = displace_substitution_in_sequence(sequence, start, end)
    while size_min < size and len(sequence) > 1:
        size = size_min
        size_min, start, end = select_minimal_displacement(sequence)
        sequence = displace_substitution_in_sequence(sequence, start, end)
    return sequence