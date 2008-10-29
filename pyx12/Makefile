#DOCTARGET = ../doc/epydoc
# See http://epydoc.sourceforge.net/manual-fields.html
DOCTARGET = ../../pyx12-web/doc/epydoc

all:
	doc

doc:
	epydoc -v --check --html --name Pyx12 --graph classtree --exclude=tests -u http://pyx12.sourceforge.net/ --no-frames -o $(DOCTARGET) .

clean:
	rm -f *.pyc *.pyo *~
