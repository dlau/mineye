import cv2
import numpy
import sqlite3
import pickle
from datetime import datetime


#max number of images in each matrix, for parallel processing
DESC_MAX_LEN = 100000
#sqlite db for persistence
BANK_FILENAME = 'bank.db'

'''
note the licensing issues with using SURF/SIFT, alternatives are FREAK, BRISK for
feature detection
'''
def get_surf_des(filename):
    f = cv2.imread(filename)
    #hessian threshold 800, 64 not 128
    surf = cv2.SURF(800, extended=False)
    kp, des = surf.detectAndCompute(f, None)
    return kp, des

def get_conn():
    return sqlite3.connect('bank.db')

class _img:
    def __init__(self):
        self.imap = []
        self.r = 0
        self.descs = []
        index_params = dict(algorithm=1,trees=4)
        self.flann = cv2.FlannBasedMatcher(index_params,dict())

    def add_image(self, filename, des=None):
        if des == None:
            kv, des = get_surf_des(filename)
        self.imap.append({
            'index_start' : self.r,
            'index_end' : self.r + des.shape[0] - 1,
            'file_name' : filename
        })
        self.r += des.shape[0]
        #it's really slow to do a vstack every time, so just maintain a list and
        #replicate it as a concatenated numpy ndarray every time. an optimization
        #would be to do a numpy.vstack((self.descs, numpy,array(des))) where self.descs
        #is a numpy.array
        self.descs.append(des)

    def match(self, filename, limit=20):
        kp, to_match = get_surf_des(filename)
        img_db = numpy.vstack(numpy.array(self.descs))
        #this should be reversed, need to update distance calculation
        matches = self.flann.knnMatch(img_db, to_match, k=4)
        sim = dict()
        for img in self.imap:
            sim[img['file_name']] = 0
        for i in xrange(0, len(matches)):
            match = matches[i]
            if match[0].distance < (.6 * match[1].distance):
                for img in self.imap:
                    if img['index_start'] <= i and img['index_end'] >= i:
                        sim[img['file_name']] += 1
        return sim

    def __len__(self):
        return len(self.descs)

class img:
    def __init__(self):
        self.ims = [_img()]
        self.count = 0

    def get_count(self):
        return self.count

    def add_image(self, filename, des=None):
        self.count += 1
        self.ims[-1].add_image(filename, des=des)
        if len(self.ims[-1]) > DESC_MAX_LEN:
            self.ims.append(_img())

    def match(self, filename, limit=20):
        import multiprocessing.dummy
        p = multiprocessing.dummy.Pool(10)

        def f(instance):
            return instance.match(filename, limit=limit)

        res = p.map(f, [i for i in self.ims])
        sim = dict((k,v) for d in res for (k,v) in d.items())
        sorted_sim = sorted(sim.items(), key=lambda x:x[1], reverse=True)[0:limit]
        sorted_sim = [{'image' : x[0], 'similarity' : x[1]} for x in sorted_sim]
        sorted_sim = filter(lambda x:x['similarity'] > 5, sorted_sim)
        return sorted_sim

class persisted_img(img):
    def __init__(self):
        #optimization, should additionally wrap img once more instead, so it works without persistence
        img.__init__(self)
        with get_conn() as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS descs
                        (filename, des,kp)
                        ''')
            conn.commit()
            c.execute(
                '''
                SELECT filename,des
                FROM descs
            ''')
            while True:
                row = c.fetchone()
                if not row:
                    break
                filename = row[0]
                des = pickle.loads(str(row[1]))
                print 'img.__init__: loading descriptor for file %s from db' % (filename)
                if des == None:
                    print 'img.__init__: error loading descriptor for %s from db' % (filename)
                    continue
                self.add_image(filename, des=des)

    def add_image(self, filename, des=None):
        if des == None:
            kv, des = get_surf_des(filename)
            with get_conn() as conn:
                c = conn.cursor()
                data = sqlite3.Binary(pickle.dumps(des, pickle.HIGHEST_PROTOCOL))
                c.execute('''
                    INSERT INTO descs(filename, des) VALUES (?,:data)
                    ''',
                    [filename, data]
                )
                print 'INSERT  %s to db' % (filename)
                conn.commit()
        img.add_image(self, filename, des=des)


