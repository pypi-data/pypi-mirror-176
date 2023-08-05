# CFLAGS for CC
CFLAGS=-lm -std=c++17 -Wextra -O3

# Compiler
CCo=g++ -fPIC -c $(CFLAGS)
CC=g++ -fPIC $(CFLAGS)
CCWo=x86_64-w64-mingw32-g++-win32 -c $(CFLAGS)
CCW=x86_64-w64-mingw32-g++-win32 $(CFLAGS)

ifndef BUILDDIR 
	BUILDDIR=../build
endif

all: obj lib

obj:
	$(CCo) spline.cc -o $(BUILDDIR)/spline.o
	$(CCo) libspline.cc -o $(BUILDDIR)/libspline.o

winobj:
	$(CCWo) spline.cc -o $(BUILDDIR)/spline.o
	$(CCWo) libspline.cc -o $(BUILDDIR)/libspline.o

lib: 
	$(CC) -shared -o ../lib/libspline/libspline.so $(BUILDDIR)/*.o
	
winlib: 
	$(CCW) -shared -o ../lib/libspline/libspline.dll $(BUILDDIR)/*.o
	