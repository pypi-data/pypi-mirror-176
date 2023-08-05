mkdir ..\build
g++ -c -lm -fPIC -std=c++17 -Wextra spline.cc -o ..\build\spline.o
g++ -c -lm -fPIC -std=c++17 -Wextra libspline.cc -o ..\build\libspline.o
	
