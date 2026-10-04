CXX = g++
CXXFLAGS = -Wall -O2
LIBS = -lgmp

all: cca_attack

cca_attack: src/cca_attack.cpp
	$(CXX) $(CXXFLAGS) $< -o $@ $(LIBS)

clean:
	rm -f cca_attack

.PHONY: all clean
