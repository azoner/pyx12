CC = g++
CFLAGS=-Wall  # c++ compiler flags
#LDFLAGS=-Wall   # linker flags
LDFLAGS = -lm -Wall
#-I /usr/local/include -L /usr/local/lib 

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

clean:
	rm -f *.o *.core
