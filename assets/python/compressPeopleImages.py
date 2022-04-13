from PIL import Image
from os import listdir, remove
from os.path import isfile, join, getsize

folderPath = "/home/runner/work/geolabWeb/geolabWeb/geolabWeb/assets/images/peopleImages"

baseWidth = 540
baseHeight = 540

for f in listdir(folderPath):
    if isfile(join(folderPath, f)):
        if 1000*1000 < getsize(join(folderPath, f)):
            personImage = Image.open(join(folderPath, f))
            curWidth, curHeight = personImage.size
            if curWidth >= curHeight:
                widthPercent = (baseWidth/float(curWidth))
                newWidth = baseWidth
                newHeight = int((float(curHeight)*float(widthPercent)))
            else:
                heightPercent = (baseHeight/float(curHeight))
                newWidth = int((float(curWidth)*float(heightPercent)))
                newHeight = baseHeight
            personImage = personImage.resize((newWidth, newHeight), Image.ANTIALIAS)
            remove(join(folderPath, f))
            personImage.save(join(folderPath, f))