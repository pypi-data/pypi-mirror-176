call compileobj.bat

mkdir ..\lib\libspline
g++ -lm -fPIC -std=c++17 -Wextra -shared -o ..\lib\libspline\libspline.so ..\build\*.o

