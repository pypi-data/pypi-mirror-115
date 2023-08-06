#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pkg_resources import get_distribution
__version__ = get_distribution("substitutionstring").version

from .substitution import Substitution
from .substitution_string import SubstitutionString
from .substitution_sequence import SubstitutionSequence
