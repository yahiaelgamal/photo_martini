import sys
import os
s = os.path.abspath('.')+'/libs/pyexif'
sys.path.append(s)
import exif

keys = set(['DateTime', 'ExposureProgram', 'ShutterSpeedValue',
            'FNumber', 'FocalLength', 'ISOSpeedRatings', 'ExposureProgram',
            'Model', 'ExposureTime', 'Orientation', 'MeteringMode'])


attr = {x: {} for x in keys}


def get_all_files(path):
    """ This method returns the absolute values for all files in
    the path given (string)"""

    files = os.listdir(path)
    files = map(lambda x: os.path.join(path, x), files)

    dirs = filter(lambda x: os.path.isdir(x), files)
    files = filter(lambda x: x.endswith(('jpg', 'JPG', 'CR2')), files)

    for d in dirs:
        files += get_all_files(d)

    return files


def exif_map(files):
    for i, f in enumerate(files):
        print i, '/', len(files), f[f.index('.')+1:]
        try:
            info = exif.parse(f)
        except:
            print 'exception'

        if 'Model' in info and info['Model'] != 'Canon EOS REBEL T3i':
            continue

        for k in set(info.keys()) & keys:
            if k == 'DateTime':  # cluster by day
                value = info[k][0:10]
            else:
                value = info[k]

            if value not in attr[k]:
                attr[k][value] = 1
            else:
                attr[k][value] += 1


print(sys.argv)
photo_directory = sys.argv[1]
files = get_all_files(photo_directory)
print 'files ', len(files)
exif_map(files)

for k in attr:
    print k
    for kk in attr[k]:
        print '\t', kk, '=>', attr[k][kk]
