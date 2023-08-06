#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test of the Substitution class

"""

import unittest as ut
import random as r

from substitutionstring.substitution import Substitution
from substitutionstring.substitution_sequence import SubstitutionSequence

def generate_long_sequence(N):
    string = "abcdefghijklmnopqrstuvwxyz0123456789"
    initial_string = ''.join(r.choices(string,k=550))
    sub_string, sequence = initial_string, SubstitutionSequence()
    for _ in range(N):
        start, end = r.randrange(0,len(sub_string)), r.randrange(0,len(sub_string))
        string_ = ''.join(r.choices(string,k=start))
        if end <= start: 
            start, end = end, start
        substitution = Substitution(start,end,string_)
        sequence.append(substitution)
        sub_string = substitution.apply(sub_string)
    return sequence, initial_string

class TestSubstitutionSequence(ut.TestCase):
    
    def test_init_and_list_attributes(self,):
        s1 = Substitution(3,4,'test1')
        s2 = Substitution(5,6,'test2')
        ss = SubstitutionSequence([s1,s2])
        self.assertTrue(hasattr(ss,'sequence'))
        self.assertTrue(ss[0]==s1)
        self.assertTrue(ss[1]==s2)
        self.assertTrue(len(ss[:])==2)
        with self.assertRaises(TypeError):
            ss.append(3)
            ss.append('test')
        ss.append(s1)
        self.assertTrue(len(ss)==3)
        left_index = ss.leftmost_index()
        self.assertTrue(ss[left_index]==s1)
        self.assertTrue(s1 in ss)
        self.assertTrue(min(ss)==s1)
        self.assertTrue(max(ss)==s2) # only min is defined because max uses < as well
        return None
    
    def test_overlap(self,):
        s1 = Substitution(3,5,'test1')
        s2 = Substitution(4,6,'test2')
        ss = SubstitutionSequence([s1])
        ss.append(s2)
        self.assertTrue(ss.are_overlapping(0,1))
        self.assertTrue(ss.are_overlapping(1,0))
        ss.append(Substitution(20,25,'test4'))
        self.assertFalse(ss.are_overlapping(1,2))
        with self.assertRaises(ValueError):
            ss.are_overlapping(2,5)
        return None

    def test_displace(self,):
        string = '12345678911234567892123456789'
        s1 = Substitution(3,4,'test1')
        s2 = Substitution(5,6,'test2')
        s3 = Substitution(8,12,'test3')
        s4 = Substitution(14,16,'test4')
        ss = SubstitutionSequence([s1,s2,s3,s4])   
        string1 = ss.apply(string)
        new_ss = ss.displace(0,3)
        string2 = ss.apply(string)
        self.assertTrue(string1==string2)
        with self.assertRaises(IndexError):
            new_ss.displace(0,3)
        new_ss = new_ss.displace(0,len(new_ss)-1)
        string3 = new_ss.apply(string)
        self.assertTrue(string1==string3)
        return None
    
    def test_equivalence_sorted(self,):
        for N in range(15,25):
            with self.subTest(line=N):
                sequence, initial_string = generate_long_sequence(N)
                string1 = sequence.apply(initial_string)
                reordered_sequence = sequence.sort()
                string2 = reordered_sequence.apply(initial_string)
                self.assertTrue(string1==string2)
                # assert(string1==string2)
                for subst1,subst2 in zip(reordered_sequence[:-1],reordered_sequence[1:]):
                    with self.subTest(line=(subst1.start,subst2.start)):
                        self.assertFalse(subst1.start > subst2.start)
                        # assert(subst1.start < subst2.start)
                overlapping = [reordered_sequence.are_overlapping(p,p+1)
                               for p in range(len(reordered_sequence)-1)]
                self.assertFalse(any(overlapping))
        return None
        
