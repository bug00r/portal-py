include Revision

all: makeall

makeall:
	make -f Makefile$(PYTHON_VERSION)

.PHONY: clean

clean:
	make -f Makefile$(PYTHON_VERSION) clean

