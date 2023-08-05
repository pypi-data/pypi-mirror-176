

ifndef BUILDDIR 
	export BUILDDIR=$(shell pwd)/build
endif

ifeq ($(OS),Windows_NT)
#windows stuff here
	MD=mkdir
else
#linux and mac here
	MD=mkdir -p
endif

.PHONY: all lib obj clean header

all: obj lib header

windows: winobj winlib header

obj:
	$(MD) $(BUILDDIR)
	cd src; make obj

lib:
	$(MD) lib/libspline
	cd src; make lib

winobj:
	$(MD) $(BUILDDIR)
	cd src; make winobj

winlib: 
	$(MD) lib/libspline
	cd src; make winlib

header:
ifneq (,$(shell which python3))
	python3 generateheader.py
else
	@echo "python3 command doesn't appear to exist - skipping header regeneration..."
endif

clean:
	-rm -v lib/libspline/libspline.so
	-rm -v lib/libspline/libspline.dll
	-rmdir -v lib/libspline
	-rm -v build/*.o
	-rmdir -v build