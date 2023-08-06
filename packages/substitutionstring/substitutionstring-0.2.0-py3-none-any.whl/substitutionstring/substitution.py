#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
At a really basic level, the only modifications a string can tolerate are either
 - delete a part of the string from position `start` to position `end`
 - insert a `string` at position `start`

But these two modifications are in fact the two facets of a substitution, this later object having three attributes `start`, `end` and `string` since one has that
 - inserting a string into a string consists in susbstituting a new string when `start=end`, while
 - deleting a string consists in substituting an empty string between different `start` and `end` positions

By itself, a `Substitution` has no real meaning, since it does not handle the state of the string before and after the Substitution is performed. Then, one has to collect either: 
 1) the initial state of the string and the sequence of all the `Substitution` this string undergoes
or
 2) the final state of the string and the sequence of all the `Substitution` this string can undergo to recover its initial state

The second case is automatically handled by the object `SubstitutionString` somewhere else in this package. The first case can be recovered from the `SubstitutionString` object by using its `reversed` method.

"""

from typing import TypeVar, Type, Tuple
S = TypeVar('Substitution', bound='Substitution')

class Substitution():
    """
Represent the parameters of a substitution in a string, that is
 - `start` : the position into a given string where the deletion starts,
 - `end` : the position of a given string where the deletion ends (thus the part `string[start:end]` will be removed),
 - `string` : the string which will be inserted between start and end. Do not confound the `string` contained in this argument (which can be thought as a children string), and the string onto which the `Substitution` might apply (and can be thought as a parent string).
         
The `Substitution` class has been designed to work specifically in some reversible cleaning objects as a container for later uses. 

See elsewhere the class `SubstitutionString` for instance.
     
    """
    def __init__(self,start: int=0,end: int=0,string: str=str()) -> None:
        """
Parameters | Type | Details
-- | -- | --
`start` | integer | The position where the deletion in the parent string will start if method `Substitution.apply(string)` is called. Default is `0`
`end` | integer | The position where the deletion in the parent string will end if method `Substitution.apply(string)` is called. Default is `0`.
`string` | string | The string that will be inserted in between the `start` and `end` positions of the parent string, if method `Substitution.apply(string)` is called. Default is the empty string.

All these parameter become attributes of the `Substitution` instance.

Returns `None`.
        """
        self.start = int(start)
        self.end = int(end)
        bools = [self.end<self.start, self.end<0,  self.start<0]
        if any(bools):
            mess = "Substitution.end must be larger than Substitution.start"
            mess += " and only accepts non-negative values"
            raise ValueError(mess)
        self.string = str(string)
        return None
    
    def __len__(self,) -> int:
        """Returns the length (an integer) of the `Substitution.string` attribute."""
        return len(self.string)
    
    def __abs__(self,) -> int:
        """
Returns the change of length of the parent string if method `Substitution.apply(string)` is called. Note that this value can be negative if the inserted string is smaller than the deleted one.
        
Examples : 
```python3
abs(Substitution(3,5,'123456')) = 4
abs(Substitution(3,9,'123')) = -3
```
        """
        return self.start - self.end + len(self.string)
    
    def __repr__(self,) -> str:
        """Displays the three attributes of the `Substitution` class."""
        mess = 'Substitution(start={}, '.format(self.start)
        mess += "end={}, string=`{}`)".format(self.end,self.string)
        return mess
    
    def __eq__(self, substitution: Type[S]) -> bool:
        """
Parameters | Type | Details
-- | -- | --
`substitution` | `Substitution` instance | The `Substitution` instance to be compared with the actual one.

Returns | Type | Details
-- | -- | --
`bools` | boolean | Returns True if all `start`, `end` and `string` arguments are equal among the two `Substitution` instances. Otherwise returns False. 

Raises | Details
-- | -- 
AttributeError | In case `substitution` is not a valid `Substitution` instance.
        """
        bools = [self.start==substitution.start,
                 self.end==substitution.end,
                 self.string==substitution.string]
        return all(bools)

    def __gt__(self, substitution: Type[S]) -> bool:
        """
Parameters | Type | Details
-- | -- | --
`substitution` | `Substitution` instance | The `Substitution` instance to be compared with the actual one.

Returns | Type | Details
-- | -- | --
`bools` | boolean | Returns `True` when `substitution` is completely on the left of `Substitution` without overlapping. Otherwise returns `False`. 

Raises | Details
-- | -- 
AttributeError | In case `subst` is not a valid `Substitution` instance (at least it has no `end` attribute).

`Substitution` is supposed to apply prior to `substitution` for the notion of overlapping to be make sense, and the two `Substitution` should be consecutive in a sequence of `Substitution`, applied to a given parent string. These conditions can not be verified at the level of the `Substitution` object.
        """
        condition = self.start > substitution.end
        return True if condition else False

    def __ge__(self, substitution: Type[S]) -> bool:
        """
Parameters | Type | Details
-- | -- | --
`substitution` | `Substitution` instance | The `Substitution` instance to be compared with the actual one.

Returns | Type | Details
-- | -- | --
`bools` | boolean | `True` when `substitution` partially overlaps on the left of the `Substitution` object. Otherwise `False`.  

Raises | Details
-- | -- 
AttributeError | In case `substitution` is not a valid `Substitution` instance (neither `start` nor `end` attribute, or at least of them absent).

`Substitution` is supposed to apply prior to `substitution` for the notion of overlapping to be make sense, and the two `Substitution` should be consecutive in a sequence of `Substitution`, applied to a given parent string. These conditions can not be verified at the level of the `Substitution` object.
        """
        condition = substitution.start <= self.start <= substitution.end
        return True if condition else False
    
    def __lt__(self, substitution: Type[S]) -> bool:
        """
Parameters | Type | Details
-- | -- | --
`substitution` | `Substitution` instance | The `Substitution` instance to be compared with the actual one.

Returns | Type | Details
-- | -- | --
`bools` | boolean | `True` when `substitution` is completely on the irght of the `Substitution` object without overlapping. Otherwise `False`.  

Raises | Details
-- | -- 
AttributeError | In case `substitution` is not a valid `Substitution` instance (at least it has no `start` attribute).

`Substitution` is supposed to apply prior to `substitution` for the notion of overlapping to be make sense, and the two `Substitution` should be consecutive in a sequence of `Substitution`, applied to a given parent string. These conditions can not be verified at the level of the `Substitution` object.
        """
        condition = self.start + len(self) < substitution.start
        return True if condition else False
    
    def __le__(self, substitution: Type[S]) -> bool:
        """
Parameters | Type | Details
-- | -- | --
`substitution` | `Substitution` instance | The `Substitution` instance to be compared with the actual one.

Returns | Type | Details
-- | -- | --
`bools` | boolean | `True` when `substitution` partially overlaps on the right of the `Substitution` object. Otherwise `False`.  

Raises | Details
-- | -- 
AttributeError | In case `substitution` is not a valid `Substitution` instance (at least it has no `start` attribute).

`Substitution` is supposed to apply prior to `substitution` for the notion of overlapping to be make sense, and the two `Substitution` should be consecutive in a sequence of `Substitution`, applied to a given parent string. These conditions can not be verified at the level of the `Substitution` object.
        """
        condition = self.start < substitution.start <= self.start + len(self)
        return True if condition else False
    
    def __check_start_end_string(self, string: str) -> None:
        """Check whether the parameters of the `Substitution` instance are compatible with the given `string`. Raises an IndexError in case they are not compatible."""
        bools = [self.start>len(string), self.start<0,
                 self.end>len(string), self.end<0,
                 self.start>self.end,]
        if any(bools):
            mess = "Incompatible string for Substitution: "
            mess += "got start={}, end={} ".format(self.start, self.end)
            mess += "for a string of length {}".format(len(string))
            raise IndexError(mess)
        return None
    
    def apply(self, string: str) -> str:
        """
Apply the `Substitution` to a given parent`string`. Returns the string after the substitution is performed. Raises an IndexError in case the Substitution and the string are not compatible.

Parameters | Type | Details
-- | -- | --
`string` | a string | The parent string onto which the `Substitution` will be applied.

Returns | Type | Details
-- | -- | --
`string` | string | The state of the parent string once the substitution is done.

Raises | Details
-- | -- 
IndexError | In case `Substitution` is not compatible with the parent string. For instance if `Substitution.end` is larger than the length of the input `string`.
        """
        self.__check_start_end_string(string)
        return string[:self.start] + self.string + string[self.end:]
    
    def __call__(self, string: str) -> str:
        """Alias for `Substitution.apply(string)`. Returns a string."""
        return self.apply(string)
    
    def revert(self, string: str) -> Type[S]:
        """
Reverts the `Substitution` object that one can apply to the modified string in order to recover the initial one.

Parameters | Type | Details
-- | -- | --
`string` | a string | The parent string onto which the `Substitution` should be applied. The `Substitution` will not be applied, but its inverse will be calculated and returned.

Returns | Type | Details
-- | -- | --
`substitution` | `Substitution` instance | The `Substitution` that should be applied to `Substitution.apply(string)` in order to recover the initial string.
        
Example:
```python3
string = '0123456789'
subst = Substitution(3,5,'abc')
sub_string = subst.apply(string) # returns '012abc56789'
revertSubst = subst.revert(string)
revertSubst.apply(sub_string) # returns '0123456789'
```
        """
        substitution = Substitution(start = self.start,
                                    end = self.start+len(self),
                                    string = string[self.start:self.end])  
        return substitution
    
    def apply_and_revert(self, string: str) -> Tuple[str, Type[S]]:
        """

Perform both the `Substitution.apply` and the `Substitution.revert` onto a string. Returns the string and the `Substitution` object, in that order.

Parameters | Type | Details
-- | -- | --
`string` | a string | The parent string onto which the `Substitution` will be applied.

Returns | Type | Details
-- | -- | --
`string` | a string | The state of the string after the `Substitution` is performed.
`substitution` | `Substitution` instance | The `Substitution` that should be applied to `Substitution.apply(string)` in order to recover the initial string.
        
Examples : 
```python3
string = '0123456789'
subst = Substitution(3,5,'abcde')
string_, subst_ = subst.apply_and_revert(string)
# string_ is '012abcde56789'
# subst_ is Substitution(3, 8, '34')
subst_.apply(string_) # gives back the string '0123456789'
```
        
Note that an `apply_and_revert` applied twice give back the initial objects.

```python3
string0 = '0123456789'
subst0 = Substitution(3,5,'abcde')
string1, subst1 = subst0.apply_and_revert(string0)
string2, subst2 = subst1.apply_and_revert(string1)
assert(string2==string0)
assert(subst2==subst0)
```
        """
        return self.apply(string), self.revert(string)

    def shift_start_end(self, start: int, end: int) -> Tuple[int, int]:
        """
Find the new position `start` and `end` (seen as the index of a string) as if `Substitution` was not applied. This method allows to transfer the position of a token throught the different `Substitution` objects of a sequence. It is useful for the `restore` method of a `SubstitutionString` instance.

Parameters | Type | Details
-- | -- | --
`start` | int | The initial position inside a string that one wants to shift by the `Substitution`
`end` | int | The final position inside a string that one wants to shift by the `Substitution`.

Returns | Type | Details
-- | -- | --
`start` | int | The shifted initial position.
`end` | int| The shifted final position.

Examples:
```
python
string0 = '0123456789'
subst0 = Substitution(3,5,'abcde')
string1, subst1 = subst0.apply_and_revert(string0)

# string1[3:8] is 'abcde'
start0, end0 = subst1.shift_start_end(3,8) # returns 3,5
# string0[start0:end0] is '34', the deleted part of string0 by subst0

# string0[3:5] is '34', the deleted part of string0 by subst0
start1, end1 = subst0.shift_start_end(3,5) # returns 3,8
# string1[3:8] is 'abcde', the inserted part of string1 from string0 by subst0
```
        """
        if self.end <= start:
            start += abs(self)
        elif self.start <= start <= self.end:
            start = self.start
        if self.end <= end:
            end += abs(self)
        elif self.start < end <= self.end:
            end = self.start + len(self)  
        return start, end
