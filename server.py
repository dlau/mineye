from os import listdir
from os.path import isfile, join
import traceback
import json
import uuid
import re
import tempfile
from flask import Flask, request
import wand.image
import wand.display
import wand.exceptions
app = Flask(__name__)

#local stuff
from img import persisted_img
im = persisted_img()

BANK_PATH = 'static/img/bank'
BANK_THUMB_PATH = join(BANK_PATH,'thumb')
print 'USING BANK PATH ' + BANK_PATH
print 'USING THUMB PATH ' + BANK_THUMB_PATH

def get_images(path):
    #this isn't very robust, oh well
    return filter(
        lambda x : re.search('\.(jpg|jpeg|png)', x.lower()) != None,
        [join(path, f) for f in listdir(path) if isfile(join(path,f))]
    )

def get_bank_images():
    return get_images(BANK_PATH)

def get_thumb_images():
    return get_images(BANK_THUMB_PATH)

@app.route("/")
def index():
    return '''
        <html>
            <head>
            </head>
            <body>
              <div id="content"></div>
              <script type="text/javascript" src="/static/js/all.js"></script>
            </body>
        </html>
        '''

@app.route('/similar', methods=['POST'])
def similar():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            tmpfile = join(
                tempfile.gettempdir(),
                file.name
            )
            file.save(tmpfile)
            #lol shitty
            try:
                with wand.image.Image(filename=tmpfile) as img:
                    img.resize(256, 256)
                    img.save(filename=tmpfile)
                matches = im.match(tmpfile, limit=10)
                return json.dumps(matches)
            except:
                traceback.print_exc()
                pass
    return '', 400

@app.route('/bank', methods=['GET', 'POST'])
def bank():
    if request.method == 'POST':
        file = request.files['file']
        print file
        if file:
            tmpfile = join(
                tempfile.gettempdir(),
                file.name
            )
            guid = str(uuid.uuid4().get_hex().upper()[0:12]) + '.jpg'
            dstfile = join(
                BANK_PATH,
                guid
            )
            dstfile_thumb = join(
                BANK_THUMB_PATH,
                guid
            )
            file.save(tmpfile)
            try:
                with wand.image.Image(filename=tmpfile) as img:
                    img.save(filename=dstfile)
                    #will potentially produce some funny results with extremely wide/oblong images
                    img.resize(256, 256)
                    img.save(filename=dstfile_thumb)
                    im.add_image(dstfile_thumb)
            except wand.exceptions.MissingDelegateError:
                return 'input is not a valid image', 500
            return '', 200

    elif request.method == 'GET':
        limit = 10
        try:
            limit = int(request.args.get('limit', '10'))
        except ValueError:
            pass
        #note, will spit back any non dir
        files = get_bank_images()
        return json.dumps(['/'+f for f in files[0:limit]])
    return '', 400
if __name__ == "__main__":
    #todo: toggle debug from config
    app.debug = True
    app.run()
