# A simple JSON Generator Based off of the XML Writer in pyx12.xmlwriter
import sys

"""
Tyler's Notes
loop: [
    seg: {
        ele: ...,
        ele: ...
    },
    seg: {
        ele: ...,
        ele: ...
    },
    loop: [

    ],
    ...
]

Todo: Handle commas correctly. Otherwise, almost there!
"""
class JSONriter(object):
    """
    Doctest:
        >>>from jsonwriter import JSONriter
        >>>writer = JSONriter()
        >>>#Notice: there is no error checking to ensure that the root element
        >>>#specified in the doctype matches the top-level element generated
        >>>writer.push(u"xsa")
        >>>#Another element with child elements
        >>>writer.push(u"vendor")
        >>>#Element with simple text (#PCDATA) content
        >>>writer.elem(u"name", u"Centigrade systems")
        >>>writer.elem(u"email", u"info@centigrade.bogus")
        >>>writer.elem(u"vendor", u"Centigrade systems")
        >>>#Close currently open element ("vendor)
        >>>writer.pop()
        >>>#Element with an attribute
        >>>writer.push(u"product", {u"id": u"100\\u00B0"})
        >>>writer.elem(u"name", u"100\\u00B0 Server")
        >>>writer.elem(u"version", u"1.0")
        >>>writer.elem(u"last-release", u"20030401")
        >>>#Empty element
        >>>writer.empty(u"changes")
        >>>writer.pop()
        >>>writer.pop()
    startElement
    endElement
    emptyElement
    text, data
    endDocument
    attribute
    indentation
    close
    flush
    """

    def __init__(self, out=sys.stdout, encoding="utf-8", indent=" "):
        """
        out      - a stream for the output
        encoding - an encoding used to wrap the output for unicode
        indent   - white space used for indentation
        """
        self.encoding = encoding
        self.out = out
        self.stack = []
        self.indent = indent
        # self._write("{")

    def push(self, elem, attrs={}):
        """
        Create an element which will have child elements
        """
        if elem == "comp":
            # self.stack.append(elem)
            return
        elif elem == "subele":
            import pdb;pdb.set_trace()
        self._indent()
        for (_, v) in list(attrs.items()):
            if elem == "loop":
                self._write("""{"%s": [\n""" % self._escape_attr(v))
            elif elem == "seg":
                self._write("""{"%s": {\n""" % self._escape_attr(v))
            else:
                import pdb;pdb.set_trace()
        self.stack.append(elem)

    def elem(self, elem, content, attrs={}, last=False):
        """
        Create an element with text content only
        """
        self._indent()
        for (_, v) in list(attrs.items()):
            if last:
                self._write(""""%s": "%s"\n""" % (self._escape_attr(v), self._escape_cont(content)))
            else:
                self._write(""""%s": "%s",\n""" % (self._escape_attr(v), self._escape_cont(content))) # Fix Commas
    
    def pop(self, last=False):
        """
        Close an element started with the push() method
        """
        if last:
            if len(self.stack) > 0:
                elem = self.stack[-1]
                del self.stack[-1]

                if elem == "seg":
                    self._indent()
                    self._write("}}\n")
                elif elem == "loop":
                    self._indent()
                    self._write("]}\n")
        else:
            if len(self.stack) > 0:
                elem = self.stack[-1]
                del self.stack[-1]
                if elem == "seg":
                    self._indent()
                    self._write("}},\n")
                elif elem == "loop":
                    self._indent()
                    self._write("]},\n")

    def __len__(self):
        return len(self.stack)

    def _indent(self):
        self._write(self.indent * (len(self.stack) * 2))

    def _escape_cont(self, text):
        if text is None:
            return None
        return text.replace("&", "&amp;")\
            .replace("<", "&lt;").replace(">", "&gt;")

    def _escape_attr(self, text):
        if text is None:
            return None
        return text.replace("&", "&amp;") \
            .replace("'", "&apos;").replace("<", "&lt;")\
            .replace(">", "&gt;").replace('\n', '')

    def _write(self, strval):
        self.out.write(strval)