# Overview
Very simply, this project demonstrates how to match an image to a bank of pre-existing images. It contains a simple front-end and image bank. The python implementation of the image bank can be easily adapted for other applications.

The image comparisons use [SURF: Speeded Up Robust Features](http://www.vision.ee.ethz.ch/~surf/eccv06.pdf) which is **scale, orientation, and to some degree affine invariant**.

A common problem in managing large numbers of images is detecting *slight* duplicates. Using a library like OpenCV which is widely available across platforms and languages is a great way to detect these duplicates.

![scale orientation invariant](http://i.imgur.com/nFASitk.gif)


# Animated description

![animation](http://i.cubeupload.com/8nVjdO.gif)


# How it works
To add an image to the bank:
- Compute SURF descriptors for the image
- Concatenate the descriptor to a "mega matrix" of pre-existing ones, making note of it's position.

To look up an image:
- Compute SURF descriptors for the image
- Perform a knn search in the "mega matrix" for the SURF descriptors found above
- For all matches, if the two are within a certain distance threshold, we increment a similary value with respect to that candidate by 1. This creates an arbitrary similarity index.
- Return the top results


The server is implemented using [flask](http://flask.pocoo.org/) and the front end uses [react](http://facebook.github.io/react/)


# Install:
## OSX
Need to install `opencv` and `imagemagick` (todo: add links)
```sh
pip install sqlite3
pip install numpy
pip install flask
pip install wand
pip install flask
npm install
```

# Development:
compile front end
`webpack`

watch for changes on front end
`webpack --watch`

run server:
`python server.py`

watch for changes on server:
uncomment this line in `server.py` `app.debug = True`
**note: this is by default on**

# Optimization:
- The implementation is poorly optimized, there is a rudimentary attempt to distribute the "mega matrix" to take advantage of multiple cores. At any sort of scale, you probably want to look into doing some sort of distributed nearest neighbor search.

- By default the server persists the bank data in `bank.db` which is a simple sqlite database with pickled python objects. This is merely for convenience between server restarts. While it is running, the server keeps everything in local memory.

# Related projects:
- [isk-daemon](https://github.com/ricardocabral/iskdaemon)

# Notes:

- Tested with around 200k images without issues.

- This is only tested on OS X Mavericks, it shouldn't have any problems on linux. It is completely untested on windows.

- [A Sample dataset](http://www.vision.caltech.edu/Image_Datasets/Caltech256/). untar it and just POST them all to the server `find <MY_DATASET_DIR> -name "*.<IMAGE_EXTENSION>" -exec curl -i -F file=@{} \;`


# LICENSE
**mineye** source code is released under the **MIT License**

The **SURF and SIFT algorithms implemented by OpenCV are patented** You will have to switch out the feature detector for something else.
