from PIL import Image
import hashlib
import time
import os
import math

iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
               'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
imageset = []

class VectorCompare:
    def magnitude(self,concordance):
        total = 0
        for word,count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    def relation(self,concordance1, concordance2):
        relevance = 0
        topvalue = 0
        for word,count in concordance1.items():
            #print(word)
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

v = VectorCompare()

def VectorGet(im):
    vector = {}
    count = 0
    for i in im.getdata():
        vector[count] = i
        count += 1
    return vector

def getLetter():
    for letter in iconset:
        for img in os.listdir('python_captcha/python_captcha/iconset/%s/' % (letter)):
            t = []
            if img != "Thumbs.db" and img != ".DS_Store":  # windows check...
                t.append(VectorGet(Image.open("python_captcha/python_captcha/iconset/%s/%s" % (letter, img))))
            imageset.append({letter: t})

def changeColor(im,image2,t):
    for x in range(im.size[1]):
        for y in range(im.size[0]):
            pix = im.getpixel((y, x))
            t[pix] = pix
            if pix == 220 or pix == 227:  # these are the numbers to get
                image2.putpixel((y, x), 0)
    return image2,t


def recordPos(image2):
    letterlist=[]
    wordin = False
    wordexist = False
    start = 0
    end = 0
    for y in range(image2.size[0]):  # slice across
        for x in range(image2.size[1]):  # slice down
            pix = image2.getpixel((y, x))
            if pix != 255:
                wordin = True

        if wordexist == False and wordin == True:
            wordexist = True
            start = y

        if wordexist == True and wordin == False:
            wordexist = False
            end = y
            letterlist.append((start, end))

        wordin = False
    return letterlist

def guessLetter(letterlist,image2):
    count = 0
    for letter in letterlist:
        m = hashlib.md5()
        image3 = image2.crop((letter[0], 0, letter[1], image2.size[1]))
        predict = []

        for image in imageset:
            for x, y in image.items():
                if len(y) != 0:
                    predict.append((v.relation(y[0], VectorGet(image3)), x))

        predict.sort(reverse=True)
        print("", predict[0])
        count += 1

def getPic():
    rootdir="./python_captcha/python_captcha/examples"
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    img=[]
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path) and path[len(path)-3:]=="gif":
              im=Image.open(path)
              img.append(im)
    return img

def main ():
    getPic()
    getLetter()
    img=getPic()
    #im = Image.open("python_captcha/python_captcha/captcha.gif")
    for im in img:
        image2 = Image.new("P", im.size, 255)
        im.convert("P")
        t = {}
        image2,t=changeColor(im,image2,t)
        letterlist=recordPos(image2)
        guessLetter(letterlist,image2)
        print("\n")


if __name__ == '__main__':
    main()
