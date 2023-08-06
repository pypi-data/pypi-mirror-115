#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import random as r

from substitutionstring.substitution import Substitution
from substitutionstring.substitution_string import SubstitutionString
from substitutionstring import compression_tools as compress

string = "abcdefghijklmnopqrstuvwxyz     0123456789"

def generate_long_sequence(N):
    initial_string = ''.join(r.choices(string,k=550))
    sstring = SubstitutionString(initial_string)
    for _ in range(N):
        start, end = r.randrange(0,len(sstring.string)), r.randrange(0,len(sstring.string))
        string_ = ''.join(r.choices(string,k=start))
        if end <= start: 
            start, end = end, start
        sstring.substitute(start,end,string_)
    return sstring, initial_string

class test_Compression(ut.TestCase):
    
    def test_displace_substitution(self,):
        N=25
        sstring,initial_string = generate_long_sequence(N)
        sequence = list(reversed(sstring))
        
        combinaisons = [(i,j) for j in range(N) for i in range(N) if i<j]
        
        for comb in combinaisons:
            with self.subTest(line=comb):
                sequence_ = compress.displace_substitution_in_sequence(sequence, comb[0], comb[1])
                test_string = initial_string
                for subst in sequence_:
                    test_string = subst.apply(test_string)
                self.assertTrue(test_string==sstring.string)
    
        combinaisons = [(i,j) for j in range(N) for i in range(N) if i>j]
        
        for comb in combinaisons:
            with self.subTest(line=comb):
                sequence_ = compress.displace_substitution_in_sequence(sequence, comb[0], comb[1])
                test_string = initial_string
                for subst in sequence_:
                    test_string = subst.apply(test_string)
                self.assertTrue(test_string==sstring.string)
        
        return None
    
    def test_minimal_sequence(self,):
        N=50
        sstring,initial_string = generate_long_sequence(N)
        sequence = list(reversed(sstring))
        
        min_sequence = compress.compress_sequence(sequence)
        
        test_string = initial_string
        for subst in min_sequence:
            test_string = subst.apply(test_string)
        self.assertTrue(test_string==sstring.string)
        return None
