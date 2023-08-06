#!/usr/bin/env python3

from __future__ import print_function

### Groups a list according to the specified function
# @param [in] arr       - Array to group
# @param [in] fnc       - Function that specifies grouping
#                           The function should take two parameters
#                           and return True if the items belong in
#                           the same group.
# @param [in] vals      - Set to True if you want the function
#                         to return a list of values.  If set
#                         to False, the function will return a
#                         list of keys.
#
# Example to group items less than three appart
# @begincode
#
# groups = groupList([1, 3, 6, 10, 12, 14, 21, 35], lambda a, b: 3 >= abs(a-b), True)
#
# > [[1, 3, 6], [10, 12, 14], [21], [35]]
#
# @endcode
#
def groupList(arr, fnc, vals = False):

    l = len(arr)
    if 1 > l:
        return []
    elif 1 == l:
        return [[0]]

    g = 0
    m = [-1] * l
    for k1 in range(0, l):

        for k2 in range(k1 + 1, l):

            # Can they be grouped?
            if fnc(arr[k1], arr[k2]):

                # a nor b in group, a and b join new group
                if -1 == m[k1] and -1 == m[k2]:
                    m[k1] = g
                    m[k2] = g
                    g += 1

                # a not in group, b in group, a joins b
                elif -1 == m[k1] and -1 != m[k2]:
                    m[k1] = m[k2]

                # a in group, b not in group, b joins a
                elif -1 != m[k1] and -1 == m[k2]:
                    m[k2] = m[k1]

                # Both in groups, merge groups if not already in the same group
                elif m[k1] != m[k2]:
                    g = g - 1
                    fr = m[k1]
                    to = m[k2]
                    if g == to:
                        to, fr = fr, to
                    for k3 in range(0, l):
                        if m[k3] == fr:
                            m[k3] = to
                        elif m[k3] == g:
                            m[k3] = fr

        # Create new group
        if -1 == m[k1]:
            m[k1] = g
            g += 1

    ret = [[] for i in range(0, g)]
    for k in range(0, l):
        ret[m[k]].append(arr[k] if vals else k)

    return ret


### Groups a list according to the specified function
#
# This function is the same as groupList() but it minimizes the number
# of calls to the given compare function.
#
# @param [in] arr       - Array to group
# @param [in] fnc       - Function that specifies grouping
#                           The function should take two parameters
#                           and return True if the items belong in
#                           the same group.
# @param [in] vals      - Set to True if you want the function
#                         to return a list of values.  If set
#                         to False, the function will return a
#                         list of keys.
#
# Example to group items less than three appart
# @begincode
#
# groups = groupList2([1, 3, 6, 10, 12, 14, 21, 35], lambda a, b: 3 >= abs(a-b), True)
#
# > [[1, 3, 6], [10, 12, 14], [21], [35]]
#
# @endcode
#
def groupList2(arr, fnc, vals = False):

    l = len(arr)
    if 1 > l:
        return []
    elif 1 == l:
        return [[0]]

    lg = -1
    m = [-1] * l
    g = [-1] * l

    # Create a group map
    for k1 in range(0, l):
        ingroup = -1
        gi = 0
        while -1 != g[gi]:

            # First group item
            k2 = g[gi]

            while True:

                # Does it group with this item
                if fnc(arr[k1], arr[k2]):

                    # If we're already in a group, merge that group
                    if -1 != ingroup:

                        # Find the end of the group we're in
                        eg = k1
                        while m[eg] != -1:
                            eg = m[eg]

                        # Append current group
                        m[eg] = g[gi]

                        # Move last group to current slot
                        g[gi] = g[lg]
                        g[lg] = -1
                        lg -= 1
                        gi -= 1

                    # Add us to this group
                    else:

                        # Insert ourselves here
                        m[k1] = m[k2]
                        m[k2] = k1

                        # Item has been grouped
                        ingroup = gi

                    break

                # Last item?
                if m[k2] == -1:
                    break

                # Next item
                k2 = m[k2]

            gi += 1

        # Create a new group if it didn't fit anywhere
        if -1 == ingroup:
            g[gi] = k1
            lg = gi

    # Create groups by crawling the map
    gi = 0
    ret = []
    while gi < len(g) and -1 != g[gi]:

        # Where to start in the map
        mi = g[gi]

        ret.append([])
        ri = len(ret)-1
        while True:

            # Log(mi)

            ret[ri].append(arr[mi] if vals else mi)

            # Last item?
            if m[mi] == -1:
                break

            # Next item
            mi = m[mi]

        # Next group
        gi += 1

    return ret


### Groups a dict according to the specified function
# @param [in] arr       - Array to group
# @param [in] fnc       - Function that specifies grouping
#                           The function should take two parameters
#                           and return True if the items belong in
#                           the same group.
# @param [in] vals      - Set to True if you want the function
#                         to return a list of values.  If set
#                         to False, the function will return a
#                         list of keys.
#
# Example to group items less than three appart
# @begincode
#
# d = {'k0': 1, 'k1': 3, 'k2': 6, 'k3': 10, 'k4': 12, 'k5': 14, 'k6': 21, 'k7': 35, 'k8': 7, 'k9': 23}
# groups = groupDict(d, lambda a, b: 3 >= abs(a-b), True)
#
# @endcode
#
def groupDict(obj, fnc, vals = False):

    m = groupList([*obj.values()], fnc, vals)

    # Map keys
    if not vals:
        k = [*obj.keys()]
        for g in m:
            for i in range(0, len(g)):
                g[i] = k[g[i]]

    return m


### Groups a dict according to the specified function
#
# This function is the same as groupDict() but it minimizes the number
# of calls to the given compare function.
#
# @param [in] arr       - Array to group
# @param [in] fnc       - Function that specifies grouping
#                           The function should take two parameters
#                           and return True if the items belong in
#                           the same group.
# @param [in] vals      - Set to True if you want the function
#                         to return a list of values.  If set
#                         to False, the function will return a
#                         list of keys.
#
# Example to group items less than three appart
# @begincode
#
# d = {'k0': 1, 'k1': 3, 'k2': 6, 'k3': 10, 'k4': 12, 'k5': 14, 'k6': 21, 'k7': 35, 'k8': 7, 'k9': 23}
# groups = groupDict2(d, lambda a, b: 3 >= abs(a-b), True)
#
# @endcode
#
def groupDict2(obj, fnc, vals = False):

    m = groupList2([*obj.values()], fnc, vals)

    # Map keys
    if not vals:
        k = [*obj.keys()]
        for g in m:
            for i in range(0, len(g)):
                g[i] = k[g[i]]

    return m

