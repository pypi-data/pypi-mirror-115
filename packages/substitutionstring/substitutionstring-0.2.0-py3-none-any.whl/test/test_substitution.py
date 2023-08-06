#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test of the Substitution class

"""

import unittest as ut

from substitutionstring.substitution import Substitution

class TestSubstitution(ut.TestCase):
    
    def test_init(self,):
        subst = Substitution(start=3, end=7, string='abcde')
        self.assertTrue(subst.start==3)
        self.assertTrue(subst.end==7)
        self.assertTrue(subst.string=='abcde')
        self.assertTrue(len(subst)==5)
        self.assertTrue(len(subst)==len(subst.string))
        self.assertTrue(abs(subst)==1)
        self.assertTrue(abs(Substitution(3,9,'123'))==-3)
        with self.assertRaises(ValueError):
            Substitution(-10,12,'AB') # negative start
            Substitution(-10,-8,'AB') # negative end
            Substitution(10,8,'AB') # end < start 
        return None       
    
    def test_apply(self,):
        string = "01234567891123456789"
        subst = Substitution(start=3, end=7, string='abcde')
        sstring = subst(string)
        self.assertTrue(sstring=='012abcde7891123456789')
        sstring_ = Substitution(10,12,'AB').apply(sstring)
        self.assertTrue(sstring_=='012abcde78AB123456789')
        with self.assertRaises(IndexError):
            Substitution(100,120,'AB').apply(string)
            Substitution(10,120,'AB').apply(string)
        return None
    
    def test_revert(self,):
        string = "01234567891123456789"
        subst = Substitution(start=3, end=7, string='abcde')
        sstring = subst(string)
        self.assertTrue(sstring=='012abcde7891123456789')
        revertSubst = subst.revert(string)
        string_test = revertSubst(sstring)
        self.assertTrue(string_test==string)
        return None

    def test_apply_and_revert(self,):
        string0 = "01234567891123456789"
        subst0 = Substitution(start=3, end=7, string='abcde')
        string1, subst1 = subst0.apply_and_revert(string0)
        self.assertTrue(string1=='012abcde7891123456789')
        subst1_ = Substitution(start=3, end=8, string='3456')
        self.assertTrue(subst1_.start==subst1.start)
        self.assertTrue(subst1_.end==subst1.end)
        self.assertTrue(subst1_.string==subst1.string)
        self.assertTrue(subst1_==subst1)
        string2, subst2 = subst1.apply_and_revert(string1)
        self.assertTrue(string2==string0)
        self.assertTrue(subst2==subst0)
        return None
    
    def test_order_substitution(self,):
        """One verifies that the order is maintained in the ensemble of possible Substitutions"""
        configurations = {}    
        sigma1 = ['1','12','123','1234','12345']
        sigma2 = ['a','ab','abc','abcd','abcde']
        for s1 in range(5):
            for s2 in range(5):
                for i1 in range(5):
                    e1 = s1 + i1
                    for i2 in range(5):
                        e2 = s2 + i2
                        for string1 in sigma1:
                            for string2 in sigma2:
                                S1 = Substitution(s1,e1,string1)
                                S2 = Substitution(s2,e2,string2)
                                c1 = S1 < S2
                                c2 = S1 <= S2
                                c3 = S1 > S2
                                c4 = S1 >= S2 
                                configurations[(s1,e1,string1,s2,e2,string2)]=(c1,c2,c3,c4)
        problems_, corrects_ = [], []
        for substitutions, bools in configurations.items():
            if sum(bools) != 1:      
                problems_.append((substitutions,bools))
            elif sum(bools) == 1:
                corrects_.append(substitutions)
        self.assertTrue(len(problems_)==0)
        self.assertTrue(len(corrects_)==len(configurations))
        return True


