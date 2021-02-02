# A simple JSON Generator Based off of the XML Writer in pyx12.xmlwriter
import sys


class JSONriter(object):
    """
    Doctest:
        >>>from jsonwriter import JSONriter
        >>>writer = JSONriter()
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
    """

    def __init__(self, out=sys.stdout, encoding="utf-8", indent="\t", words_mode=True):
        """
        out      - a stream for the output
        encoding - an encoding used to wrap the output for unicode
        indent   - white space used for indentation
        words_mode - boolean for using string fields rather than codes in output
        """
        self.encoding = encoding
        self.out = out
        self.stack = []
        self.indent = indent
        self.words_mode = words_mode
        self.element_count = 0

    def push(self, elem, attrs={}, first=False):
        """
        Create an element which will have child elements
        """
        if elem == "comp":
            return
        self._indent()

        if first:
            for (_, v) in list(attrs.items()):
                if elem == "loop":
                    self._write("""{"%s": [""" % self._escape_attr(v)) #newline
                elif elem == "seg":
                    self._write("""{"%s": {""" % self._escape_attr(v)) #newline
        else:
            for (_, v) in list(attrs.items()):
                if elem == "loop":
                    self._write(""",{"%s": [""" % self._escape_attr(v)) #newline
                elif elem == "seg":
                    self._write(""",{"%s": {""" % self._escape_attr(v)) #newline
        self.stack.append(elem)

    def elem(self, elem, content, attrs={}, last=False):
        """
        Create an element with text content only
        """
        self._indent()
        for (_, v) in list(attrs.items()):
            self.element_count += 1
            if last:
                self._write('''"%s": "%s"''' % (self._escape_attr(v), self._escape_cont(content))) #Newline
            else:
                self._write(""""%s": "%s",""" % (self._escape_attr(v), self._escape_cont(content))) # Newline
    
    def pop(self, last=True):
        """
        Close an element started with the push() method
        """
        if len(self.stack) > 0:
            elem = self.stack[-1]
            del self.stack[-1]
            if last:
                if elem == "seg":
                    self._indent()
                    self._write("}}") #newline
                elif elem == "loop":
                    self._indent()
                    self._write("]}") #newline
            else:
                if elem == "seg":
                    self._indent()
                    self._write("}},") #newline
                elif elem == "loop":
                    self._indent()
                    self._write("]},") #newline

    def __len__(self):
        return len(self.stack)

    def _indent(self):
        return
        # Todo : enable multi line json output
        # This gets tricky with formatting commas and indents!
        self._write(self.indent * (len(self.stack) * 2))

    def _escape_cont(self, text):
        if text is None:
            return None
        return text.replace("&", "&amp;")\
            .replace("<", "&lt;").replace(">", "&gt;").replace("\t", "")

    def _escape_attr(self, text):
        if self.words_mode:
            return text.replace(' ', '_').replace(',', '')
        if text is None:
            return None
        return text.replace("&", "&amp;") \
            .replace("'", "&apos;").replace("<", "&lt;")\
            .replace(">", "&gt;")

    def _write(self, strval):
        self.out.write(strval)