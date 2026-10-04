CXX = g++
CXXFLAGS = -Wall -O2

all: timing_attack

timing_attack: src/timing_attack.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

clean:
	rm -f timing_attack

.PHONY: all clean
