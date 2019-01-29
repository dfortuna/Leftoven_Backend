import os
import shutil
import uuid
from pathlib2 import Path
from flask import Flask, request
from flask_restful import Api
from flask_uploads import UploadSet, configure_uploads, IMAGES
import json

from classifier.image_classifier import ImageClassifier
from models.ingredients_db import Ingredient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dante'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

ingredientName = ""
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'temp/'
configure_uploads(app, photos)

classifier = ImageClassifier()

@app.route('/IngredientToCheck', methods=['POST'])
def uploadFile():
    if 'photos' in request.files:
        ingredient_pic = request.files['photos']
        (label, odds) = classifier.classifier(ingredient_pic)
        if odds < 50.0:
            photos.save(ingredient_pic)
            filename = ingredient_pic.filename
            return filename, 404
        else:
            return label, 200

def teste():
    aaa=1

@app.route('/InformIngredientName', methods=['POST'])
def postName():
    json_data = request.get_json()
    filename = json_data["filename"]
    label = json_data["label"]
    (ingredientName, fileExtension) = os.path.splitext(filename) #separate name and extension
    dataset_directory = 'dataset/{}/'.format(label) #format destination directory PATH
    Path(dataset_directory).mkdir(parents=True, exist_ok=True) #create destination directory from PATH
    uniqueFileName = str(uuid.uuid4())+fileExtension
    os.rename('temp/'+filename, 'temp/'+uniqueFileName) #rename file to a unique name
    shutil.move('temp/'+uniqueFileName, dataset_directory) #move file from /temp to destination directory

    dataset_ingredient_count = len(os.listdir(dataset_directory))
    if dataset_ingredient_count >= 1:
        #if ingredient has 100 unrecognized pics, train classifier..
        msg = classifier.train_classifier(dataset_directory)
        if msg == 200:
            #if classifier returns 200 add 1 to ingredient_classifier_trained in Ingredient table if exists
            #otherwise insert label and ingredient_classifier_trained == 1
            exists = Ingredient.select_ingredient_name(label) # exists is 'None' if not found
            if exists:
                Ingredient.update_classifier_trained(label)
            else:
                ingredient = Ingredient(ingredient_label=label, classifier_trained=1)
                ingredient.insert() #update Ingredient table with trained ingredient
            shutil.rmtree(dataset_directory) # delete pics used by classifier
    return 'good job', 200

@app.route('/getIngredients', methods=['GET'])
def getSupportedIngredients():
    ingredient_list = Ingredient.select_by_classifier_trained(1)
    if ingredient_list:
        return json.dumps(ingredient_list)
    return {'message': 'Not found'}, 404


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
