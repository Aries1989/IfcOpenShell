mkdir build && cd build

cmake -G "NMake Makefiles" ^
 -DCMAKE_INSTALL_PREFIX="%LIBRARY_PREFIX%" ^
 -DCMAKE_BUILD_TYPE=Release ^
 -DCMAKE_PREFIX_PATH="%LIBRARY_PREFIX%" ^
 -DCMAKE_SYSTEM_PREFIX_PATH="%LIBRARY_PREFIX%" ^
 -DBOOST_LIBRARYDIR="%LIBRARY_PREFIX%\lib" ^
 -DBOOST_INCLUDEDIR="%LIBRARY_PREFIX%\include" ^
 -DOCC_INCLUDE_DIR="%LIBRARY_PREFIX%\include\oce" ^
 -DOCC_LIBRARY_DIR="%LIBRARY_PREFIX%\lib" ^
 -DCOLLADA_SUPPORT=Off ^
 -DBUILD_EXAMPLES=Off ^
 -DBUILD_GEOMSERVER=Off ^
 -DBUILD_CONVERT=Off ^
 ../cmake
 
if errorlevel 1 exit 1

cmake --build . --target INSTALL --config Release

if errorlevel 1 exit 1
