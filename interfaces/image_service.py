import os
import shutil
import uuid
from pathlib2 import Path
from flask import Flask, request
from flask_restful import Resource
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'temp/'
configure_uploads(app, photos)


class ImagePicture(Resource):

	apppy_app = ""
	ingredientName = ""

	def post(self):
		print('*************************')
		print('##',request.files.to_dict())
		teste1 = request.files.to_dict()
		teste2 = teste1['photos']
		print(teste2)
				 
		
		
		print('*************************')
		if 'photos' in request.files:

			# --- insert classifier here ---
			# --  if classifier response is low, save to DB
			# --  _filename will be == to the json response

			_filename = request.files['photos'].filename      #extract filename with extension
			(ingredientName, fileExtension) = os.path.splitext(_filename) #separate name and extension
			dataset_directory = 'dataset/{}/'.format(ingredientName) #format destination directory PATH
			photos.save(request.files['photos'])              # save to the temp directory
			Path(dataset_directory).mkdir(parents=True, exist_ok=True) #create destination directory from PATH
			uniqueFileName = str(uuid.uuid4())+fileExtension 
			os.rename('temp/'+_filename, 'temp/'+uniqueFileName)  #rename file to a unique name
			shutil.move('temp/'+uniqueFileName, dataset_directory) #move file from /temp to destination dataset_directory

			return "sucess", 200
		return "invalid option", 500