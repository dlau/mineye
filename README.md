#How it works
...todo

#Install:
##OSX
Need to install `opencv` and `imagemagick` (todo: add links)
```sh
pip install sqlite3
pip install numpy
pip install flask
pip install wand
pip install flask
npm install
```

#Development:
compile front end
`webpack`

watch for changes on front end
`webpack --watch`

run server:
`python server.py`

watch for changes on server:
todo

#A few notes
This was thrown together in an afternoon as part of a proof of concept. The memory usage is very poorly optimized. The server contains a naive parallel lookup that simply splits up the "mega matrix" up into many parts and combines the result. The take away from this code should not be the specific implementation, but the concept used to achieve the goal--namely concatenating feature vectors and performing an approximate near neighbor lookup with in input image.

I don't profess to know

This is only tested on OS X Mavericks, it shouldn't have any problems on linux. It is completely untested on windows.

#todo:
consolidate this into a tutorial

#LICENSE
**mineye** source code is released under the **MIT License**

The **SURF and SIFT algorithms implemented by OpenCV are patented** You will have to switch out the feature detector for something else.
