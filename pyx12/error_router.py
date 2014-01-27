import logging
import error_router

class error_router(ErrorHandlerBase):
    """
    A error object - used for testing.
    Stores the current error in simple variables.
    """
    def __init__(self, targets=None):
        self.targets = []
        if targets is not None:
            self.targets.extend(targets)

    def add_target(self, target):
        self.targets.append(targets)


    #def _call_targets(self, f):
    #    for target in self.targets:
    #        try:


    def reset(self):
        """
        Clear any errors
        """
        for target in self.targets:
            target.reset()

    def get_cur_line(self):
        """
        @return: Current file line number
        @rtype: int
        """
        return self.cur_line

    def get_id(self):
        """
        @return: Error node type
        @rtype: string
        """
        return self.id

    def add_isa_loop(self, seg, src):
        """
        """
        pass
        #raise ErrorErrhNull, 'add_isa loop'

    def add_gs_loop(self, seg, src):
        """
        """
        pass

    def add_st_loop(self, seg, src):
        """
        """
        pass

    def add_seg(self, map_node, seg, seg_count, cur_line, ls_id):
        """
        """
        pass

    def add_ele(self, map_node):
        """
        """
        pass

    def isa_error(self, err_cde, err_str):
        """
        @param err_cde: ISA level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_cde = err_cde
        self.err_str = err_str

    def gs_error(self, err_cde, err_str):
        """
        @param err_cde: GS level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_cde = err_cde
        self.err_str = err_str

    def st_error(self, err_cde, err_str):
        """
        @param err_cde: Segment level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_cde = err_cde
        self.err_str = err_str

    def seg_error(self, err_cde, err_str, err_value=None, src_line=None):
        """
        @param err_cde: Segment level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_cde = err_cde
        self.err_str = err_str

    def ele_error(self, err_cde, err_str, bad_value, refdes=None):
        """
        @param err_cde: Element level error code
        @type err_cde: string
        @param err_str: Description of the error
        @type err_str: string
        """
        self.err_cde = err_cde
        self.err_str = err_str

    def close_isa_loop(self, node, seg, src):
        """
        """
        pass

    def close_gs_loop(self, node, seg, src):
        """
        """
        pass

    def close_st_loop(self, node, seg, src):
        """
        """
        pass

    def find_node(self, type):
        """
        Find the last node of a type
        """
        pass

    def get_parent(self):
        return None

#    def get_first_child(self):
#        """
#        """
#        if len(self.children) > 0:
#            return self.children[0]
#        else:
#            return None

    def get_next_sibling(self):
        """
        """
        return None

    def get_error_count(self):
        """
        """
        if self.err_cde is not None:
            return 1
        else:
            return 0

    def handle_errors(self, err_list):
        pass

    def is_closed(self):
        """
        @rtype: boolean
        """
        return True

    def __repr__(self):
        """
        """
        return '%i: %s' % (-1, self.id)
