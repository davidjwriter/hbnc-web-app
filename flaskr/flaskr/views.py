from flaskr import *
from flaskr.lib import *
from flaskr.model import *

#Current App Workings
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/uploadPics')
def uploadPics():
    return render_template('uploadPics.html')

@app.route('/checkin')
def checkin():
    return redirect(url_for('landing'))

@app.route('/uploadDocs')
def uploadDocs():
    return render_template('uploadDocs.html')

@app.route('/uploadDocsToFolder', methods=['POST'])
def uploadDocsToFolder():
    orderNum = request.form.get('orderNum')
    docs = request.files.getlist('docs')
    orderDir = os.path.join(app.config['PICS']) + "/" + str(orderNum)
    docDir = os.path.join(app.config['PICS']) + "/" + str(orderNum) + "/documents"
    mode = 0o777
    supermakedirs(orderDir, mode)
    supermakedirs(docDir, mode)
    counter = 0
    beforeName = orderNum + "_before_" + str(counter)
    for f in docs:
        counter += 1
        beforeName = orderNum + "_before_" + str(counter)
        #f.filename = createFileName(beforeName, f.filename.split(".")[len(f.filename.split(".")) - 1])
        f.save(os.path.join(docDir, f.filename))
    flash("Thanks for uploading these documents!")
    return redirect(url_for('landing'))



@app.route('/uploadPicsToFolder', methods=['POST'])
def uploadPicsToFolder():
    #First lets get all the before pictures
    beforePics = request.files.getlist('before')
    extraDict = request.files

    #Go through extra files to get any extra files added
    counter = 0
    name = "before_" + str(counter)
    fileVal = extraDict.get(name)
    while (fileVal is not None):
        beforePics.append(fileVal)
        counter += 1
        name = "before_" + str(counter)
        fileVal = extraDict.get(name)

    #Now we can get all the after pictures
    afterPics = request.files.getlist('after')
    extraDict = request.files
    #Go through extra files to get any extra files added
    counter = 0
    name = "after" + str(counter)
    fileVal = extraDict.get(name)
    while (fileVal is not None):
        afterPics.append(fileVal)
        counter += 1
        name = "after_" + str(counter)
        fileVal = extraDict.get(name)

    orderNum = request.form.get('orderNum')
    flash("Thanks for Uploading Pics!")
    #cleanPics()
    #NOTE: We never clean out pics and only have 20gb of storage
    #I think whenever we implement google drive transfer we will delete
    #Pics from server storage
    orderDir = os.path.join(app.config['PICS']) + "/" + str(orderNum)
    beforeDir = os.path.join(app.config['PICS']) + "/" + str(orderNum) + "/before"
    afterDir = os.path.join(app.config['PICS']) + "/" + str(orderNum) + "/after"
    mode = 0o777
    supermakedirs(orderDir, mode)
    supermakedirs(beforeDir, mode)
    supermakedirs(afterDir, mode)
    counter = 0
    beforeName = orderNum + "_before_" + str(counter)
    for f in beforePics:
        counter += 1
        beforeName = orderNum + "_before_" + str(counter)
        f.filename = createFileName(beforeName, f.filename.split(".")[len(f.filename.split(".")) - 1])
        f.save(os.path.join(beforeDir, f.filename))
        #f.save(beforeDir, f.filename)
    counter = 0
    afterName = orderNum + "_after_" + str(counter)
    for f in afterPics:
        counter += 1
        afterName = orderNum + "_after_" + str(counter)
        f.filename = createFileName(afterName, f.filename.split(".")[len(f.filename.split(".")) - 1])
        f.save(os.path.join(afterDir, f.filename))
        #f.save(beforeDir, f.filename)
    resize(str(orderNum))
    return redirect(url_for('landing'))

#Old App Workings
#Left in for now just for references
@app.route('/addRecipe')
def addRecipe():
    ingredients = db.session.query(Item).all()
    return render_template('addRecipe.html', ingredients=ingredients)

@app.route('/createRecipe', methods=['POST'])
def createRecipe():
    name = request.form.get('name')
    pic = request.files.getlist('picture')
    items = request.form.getlist('items')
    itemArr = []
    for item in items:
        if (item is not ""):
            itemArr.append(item)
    print("Name: ", name)
    for f in pic:
        f.filename = createFileName(name, f.filename.split(".")[len(f.filename.split(".")) - 1])
        f.save(os.path.join(app.config['PICS'], f.filename))
        print("File: ", f)
    for i in items:
        print("Item: ", i)
    return render_template('editRecipe.html', measurements=app.config['MEASUREMENTS'], types=app.config['TYPES'], name=name, pic=pic[0].filename, items=itemArr)

@app.route('/editRecipe')
def editRecipe():
    recipes = db.session.query(Recipe).all()
    return render_template("editRecipes.html", recipes=recipes)

@app.route('/deleteRecipes', methods=['POST'])
def deleteRecipes():
    recipes = request.form.getlist('recipe')
    for ide in recipes:
        recipe = db.session.query(Recipe).filter_by(id = ide).delete()
    db.session.commit()
    flash("Recipe Successfully Deleted")
    return redirect(url_for('landing'))

@app.route('/changeRecipe/<recipeID>')
def changeRecipe(recipeID):
    recipe = db.session.query(Recipe).filter_by(id = recipeID).first()
    items = recipe.listOfItems
    itemList = []
    for item in items.split(","):
        if (item is not "" and item is not None):
            itemList.append(db.session.query(Item).filter_by(id = item).first())
    return render_template('changeRecipe.html', measurements=app.config['MEASUREMENTS'], types=app.config['TYPES'], recipe=recipe, items=itemList, pic=getFileName(recipe.name))

@app.route('/add/<name>', methods=['POST'])
def addRecipeToDB(name):
    items = request.form.getlist('items')
    itemsArr = []
    itemIDs = []
    for item in items:
        itemsArr.append((str(item),
                        request.form.get(str(item) + 'q'),
                        request.form.get(str(item) + 'm'),
                        request.form.get(str(item) + 't')));
    for tup in itemsArr:
        if (not isItem(tup)):
            itemIDs.append(createItem(tup))
        else:
            ingredient = db.session.query(Item).filter_by(name = tup[0], quantity = tup[1], measurement = tup[2], type = tup[3]).all()
            itemIDs.append(ingredient[0].id)
    recipeName = name.split("/")[len(name.split("/")) - 1].split(".")[0]
    listOfItems = ""
    for ide in itemIDs:
        if (listOfItems == ""):
            listOfItems = str(ide)
        else:
            listOfItems = listOfItems + " ," + str(ide)
    newRecipe = Recipe(name = recipeName, listOfItems = listOfItems, file = getFileName(name))
    db.session.add(newRecipe)
    db.session.commit()
    return redirect(url_for('landing'))

@app.route('/startShopping')
def startShoppingList():
    recipes = db.session.query(Recipe).all()
    return render_template("startShoppingList.html", recipes=recipes)

@app.route('/createList', methods=['POST'])
def createShoppingList():
    recipes = request.form.getlist('recipe')
    recipeList = {}
    for ide in recipes:
        recipe = db.session.query(Recipe).filter_by(id = ide).first()
        recipeName = recipe.name
        recipeFile = recipe.file
        for itemID in recipe.listOfItems.split(","):
            item = db.session.query(Item).filter_by(id = itemID).first()
            try:
                recipeList[item.type].append(item)
            except:
                recipeList[item.type] = [item]
    recipeList = reduceList(recipeList)
    app.config['CURR_RECIPE'] = recipeList
    return render_template('generateList.html', recipeList=recipeList)

@app.route('/finalize', methods=['POST'])
def finalizeShoppingList():
    currList = app.config['CURR_RECIPE']
    for itemType in currList:
        delItems = request.form.getlist(itemType)
        for itemID in delItems:
            for i in currList[itemType]:
                if (i.id == int(itemID)):
                    currList[itemType].remove(i)
    app.config['CURR_RECIPE'] = currList
    return render_template('shoppingList.html', recipeList=currList)

@app.route('/updateRecipe/<recipeID>', methods=['POST'])
def updateRecipe(recipeID):
    itemsArr = []
    itemIDs = []
    recipe = db.session.query(Recipe).filter_by(id = recipeID).first()
    items = recipe.listOfItems
    for itemID in items.split(","):
        item = db.session.query(Item).filter_by(id = itemID).first()
        print(item.name, request.form.get(str(item.name) + 'q'), request.form.get(item.name + 'm'), request.form.get(item.name + 't'))
        itemsArr.append((str(item.name),
                        request.form.get(str(item.name) + 'q'),
                        request.form.get(str(item.name) + 'm'),
                        request.form.get(str(item.name) + 't')));
    for tup in itemsArr:
        if (not isItem(tup)):
            itemIDs.append(createItem(tup))
        else:
            ingredient = db.session.query(Item).filter_by(name = tup[0], quantity = tup[1], measurement = tup[2], type = tup[3]).all()
            itemIDs.append(ingredient[0].id)
    listOfItems = ""
    for ide in itemIDs:
        if (listOfItems == ""):
            listOfItems = str(ide)
        else:
            listOfItems = listOfItems + " ," + str(ide)
    recipe.listOfItems = listOfItems
    db.session.commit()
    return redirect(url_for('landing'))

@app.route('/download')
def downloadList():
    recipeList = app.config['CURR_RECIPE']
    newFile = os.path.join(app.config['DOCS'], 'shoppingList.txt')
    output = open(newFile, 'w')
    for t in recipeList:
        output.write("\t" + str(t).upper())
        output.write("\n\n")
        for item in recipeList[t]:
            output.write("   * " + str(item.name) + " " + str(item.quantity) + " " + str(item.measurement))
            output.write("\n")
        output.write("==========================================================================")
    output.close()
    retFile = 'documents/' + 'shoppingList.txt'
    return send_file(retFile, as_attachment=True, mimetype='text/plain')
