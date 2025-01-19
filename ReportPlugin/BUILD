Build Requirements
---------
Ubuntu 24.04 installed with:

build-essential, cmake, libjsoncpp-dev, uuid-dev, orthanc-dev

Build steps
--------
1. mkdir Build
2. cd Build
3. cmake .. -DALLOW_DOWNLOADS=ON -DCMAKE_BUILD_TYPE=Release
4. make

Note:
 Sometimes if you're not careful when fooling around with local
 orthanc tree builds you'll end up with SDK include files
 in /usr/local/include/orthanc- this will be picked in preference
 to where the installed and preferred SDK version is (/usr/include).
 This can lead to you building a plugin that cannot work on the
 targeted version of Orthanc. Beware!

