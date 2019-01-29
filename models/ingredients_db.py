from db import db

class Ingredient(db.Model):
	__tablename__ = 'ingredient'
	id = db.Column(db.Integer, primary_key=True)
	ingredient_label = db.Column(db.String(80), unique=True, nullable=False)
	classifier_trained = db.Column(db.Integer,  nullable=False)

	def __repr__(self):
		return '<Ingredient %r>' % self.ingredient_label

	def __init__(self, ingredient_label, classifier_trained):
		self.ingredient_label = ingredient_label
		self.classifier_trained = classifier_trained

	# INSERT **********************************************************************************
	#creating -------> ing = Ingredient(ingredient_label='blabla', classifier_trained=0)
	#adding to db ---> db.session.add(ing)
	#                  db.session.commit
	def insert(self):
		db.session.add(self)
		db.session.commit()

	#SELECT *********************************************************************************
	#@classmethod allows the method to be called without an instance of the class
	#'cls' is the representation of the class
	#convert instance of INGREDIENT to a list that can be sent as JSON format to a GET request
	@classmethod
	def select_ingredient_name(cls, _name):
		return cls.query.filter_by(ingredient_label=_name).first()

	@classmethod
	def select_by_id(cls, _id):
		return cls.query.filter_by(id=_id).first()

	@classmethod
	def select_by_classifier_trained(cls, _classifier_trained):
		ingredients_result = cls.query.filter(Ingredient.classifier_trained>=_classifier_trained).all()
		ingredient_list = []
		for i in ingredients_result:
			ingredient = {'ingredient_label': i.ingredient_label, 'classifier_trained': i.classifier_trained}
			ingredient_list.append(ingredient)
		return {"Ingredient":ingredient_list}

	#UPDATE **********************************************************************************
	#by querying the entity, changing it and commiting, updates it
	#cls.query.filter_by(my_field_1 = 'value1').update(my_field2 = 'new_value') -> updates all objects
	@classmethod
	def update_classifier_trained(cls, name):
		#ingredient = cls.query.filter_by(ingredient_label=name).first()
		ingredient = db.session.query(Ingredient).filter_by(ingredient_label=name).first()
		number = ingredient.classifier_trained + 1
		ingredient.classifier_trained = number
		db.session.commit

	#DELETE *********************************************************************************
	@classmethod
	def delete_row(cls, row):
		db.session.delete(row)
		db.session.commit()
