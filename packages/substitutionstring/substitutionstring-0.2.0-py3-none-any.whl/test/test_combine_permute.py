#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test of the compression_tools
"""

import unittest as ut

from substitutionstring.substitution import Substitution
from substitutionstring import compression_tools as compress
from substitutionstring import substitution_tools as subtools

class Permutations(ut.TestCase):
    
    def test_permute_non_overlapping(self,):
        
        string = "je suis un test de chaine de caractères\n0123456789112345678921234567893123456789"

        substitution1 = Substitution(start=3,end=7,string="étais")
        substitution2 = Substitution(start=20,end=26,string="test")

        st = string
        for s in [substitution1,substitution2]:
            st = s.apply(st)
        
        s12,s21 = compress.permute_non_overlapping(substitution1,substitution2)
        st_test = string
        for s in [s12,s21]:
            st_test = s.apply(st_test)
        self.assertTrue(st_test==st)
        
        st = string
        for s in [substitution2,substitution1]:
            st = s.apply(st)
        
        s12,s21 = compress.permute_non_overlapping(substitution2,substitution1)
        st_test = string
        for s in [s12,s21]:
            st_test = s.apply(st_test)
        self.assertTrue(st_test==st)
        return None
    
    def test_permute_overlapping(self,):
        
        substitution1 = Substitution(start=3,end=7,string="étais")
        substitution2 = Substitution(start=4,end=9,string="test")
        with self.assertRaises(ValueError):
            compress.permute_non_overlapping(substitution1,substitution2)
            compress.permute_non_overlapping(substitution2,substitution1)
        return None
    
    def test_permute_contiguous(self,):
        substitution1 = Substitution(start=3,end=7,string="étais")
        substitution2 = Substitution(start=8,end=12,string="test")
        with self.assertRaises(ValueError):
            compress.permute_non_overlapping(substitution1,substitution2)
            
        string = "je suis un test de chaine de caractères\n0123456789112345678921234567893123456789"
        st = string
        for s in [substitution2,substitution1]:
            st = s.apply(st)
        
        s12,s21 = compress.permute_non_overlapping(substitution2,substitution1)
        st_test = string
        for s in [s12,s21]:
            st_test = s.apply(st_test)
        self.assertTrue(st_test==st)
        return None
    
class Combine(ut.TestCase):
    
    def test_combine_partial_overlap(self,):
        string = "je suis un test de chaine de caractères\n0123456789112345678921234567893123456789"
        substitution1 = Substitution(19,25,'cas 21')
        substitution2 = Substitution(11,22,'nouveau cas')

        with self.assertRaises(ValueError):
            compress.permute_non_overlapping(substitution1,substitution2)
            compress.permute_non_overlapping(substitution2,substitution1)
        
        st = string
        for s in [substitution1,substitution2]:
            st = s.apply(st)

        s12 = compress.combine_overlapping(substitution1,substitution2)
        stest = s12.apply(string)
        self.assertTrue(stest==st)
        
        st = string
        for s in [substitution2,substitution1]:
            st = s.apply(st)
            
        s21 = compress.combine_overlapping(substitution2,substitution1)
        stest_ = s21.apply(string)
        self.assertTrue(stest_==st)
        return None

    def test_combine_partial_overlap_contiguous(self,):
        string = "0123456789112345678921234567893123"
        string += '\n'+string
        substitution1 = Substitution(7,12,'abc')
        substitution2 = Substitution(10,22,'ABCDEF')
        
        with self.assertRaises(ValueError):
            compress.permute_non_overlapping(substitution1,substitution2)
            compress.permute_non_overlapping(substitution2,substitution1)
        
        st = string
        for s in [substitution1,substitution2]:
            st = s.apply(st)

        s12 = compress.combine_overlapping(substitution1,substitution2)
        stest = s12.apply(string)
        self.assertTrue(stest==st)
        
        st = string
        for s in [substitution2,substitution1]:
            st = s.apply(st)
            
        s21 = compress.combine_overlapping(substitution2,substitution1)
        stest_ = s21(string)
        self.assertTrue(stest_==st)
        return None

    def test_combine_complete_overlap(self,):
        string = "0123456789112345678921234567893123"
        string += '\n'+string
        substitution1 = Substitution(7,12,'abc')
        substitution2 = Substitution(5,22,'ABCDEF')
        
        with self.assertRaises(ValueError):
            compress.permute_non_overlapping(substitution1,substitution2)
            compress.permute_non_overlapping(substitution2,substitution1)
        
        st = string
        for s in [substitution1,substitution2]:
            st = s.apply(st)

        s12 = compress.combine_overlapping(substitution1,substitution2)
        stest = s12.apply(string)
        self.assertTrue(stest==st)
        
        st = string
        for s in [substitution2,substitution1]:
            st = s.apply(st)
            
        s21 = compress.combine_overlapping(substitution2,substitution1)
        stest_ = s21.apply(string)
        self.assertTrue(stest_==st)
        
        substitution1 = Substitution(5,12,'abcdefghijklmnop')
        substitution2 = Substitution(9,15,'ABCDEF')
        
        with self.assertRaises(ValueError):
            compress.permute_non_overlapping(substitution1,substitution2)
            compress.permute_non_overlapping(substitution2,substitution1)
        
        st = string
        for s in [substitution1,substitution2]:
            st = s.apply(st)

        s12 = compress.combine_overlapping(substitution1,substitution2)
        stest = s12.apply(string)
        self.assertTrue(stest==st)
        
        st = string
        for s in [substitution2,substitution1]:
            st = s.apply(st)
            
        s21 = compress.combine_overlapping(substitution2,substitution1)
        stest_ = s21.apply(string)
        self.assertTrue(stest_==st)        
        return None

    def test_combine_same_start(self,):
        string = "0123456789112345678921234567893123"
        string += '\n'+string
        substitution1 = Substitution(7,12,'abc')
        substitution2 = Substitution(7,22,'ABCDEF')
        
        with self.assertRaises(ValueError):
            compress.permute_non_overlapping(substitution1,substitution2)
            compress.permute_non_overlapping(substitution2,substitution1)
        
        st = string
        for s in [substitution1,substitution2]:
            st = s.apply(st)

        s12 = compress.combine_overlapping(substitution1,substitution2)
        stest = s12.apply(string)
        self.assertTrue(stest==st)
        
        st = string
        for s in [substitution2,substitution1]:
            st = s.apply(st)
            
        s21 = compress.combine_overlapping(substitution2,substitution1)
        stest_ = s21.apply(string)
        self.assertTrue(stest_==st)
        
        substitution1 = Substitution(7,8,'abc')
        substitution2 = Substitution(7,9,'ABCDEF')
        
        with self.assertRaises(ValueError):
            compress.permute_non_overlapping(substitution1,substitution2)
            compress.permute_non_overlapping(substitution2,substitution1)
        
        st = string
        for s in [substitution1,substitution2]:
            st = s.apply(st)

        s12 = compress.combine_overlapping(substitution1,substitution2)
        stest = s12.apply(string)
        self.assertTrue(stest==st)
        
        st = string
        for s in [substitution2,substitution1]:
            st = s.apply(st)
            
        s21 = compress.combine_overlapping(substitution2,substitution1)
        stest_ = s21.apply(string)
        self.assertTrue(stest_==st)
        return None

    def test_combine_same_end(self,):
        string = "0123456789112345678921234567893123"
        string += '\n'+string
        substitution1 = Substitution(7,12,'abc')
        substitution2 = Substitution(8,10,'ABCDEF')
        
        with self.assertRaises(ValueError):
            compress.permute_non_overlapping(substitution1,substitution2)
            compress.permute_non_overlapping(substitution2,substitution1)
        
        st = string
        for s in [substitution1,substitution2]:
            st = s.apply(st)

        s12 = compress.combine_overlapping(substitution1,substitution2)
        stest = s12.apply(string)
        self.assertTrue(stest==st)
        
        st = string
        for s in [substitution2,substitution1]:
            st = s.apply(st)
            
        s21 = compress.combine_overlapping(substitution2,substitution1)
        stest_ = s21.apply(string)
        self.assertTrue(stest_==st)
        
        substitution1 = Substitution(7,9,'abc')
        substitution2 = Substitution(8,10,'ABCDEF')
        
        with self.assertRaises(ValueError):
            compress.permute_non_overlapping(substitution1,substitution2)
            compress.permute_non_overlapping(substitution2,substitution1)
        
        st = string
        for s in [substitution1,substitution2]:
            st = s.apply(st)

        s12 = compress.combine_overlapping(substitution1,substitution2)
        stest = s12.apply(string)
        self.assertTrue(stest==st)
        
        st = string
        for s in [substitution2,substitution1]:
            st = s.apply(st)
            
        s21 = compress.combine_overlapping(substitution2,substitution1)
        stest_ = s21.apply(string)
        self.assertTrue(stest_==st)
        return None

    def test_combine_same_start_and_end(self,):
        string = "0123456789112345678921234567893123"
        string += '\n'+string
        substitution1 = Substitution(7,12,'abc')
        substitution2 = Substitution(7,10,'ABCDEF')
        
        with self.assertRaises(ValueError):
            compress.permute_non_overlapping(substitution1,substitution2)
            compress.permute_non_overlapping(substitution2,substitution1)
        
        st = string
        for s in [substitution1,substitution2]:
            st = s.apply(st)

        s12 = compress.combine_overlapping(substitution1,substitution2)
        stest = s12.apply(string)
        self.assertTrue(stest==st)
        
        st = string
        for s in [substitution2,substitution1]:
            st = s.apply(st)
            
        s21 = compress.combine_overlapping(substitution2,substitution1)
        stest_ = s21.apply(string)
        self.assertTrue(stest_==st)
        return None
        