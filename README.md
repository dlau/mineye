#Overview
Very simply, this project demonstrates how to match an image to a bank of pre-existing images.

It contains a simple front-end and API


#How it works
To add an image to the bank:
- Compute SURF descriptors for the image
- Concatenate the descriptor to a "mega matrix" of pre-existing ones, making note of it's position.

To look up an image:
- Compute SURF descriptors for the image
- Perform a knn search in the "mega matrix" for the SURF descriptors found above
- For all matches, if the two are within a certain distance threshold, we increment a similary value with respect to that candidate by 1. This creates an arbitrary similarity index.
- Return the top results

The server is implemented using flask (todo: link) and the front end uses react (todo: link)


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

#Optimization:
- The implementation is poorly optimized, there is a rudimentary attempt to distribute the "mega matrix" to take advantage of multiple cores. At any sort of scale, you probably want to look into doing some sort of distributed nearest neighbor search.

- By default the server persists the bank data in `bank.db` which is a simple sqlite database with pickled python objects. This is merely for convenience between server restarts. While it is running, the server keeps everything in local memory.

#Closing:
- Tested with around 200k without issues.


This is only tested on OS X Mavericks, it shouldn't have any problems on linux. It is completely untested on windows.

#Inputting test data
Grab any dataset, such as:

[http://www.vision.caltech.edu/Image_Datasets/Caltech256/](http://www.vision.caltech.edu/Image_Datasets/Caltech256/)

untar it and just POST them all to the server
`find <MY_DATASET_DIR> -name "*.<IMAGE_EXTENSION>" -exec curl -i -F file=@{} \;`


#LICENSE
**mineye** source code is released under the **MIT License**

The **SURF and SIFT algorithms implemented by OpenCV are patented** You will have to switch out the feature detector for something else.
