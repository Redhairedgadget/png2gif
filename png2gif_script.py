import os
from os import path

SCRIPT_FOLDER = path.dirname(path.realpath(__file__))
import sys
sys.path.append(SCRIPT_FOLDER)
import imageio
import PIL
from PIL import Image



class Gif:
    def __init__(self, loop=None, duration=None, fps=None, isReversed=False, factor=None, gifName=None, imagesDir=None):
        self.editLoop = loop
        self.editDuration = duration
        self.editFps = fps
        self.isReversed = isReversed
        self.editFactor = factor
        self.editName = gifName
        self.imagesDir = imagesDir

    def generateGifFile(self):

        if (self.imagesDir):

            tempFileRadical=self.imagesDir+'\\'+'TMP'

            #['animationframa.png', 'animationframb.png', ...] "
            fileNames = sorted((fn for fn in os.listdir(self.imagesDir) if fn.endswith('.png')))
            images = []

            if (self.editFactor == None):
                self.editFactor = "100"

            for fileName in fileNames:
                self.resizeImage(tempFileRadical, self.imagesDir, fileName)

                # opening image to actually do the GIF creation
                image1 = imageio.imread(tempFileRadical+fileName)
                images.append(image1)

            if (self.isReversed):
                images.reverse()

            PathTuple = os.path.split(self.imagesDir)
            imagesDirBefore = PathTuple[0]

            ImagesAmount = str(len(images))

            if (self.editFps == None):
                self.editFps = "25"

            self.editDuration = 1/float(self.editFps)

            if (self.editName == None):
                self.editName = PathTuple[1]

            if (self.editLoop == None):
                self.editLoop = "0"

            imageio.mimwrite(imagesDirBefore+'\\'+self.editName+'.gif', images, loop=self.editLoop, fps=self.editFps, duration=self.editDuration)

            self.__cleaning(fileName, fileNames, tempFileRadical)

            self.editName = None
            self.editFps = None
            self.editLoop = None
            self.editFactor = None
            return True

        else:
            return False

    def resizeImage(self, tempFileRadical, imagesDir, fileName):
       # resizing image (directly before opening) as imageio makes it impossible

       with Image.open(self.imagesDir+'\\'+fileName) as image:
           image = Image.open(self.imagesDir+'\\'+fileName)

           ImageWidth = int(image.width*float(self.editFactor)/100)
           ImageHeight = int(image.height*float(self.editFactor)/100)

           im = image.resize((ImageWidth, ImageHeight), Image.ANTIALIAS)
           im.save(tempFileRadical+fileName)

    def __cleaning(self, fileName, fileNames, tempFileRadical):
        # cleaning up the mess
        for fileName in fileNames:
            os.remove(tempFileRadical+fileName)
