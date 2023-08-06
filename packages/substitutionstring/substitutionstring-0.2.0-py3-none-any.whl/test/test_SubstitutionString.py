#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test of the class SubstitutionString
"""

import unittest as ut

from substitutionstring.substitution import Substitution
from substitutionstring.substitution_string import SubstitutionString, SubstitutionSequence

class TestSubstitutionString(ut.TestCase):
    
    def test_init(self,):
        """Test the initialization of SubstitutionString, and its basic attributes."""
        string = "01234567891123456789"
        sstring = SubstitutionString(string=string)
        self.assertTrue(sstring.string==string)
        self.assertTrue(sstring.sequence==SubstitutionSequence())
        sstring.substitute(3,7,'abcde')
        self.assertTrue(sstring.string=='012abcde7891123456789')
        subst = Substitution(start=3, end=8, string='3456')
        self.assertTrue(sstring.sequence[-1]==subst)
        self.assertTrue(len(sstring)==1)
        return None
    
    def test_init_SubstitutionSequence(self,):
        "Check that one can initialize SubstitutionString with a SubstitutionSequence or alist of Substitution"
        string = "01234567891123456789"
        sequence = [Substitution(2,5,'test'),Substitution(8,12,'TEST')]
        sstring = SubstitutionString(string=string, sequence=sequence)
        self.assertTrue(sstring.string==string)
        self.assertTrue(sstring.sequence==SubstitutionSequence(sequence))
        subst_sequence = SubstitutionSequence(sequence)
        sstring = SubstitutionString(string=string, sequence=subst_sequence)
        self.assertTrue(sstring.string==string)
        self.assertTrue(sstring.sequence==subst_sequence)
        return None        
        
    def test_restore(self,):
        """Test the SubstitutionString.restore method"""
        string = "01234567891123456789"
        sstring = SubstitutionString(string=string)
        sstring.substitute(3,7,'abcde')
        r0 = sstring.restore(2,4)
        string_test = r0[0][r0[1]:r0[2]]
        self.assertTrue(string_test==string[2:7])
        r1 = sstring.restore(2,5)
        self.assertTrue(r0==r1)
        r2 = sstring.restore(2,7)
        self.assertTrue(r0==r2)
        r3 = sstring.restore(2,8)
        self.assertTrue(r0==r3)
        r4 = sstring.restore(2,9)
        string_test = r4[0][r4[1]:r4[2]]
        self.assertTrue(string_test==string[2:8])
        r5 = sstring.restore(8,10)
        string_test = r5[0][r5[1]:r5[2]]
        self.assertTrue(string_test==sstring.string[8:10])
        return None     
    
    def test_substitute(self,):
        string = "01234567891123456789"
        sstring = SubstitutionString(string=string)
        s1 = sstring.substitute(3,7,'abcde')
        subs = sstring.sequence[-1]
        self.assertTrue(subs.start==3)
        self.assertTrue(subs.end==8)
        self.assertTrue(subs.string=='3456')
        s2 = sstring.substitute(9,12,'AB')
        subs = sstring.sequence[-1]
        self.assertTrue(subs.start==9)
        self.assertTrue(subs.end==11)
        self.assertTrue(subs.string=='891')
        s3 = sstring.substitute(subs.start,subs.end,subs.string)
        self.assertTrue(s3==s1)
        self.assertTrue(len(sstring)==3)
        subs = sstring.sequence[0]
        s4 = sstring.substitute(subs.start,subs.end,subs.string)
        self.assertTrue(s4==string)
        self.assertTrue(len(sstring)==4)        
        return None
    
    def test_sub_and_sort(self,):
        string = "01234567891123456789"
        sstring = SubstitutionString(string=string)
        sstring.sub('1','a')
        self.assertTrue(len(sstring)==3)
        self.assertTrue(sstring.string=='0a23456789aa23456789')
        sstring.sub('9','b')
        self.assertTrue(len(sstring)==5)
        self.assertTrue(sstring.string=='0a2345678baa2345678b')
        sequence = list(reversed(sstring))
        string_test = SubstitutionString(string=string).apply_sequence(sequence)
        self.assertTrue(string_test==sstring.string)
        sequence = sstring.sort_sequence()
        self.assertTrue(len(sequence)==len(sstring.sequence)-2)
        string_test = SubstitutionString(string=string).apply_sequence(sequence)
        self.assertTrue(string_test==sstring.string)
        return None        
    
    def test_reversed(self,):
        string = "01234567891123456789"
        sstring = SubstitutionString(string=string)
        s1 = sstring.substitute(3,7,'abcde')
        s2 = sstring.substitute(9,12,'AB')
        reversed_sequence = list(reversed(sstring))
        s3 = SubstitutionString(string=string).apply_sequence(reversed_sequence)
        self.assertTrue(s3==s2)
        return None