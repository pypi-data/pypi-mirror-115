#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test of the substitution_tools
"""

import unittest as ut

from substitutionstring.substitution import Substitution
from substitutionstring import substitution_tools as t

class TestSubstitutionTools(ut.TestCase):
    
    def test_substitute_and_revert(self,):
        string = "01234567891123456789"
        substitution = Substitution(start=3,end=7,string="abcd")
        string_, subst = t.apply_substitution(string, substitution)
        string__, subst_ = t.apply_substitution(string_, subst)
        self.assertTrue(string__==string)
        self.assertTrue(substitution.start==subst_.start)
        self.assertTrue(substitution.end==subst_.end)
        self.assertTrue(substitution.string==subst_.string)
        return None

        