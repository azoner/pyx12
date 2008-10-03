#DOCTARGET = ../doc/epydoc
DOCTARGET = ../../pyx12-web/doc/epydoc

all:
	doc

doc:
	epydoc -v --check --html --name Pyx12 --exclude=tests -u http://pyx12.sourceforge.net/ --no-frames -o $(DOCTARGET) .
