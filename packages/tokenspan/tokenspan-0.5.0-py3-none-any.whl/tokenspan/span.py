#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
`Span` class

`Span` sub-classes the `string` class in Python, thus enabling basic usages of
string (as e.g. isupper, lower, ... see 
https://docs.python.org/3.8/library/string.html)

Its main original methods are
 - `partition(range(start,stop))` : which partitions the initial `Span` in three
 new `Span` instance, collected in a unique `Spans` instance (see below)
 - `split([range(start,end),range(start2,end2), ...])` : which splits the `Span`
 in several instances grouped in a a list of `Span` objects
 - `slice(start,stop,size,step)` : which slices the initial string from position 
`start` to position `stop` by `step` in sub-strings of size `size`, all grouped 
in a list of Span objects

"""

from .tools import _checkRange, _checkRanges, _startstop, _removeRange
from .tools import _checkSpan, _checkSameString
from .tools import _combineRanges, _cutRanges

class Span():
    """
Pseudo-Subclass of the Python string class.
It allows manipulating a string as a usual Python object, excepts it 
returns Span instances. Especially for Span instances are the 
methods : 
 - `isupper()` (for instance), which tells whether the string is 
 uppercase or not
 - `lower()` or `upper()`, to make the `Span` lower-/upper-case.
See more string methods on [the Python standard library documentation](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str).

    """ 
    
    def __init__(self,
                 string='',
                 ranges=[],
                 subtoksep=chr(32),):
        """
`Span` object is basically a `string` with a `ranges` (list of range) position. Its basic usage is : 
 - `string` extracted from all intervals defined in the `ranges` list
and its attributes are
 - `Span.string`	 -> a string
 - `Span.ranges`	 -> a list of ranges
 - `Span.subtoksep` -> a string, preferably of length 1
         """
        self.string = str(string)
        # self._extra_attributes = set(_Span_methods)
        self.subtoksep = str(subtoksep)
        # check if ranges are correct
        _checkRanges(ranges)
        # correct ranges in case some are over the string size
        ranges_ = [range(*_startstop(self.string,r.start,r.stop))
                   for r in ranges]
        # withdraw overlapping ranges
        self.ranges = _combineRanges(ranges_)
        if not self.ranges:
            self.ranges.append(range(len(self.string)))
        return None

    def _append_range(self, r):
        """Utility that appends a range in self.ranges"""
        _checkRange(r)
        # recasts r.start and r.stop inside the range(0,len(self.string))
        start, stop = _startstop(self.string,r.start,r.stop)
        self.ranges.append(range(start,stop))
        return None

    def append_range(self, r):
        """
Append a range object to self.ranges. The range r must be given in absolute coordinates.
Return self (append in place).
Raise a ValueError in case r is not a range object.
Raise a Warning in case r has start or stop attributes outside the size of Span.string, in which case thse parameters are recalculated to fit Span.string (being either 0 for start or len(Span.string) for stop).
        """
        self._append_range(r)
        self.ranges = [r for r in _combineRanges(self.ranges) if r]
        return self
    
    def append_ranges(self,ranges):
        """
Append a list of range objects to self.ranges. This method applies `append_range` several times, so please see its documentation for more details.
        """
        for r in ranges:
            self._append_range(r)
        self.ranges = [r for r in _combineRanges(self.ranges) if r]
        return self

    def _remove_range(self,r):
        """Utility that removes a range from self.ranges"""
        _checkRange(r)
        self.ranges = _removeRange(self.ranges,r)
        return None

    def remove_range(self,r):
        """
Remove the range r from Span.ranges. The range r must be given in absolute coordinates.
Return self (remove in place).
In case the range r encompass the complete string, there is no more Span.ranges associated to the outcome of this method.
        """
        self._remove_range(r)
        return self

    def remove_ranges(self,ranges):
        """
Remove a list of range objects toself.ranges. This method applies `remove_range` several times, so please see its documentation for more details.
        """
        for r in ranges:
            self._remove_range(r)
        return self

    def __len__(self):
        """Return the length of the string associated with the Span"""
        l = sum(r.stop-r.start for r in self.ranges) 
        l += (len(self.ranges)-1)*len(self.subtoksep)
        return l if l>0 else 0 # in case there is no ranges
    
    def __repr__(self):
        """Return the two main arguments (namely the `string` and the number of ranges) of a `Span` instance in a readable way."""
        mess = "Span('{}', ".format(str(self))
        mess += '['+','.join('('+str(r.start)+','+str(r.stop)+')' 
                             for r in self.ranges)
        mess += "])"
        return mess   
    
    def __str__(self):
        """
`str(Span)` method returns the recombination of the extract of each `Span.subSpan` from the `Span.string` attribute corresponding to all its `Span.ranges` attribute.
        """
        return self.subtoksep.join(self.string[r.start:r.stop] 
                                   for r in self.ranges)
    
    def __contains__(self,s):
        """If the object to be compared with is a Span related to the same string as this instance, check whether the ranges are overlapping. Otherwise, check whether the string str(s) (which transforms the other Span instance in a string in case s is not related to the same string) is a sub-string of the `Span` instance."""
        try:
            _checkSpan(s)
        except ValueError:
            b = str(s) in str(self)
        else:
            if s.string==self.string:
                b = any(r1.start<=r2.start and r1.stop>=r2.stop 
                        for r1 in self.ranges for r2 in s.ranges)
            else:
                b = False
        return b
    
    def __bool__(self):
        """Return `True` if the `Span.ranges` is non-empty, otherwise return `False`"""
        return bool(len(self))
    
    def __getitem__(self,n):
        """
Allow slice and integer catch of the elements of the string of `Span`.
Return a string.

Note: As for the usual Python string, a slice with positions outside str(Span) will outcome an empty string, whereas Span[x] with x>len(Span) would results in an IndexError.
        """
        return str(self)[n]

    def get_subSpan(self,n):
        """
Get the Span associated to the ranges elements n (being an integer or a slice).
Return a Span.
Raise a IndexError in case n is larger than the number of ranges in self.ranges.
        """
        span = Span(string=self.string,
                    ranges=[self.ranges[n],],
                    subtoksep=self.subtoksep)          
        return span
    
    @property
    def subSpans(self,):
        """
Get the Span associated to each Span.ranges in a Span object.
Return a Spans object. Keep the attributes in case Span.carry_attributes is True. 
        """
        return [self.get_subSpan(i) for i in range(len(self.ranges))]

    def __eq__(self,span):
        """
Verify whether the actual instance of Span and an extra ones have the same attributes. 

Returns a boolean.

Raise a ValueError when one object is not a Span instance
        """
        _checkSpan(span)
        bools = [span.string==self.string,
                 span.ranges==self.ranges,
                 span.subtoksep==self.subtoksep,]
        return all(bools)

    def __add__(self,span):
        """If the two Span objects have same strings, returns a new Span object with combined ranges of the initial ones."""
        return self.union(span)

    def __sub__(self,span):
        """If the two Span objects have same strings, returns a new Span object with ranges of self with Span ranges removed. Might returns an empty Span."""
        return self.difference(span)

    def __mul__(self,span):
        """If the two Span objects have same strings, returns a new Span object with ranges of self having intersection with Span ranges removed. Might returns an empty Span."""
        return self.intersection(span)

    def __truediv__(self,span):
        """If the two Span objects have same strings, returns a new Span object with ranges of self having symmetric_difference with Span ranges removed. Might returns an empty Span."""
        return self.symmetric_difference(span)
    
    @property
    def start(self,):
        """Returns the starting position (an integer) of the first ranges. Make sense only for contiguous Span."""
        return self.ranges[0].start
    @property
    def stop(self,):
        """Returns the ending position (an integer) of the last ranges. Make sense only for contiguous Span."""
        return self.ranges[-1].stop

    def union(self, span):
        """
Takes a Span object as entry, and returns a new Span instance, with Span.ranges given by the union of the actual Span.ranges with the span.ranges, when one sees the `ranges` attributes as sets of positions of each instance.

| Parameters | Type | Details |
| --- | --- | --- | 
| `span` | `Span` object | A Span object with same mother string (Span.string) and eventually different ranges that the actual instance. |

| Returns | Type | Details |
| --- | --- | --- | 
| `newSpan` | `Span` object | A `Span` object with `newSpan.ranges` = union of `Span.ranges` and `span.ranges` |

| Raises | Details | 
| --- | --- |
| ValueError | in case the entry is not a Span instance. |
| TypeError | in case the span.string is not the same as Span.string. |
        """
        _checkSpan(span)
        _checkSameString(self,span,'Span')
        newSpan = Span(string=self.string,
                       subtoksep=self.subtoksep,
                       ranges=self.ranges).append_ranges(span.ranges)
        return newSpan

    def difference(self, span):
        """
Takes a Span object as entry, and returns a new Span instance with Span.ranges given by the difference of the actual Span.ranges with the span.ranges, when one sees the `ranges` attributes as sets of positions of each instance.

| Parameters | Type | Details |
| --- | --- | --- | 
| `span` | `Span` object | A Span object with same mother string (Span.string) and eventually different ranges that the actual instance. |

| Returns | Type | Details |
| --- | --- | --- | 
| `newSpan` | `Span` object | A `Span` object with `newSpan.ranges` = difference of `Span.ranges` and `span.ranges`. |

| Raises | Details | 
| --- | --- |
| ValueError | in case the entry is not a Span instance. |
| TypeError | in case the span.string is not the same as Span.string. |
        """
        _checkSpan(span)
        _checkSameString(self,span,'Span')
        newSpan = Span(string=self.string,
                       subtoksep=self.subtoksep,
                       ranges=self.ranges).remove_ranges(span.ranges)
        return newSpan
    
    def intersection(self,span):
        """
Takes a Span object as entry and returns a new Span whose Span.ranges given by the intersection of the actual Span.ranges with the span.ranges, when one sees the `ranges` attributes as sets of positions of each instance..

| Parameters | Type | Details |
| --- | --- | --- | 
| `span` | `Span` object | A Span object with same mother string (Span.string) and eventually different ranges that the actual instance. |

| Returns | Type | Details |
| --- | --- | --- | 
| `newSpan` | `Span` object | A `Span` object with `newSpan.ranges` = intersection of `Span.ranges` and `span.ranges` |

| Raises | Details | 
| --- | --- |
| ValueError | in case the entry is not a Span instance. |
| TypeError | in case the span.string is not the same as Span.string. |
        """
        _checkSpan(span)
        _checkSameString(self,span,'Span')
        # one uses the fact that AxB = A+B-(A-B)-(B-A)
        AmB = Span(string=self.string,
                   subtoksep=self.subtoksep,
                   ranges=self.ranges).remove_ranges(span.ranges)
        BmA = Span(string=self.string,
                   subtoksep=self.subtoksep,
                   ranges=span.ranges).remove_ranges(self.ranges)
        newSpan = Span(string=self.string,
                       subtoksep=self.subtoksep,
                       ranges=span.ranges).append_ranges(self.ranges)
        newSpan.remove_ranges(BmA.ranges)
        newSpan.remove_ranges(AmB.ranges)
        ranges = [r for r in _combineRanges(newSpan.ranges) if r]
        if not ranges:
            newSpan = Span()
            newSpan.ranges = ranges
        else:
            newSpan.ranges = ranges
        return newSpan
    
    def symmetric_difference(self,span):
        """
Takes a Span object as entry, and return a new Span instance whose Span.ranges given by the symmetric difference of the actual Span.ranges with the span.ranges, when one sees the `ranges` attributes as sets of positions of each instance..

| Parameters | Type | Details |
| --- | --- | --- | 
| `span` | `Span` object | A Span object with same mother string (Span.string) and eventually different ranges that the actual instance. |

| Returns | Type | Details |
| --- | --- | --- | 
| `newSpan` | `Span` object | A `Span` object with `newSpan.ranges` = symmetric difference of `Span.ranges` and `span.ranges` |

| Raises | Details | 
| --- | --- |
| ValueError | in case the entry is not a Span instance. |
| TypeError | in case the span.string is not the same as Span.string. |
        """
        _checkSpan(span)
        _checkSameString(self,span,'Span')
        # one uses the fact that A/B = (A-B)+(B-A)
        AmB = Span(string=self.string,
                   subtoksep=self.subtoksep,
                   ranges=self.ranges).remove_ranges(span.ranges)
        BmA = Span(string=self.string,
                   subtoksep=self.subtoksep,
                   ranges=span.ranges).remove_ranges(self.ranges)
        newSpan = Span(string=self.string,
                       subtoksep=self.subtoksep,
                       ranges=AmB.ranges).append_ranges(BmA.ranges)
        newSpan.ranges = [r for r in _combineRanges(newSpan.ranges) if r]
        return newSpan
      
    def _prepareSpans(self,ranges,remove_empty):
        """Utility that removes empty ranges and constructs a list of Span objects."""
        if remove_empty:
            ranges = [r for r in ranges if any(r_ for r_ in r) or len(r)==2]
            # or len==2: to handle the case containing only a subtoksep
        spans = [Span(string=self.string,ranges=r,subtoksep=self.subtoksep)
                  for r in ranges]
        return spans
    
    def partition(self,start,end,remove_empty=False):
        """
Split the `Span.string` in three `Span` objects : 
 - `string[:start]`
 - `string[start:stop]`
 - `string[stop:]`
and put all non-empty `Span` objects in a `Spans` instance.

It acts a bit like the `str.partition(s)` method of the Python
`string` object, but `partition_Span` takes `start` and `end` 
argument instead of a string. So in case one wants to split a string in three 
sub-strings using a string 's', use `Span.partition(s)` instead, 
inherited from `str.partition(s)`.

NB : `Span.partition(s)` has no `non_empty` option.

| Parameters | Type | Details |
| --- | --- | --- | 
| `start` | int | Starting position of the splitting sequence. |
| `end` | int | Ending position of the splitting sequence. |
| `remove_empty` | bool. Default is `False` | If `True`, returns a `list of Span` instance with only non-empty `Span` objects. see `__bool__()` method for non-empty `Span` |

| Returns | Type | Details |
| --- | --- | --- | 
| `spans` | `list` of `Span` objects | The `list` object containing the different `Span` objects. |
        """
        start,end = _startstop(self,start,end)
        # ranges = _splitRanges(self.ranges,start,end,step=len(self.subtoksep))
        r1,temp_ranges = _cutRanges(self.ranges,start,step=len(self.subtoksep))
        r2,r3 = _cutRanges(temp_ranges,end-start,step=len(self.subtoksep))
        ranges = [r1,r2,r3]
        spans = self._prepareSpans(ranges,remove_empty)
        return spans
    
    def split(self,cuts,remove_empty=False):
        """
Split a text as many times as there are range entities in the cuts list.
Return a `Spans` instance.

This is a bit like `str.split(s)` method from Python `string`
object, except one has to feed `Span.split` with a full list
of `range(start,end)` range objects instead of the string 's' in `str.split(s)`
If the `range(start,end)` tuples in cuts are given by a regex re.finditer
search on `str(Span)`, the two methods give the same thing. 

| Parameters | Type | Details |
| --- | --- | --- | 
| `cuts` | a list of `range(start,end,)` range objects. start/end are integer | Basic usage is to take these cuts from [`re.finditer`](https://docs.python.org/3/library/re.html#re.finditer). The start/end integers are given in the relative coordinate system, that is, in terms of the position in `str(Span)`. |
| `remove_empty` | bool. Default is `False` | If `True`, returns a `list of Span` instance with only non-empty `Span` objects. see `__bool__()` method for non-empty `Span` |

| Return | Type | Details |
| --- | --- | --- | 
| `spans` | `list` of `Span` objects | The `list` object containing the different `Span` objects. |

        """
        _checkRanges(cuts)
        split_ranges = list()
        r1,r_temp = _cutRanges(self.ranges,cuts[0].start,step=len(self.subtoksep))
        r2,r_temp = _cutRanges(r_temp,len(cuts[0]),step=len(self.subtoksep))
        cursor = cuts[0].stop
        split_ranges += [r1,r2,]
        if len(cuts) < 2:
            return self._prepareSpans(split_ranges + [r_temp,], remove_empty)
        for r in cuts[1:]:
            r1,r_temp = _cutRanges(r_temp,r.start-cursor,step=len(self.subtoksep))
            r2,r_temp = _cutRanges(r_temp,len(r),step=len(self.subtoksep))
            split_ranges += [r1,r2,]
            cursor = r.stop
        split_ranges.append(r_temp)
        spans = self._prepareSpans(split_ranges, remove_empty)      
        return spans

    def slice(self,start=0,stop=None,size=1,step=1,remove_empty=False):
        """
Cut the `Span.string` in overlapping sequences of strings of size `size` by `step`,
put all these sequences in separated `Span` objects, and finally 
put all theses objects in a `Spans` instance.

| Parameters | Type | Details |
| --- | --- | --- | 
| `start` | int | The relative position where to start slicing the Span. |
| `stop` | int | The relative position where to stop slicing the Span. |
| `size` | int | The size of the string in each subsequent Span objects. |
| `step` | int | The number of characters skipped from one Span object to the next one. A character is given by `str(Span)` (relative coordinate) |

| Returns | Type | Details |
| --- | --- | --- | 
| `spans` | `list` of `Span` objects | The `list` object containing the different `Span` objects. |
        """
        start, stop = _startstop(self,start,stop)
        cuts = [(i,i+size) for i in range(start,stop-size+1,step)]
        slice_ranges = list()
        for start,end in cuts:
            r1,temp_ranges = _cutRanges(self.ranges,start,step=len(self.subtoksep))
            r2,r3 = _cutRanges(temp_ranges,end-start,step=len(self.subtoksep))
            slice_ranges.append(r2)
        spans = self._prepareSpans(slice_ranges,remove_empty)
        return spans
