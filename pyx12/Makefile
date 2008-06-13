CC = g++
CFLAGS=-Wall  # c++ compiler flags
#LDFLAGS=-Wall   # linker flags
LDFLAGS = -lm -Wall
#-I /usr/local/include -L /usr/local/lib 
#DOCTARGET = ../doc/epydoc
DOCTARGET = ../../pyx12-web/doc/epydoc

all:
	test_csegment

test_csegment: test_csegment.cxx
	$(CC) $(CXXFLAGS) $(LDFLAGS) -o test_csegment test_csegment.cxx

segment.o: segment.cxx segment.hxx errors.hxx
	$(CC) $(CXXFLAGS) -c segment.cxx

errors.o: errors.cxx errors.hxx
	$(CC) $(CXXFLAGS) -c errors.cxx

#test:       all
#    ./greet <../data/name1
#    ./frame <../data/name2

test1.o: test1.cxx segment.hxx
	$(CC) $(CXXFLAGS) -c test1.cxx

clean:
	rm -f *.o *.core

doc:
	epydoc -v --check --html --name Pyx12 --exclude=tests -u http://pyx12.sourceforge.net/ --no-frames -o $(DOCTARGET) .
