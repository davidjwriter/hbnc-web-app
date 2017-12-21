from flaskr import *
from flaskr.model import *


#Cleans out picture folders for new uploads
def cleanPics():
    for directory in os.listdir(os.path.join(app.config['PICS'])):
        try:
            shutil.rmtree(os.path.join(app.config['PICS'],directory))
        except:
            try:
                os.remove(os.path.join(app.config['PICS'],directory))
            except:
                print("Could Remove File or Directory")

#Creates a given directory with correct permissions
def supermakedirs(path, mode):
    if not os.path.exists(path):
        os.mkdir(path)
        os.chmod(path, mode)

#Resizes an image file to be between 100kb and 300kb
def resize(orderNum):
    beforePath = os.path.join(app.config['PICS'], orderNum + "/before")
    afterPath = os.path.join(app.config['PICS'], orderNum + "/after")
    resizePath(beforePath)
    resizePath(afterPath)

#Resize helper method to resize a given path
def resizePath(beforePath):
    for img in os.listdir(beforePath):
        try:
            counter = 0
            while (os.stat(os.path.join(beforePath, img)).st_size > app.config['MAX_SIZE']):
                with open(os.path.join(beforePath, img), 'r+b') as f:
                    with Image.open(f) as image:
                        width, height = image.size
                        ratio = getRatio(width, height, counter)
                        counter += 1
                        cover = resizeimage.resize_cover(image, ratio)
                        cover.save(os.path.join(beforePath, img), image.format)
        except:
            print("Cannot Resize Image")
#With the photos width and height this will calculate the proper dimensions
#For resizing the image
def getRatio(width, height, recur):
    if (recur == 0):
        return [width, height]
    recur += 1
    return [width / recur, height / recur]


#Checks if a given item is already in the database
def isItem(itemTuple):
    nm = itemTuple[0]
    quant = itemTuple[1]
    meas = itemTuple[2]
    typ = itemTuple[3]
    ingredient = db.session.query(Item).filter_by(name = nm, quantity = quant, measurement = meas, type = typ).all()
    if (len(ingredient) > 0):
        return True
    return False

#Creates a new Item; takes in a tuple and creates the item in the database
#Format of the tuple: (itemName, item quantity, item measurement, item type)
def createItem(itemTuple):
    name = itemTuple[0]
    quant = itemTuple[1]
    meas = itemTuple[2]
    typ = itemTuple[3]
    newItem = Item(type=typ, name=name, quantity=quant, measurement=meas)
    db.session.add(newItem)
    db.session.commit()
    return newItem.id

#Creates a filename given a file's name. This will query the database and make sure we don't have duplicates
def createFileName(name, ext):
    listofnames = db.session.query(Recipe).filter_by(name = name).all()
    counter = 0
    currName = name
    while (len(listofnames) > 0):
        currName = str(name) + str(counter)
        counter += 1
        listOfItems = db.session.query(Recipe).filter(name = currName).all()
    filename = currName + "." + str(ext)
    filename = filename.replace(" ", "-")
    return filename

#Gets the filename of a given recipe name
def getFileName(name):
    listOfPics = os.listdir(app.config['PICS'])
    for pic in listOfPics:
        if (name.replace(" ", "-") in pic):
            return pic

#Reduces the recipe list by combining same items
def reduceList(recipeList):
    for itemType in recipeList:
        delList = []
        for i in range(len(recipeList[itemType])):
            for j in range(len(recipeList[itemType])):
                if (i != j):
                    iItem = recipeList[itemType][i]
                    jItem = recipeList[itemType][j]
                    if (iItem.name == jItem.name and iItem.measurement == jItem.measurement and iItem not in delList and jItem not in delList):
                        jItem.quantity = jItem.quantity + iItem.quantity
                        delList.append(iItem)
        for index in delList:
            recipeList[itemType].remove(index)
    return recipeList
