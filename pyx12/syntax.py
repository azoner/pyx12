######################################################################
# Copyright (c) 2001-2011 
#   John Holland <john@zoner.org>
# All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.
#
######################################################################

#    $Id: map_if.py 1472 2011-10-13 19:20:13Z johnholland $

"""
X12 syntax validation functions
"""


def is_syntax_valid(seg_data, syn):
    """
    Verifies the segment against the syntax
    @param seg_data: data segment instance
    @type seg_data: L{segment<segment.Segment>}
    @param syn: list containing the syntax type, and the indices of elements
    @type syn: list[string]
    @rtype: tuple(boolean, error string)
    """
    # handle intra-segment dependancies
    if len(syn) < 3:
        err_str = 'Syntax string must have at least two comparators (%s)' \
            % (syntax_str(syn))
        return (False, err_str)

    syn_code = syn[0]
    syn_idx = [int(s) for s in syn[1:]]

    if syn_code == 'P':
        count = 0
        for s in syn_idx:
            if len(seg_data) >= s and seg_data.get_value('%02i' % (s)) != '':
                count += 1
        if count != 0 and count != len(syn_idx):
            err_str = 'Syntax Error (%s): If any of %s is present, then all are required'\
                % (syntax_str(syn), syntax_ele_id_str(seg_data.get_seg_id(), syn_idx))
            return (False, err_str)
        else:
            return (True, None)
    elif syn_code == 'R':
        count = 0
        for s in syn_idx:
            if len(seg_data) >= s and seg_data.get_value('%02i' % (s)) != '':
                count += 1
        if count == 0:
            err_str = 'Syntax Error (%s): At least one element is required' % \
                (syntax_str(syn))
            return (False, err_str)
        else:
            return (True, None)
    elif syn_code == 'E':
        count = 0
        for s in syn_idx:
            if len(seg_data) >= s and seg_data.get_value('%02i' % (s)) != '':
                count += 1
        if count > 1:
            err_str = 'Syntax Error (%s): At most one of %s may be present'\
                % (syntax_str(syn), syntax_ele_id_str(seg_data.get_seg_id(), syn_idx))
            return (False, err_str)
        else:
            return (True, None)
    elif syn_code == 'C':
        # If the first is present, then all others are required
        if len(seg_data) >= syn_idx[0] and seg_data.get_value('%02i' % (syn_idx[0])) != '':
            count = 0
            for s in syn_idx[1:]:
                if len(seg_data) >= s and seg_data.get_value('%02i' % (s)) != '':
                    count += 1
            if count != len(syn_idx) - 1:
                if len(syn_idx[1:]) > 1: verb = 'are'
                else:
                    verb = 'is'
                err_str = 'Syntax Error (%s): If %s%02i is present, then %s %s required'\
                    % (syntax_str(syn), seg_data.get_seg_id(), syn_idx[0],
                       syntax_ele_id_str(seg_data.get_seg_id(), syn_idx[1:]), verb)
                return (False, err_str)
            else:
                return (True, None)
        else:
            return (True, None)
    elif syn_code == 'L':
        if len(seg_data) > syn_idx[0] - 1 and seg_data.get_value('%02i' % (syn_idx[0])) != '':
            count = 0
            for s in syn_idx[1:]:
                if len(seg_data) >= s and seg_data.get_value('%02i' % (s)) != '':
                    count += 1
            if count == 0:
                err_str = 'Syntax Error (%s): If %s%02i is present, then at least one of '\
                    % (syntax_str(syn), seg_data.get_seg_id(), syn_idx[0])
                err_str += syntax_ele_id_str(
                    seg_data.get_seg_id(), syn_idx[1:])
                err_str += ' is required'
                return (False, err_str)
            else:
                return (True, None)
        else:
            return (True, None)
    #raise EngineError
    return (False, 'Syntax Type %s Not Found' % (syntax_str(syn)))


def syntax_str(syntax):
    """
    @rtype: string
    """
    output = syntax[0]
    for i in syntax[1:]:
        output += '%02i' % (i)
    return output


def syntax_ele_id_str(seg_id, ele_pos_list):
    """
    @rtype: string
    """
    output = ''
    output += '%s%02i' % (seg_id, ele_pos_list[0])
    for i in range(len(ele_pos_list) - 1):
        if i == len(ele_pos_list) - 2:
            output += ' or %s%02i' % (seg_id, ele_pos_list[i + 1])
        else:
            output += ', %s%02i' % (seg_id, ele_pos_list[i + 1])
    return output
