import libxml2
import errors

NodeType = {'element_start': 1, 'element_end': 15, 'attrib': 2, 'text': 3, 'CData': 4, 'entity_ref': 5, 'entity_decl':6, 'pi': 7, 'comment': 8, 'doc': 9, 'dtd': 10, 'doc_frag': 11, 'notation': 12}

"""
    if not self.map_file:
        raise errors.GSError, 'Map file not found, icvn=%s, fic=%s, vriic=%s' % (isa.icvn,self.fic,self.vriic)
"""

class map_index:
    def __init__(self, map_file):
        self.maps = []
        try:
            reader = libxml2.newTextReaderFilename(map_file)
        except:
            raise errors.EngineError, 'Map file not found: %s' % (map_file)
                    
        while reader.Read():
            #processNode(reader)
            if reader.NodeType() == NodeType['element_start'] and reader.Name() == 'version':
             while reader.MoveToNextAttribute():
                    if reader.Name() == 'icvn':
                        icvn = reader.Value()

            if reader.NodeType() == NodeType['element_end'] and reader.Name() == 'version':
                icvn = None

            if reader.NodeType() == NodeType['element_start'] and reader.Name() == 'map':
                file_name = ''
                while reader.MoveToNextAttribute():
                    if reader.Name() == 'vriic':
                        vriic = reader.Value()
                    elif reader.Name() == 'fic':
                        fic = reader.Value()

            if reader.NodeType() == NodeType['element_end'] and reader.Name() == 'map':
                self.maps.append((icvn, vriic, fic, file_name))
                vriic = None
                fic = None
                file_name = None

            if reader.NodeType() == NodeType['text']:
                file_name = reader.Value()

    
    def add_map(self, icvn, vriic, fic, map_file):
        self.maps.append((icvn, vriic, fic, map_file))
        #self.icvn = icvn
        #self.vriic = vriic
        #self.fic = fic
        #self.map_file = map_file
    
    def get_filename(self, icvn, vriic, fic):
        #print 'get_filename', icvn, vriic, fic
        for a in self.maps:
            if a[0] == icvn and a[1] == vriic and a[2] == fic:
                return a[3]
        return None

    def print_all(self):
        for a in self.maps:
            print a[0], a[1], a[2], a[3]

