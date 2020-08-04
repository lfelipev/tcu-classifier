from flask import Flask, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
import joblib
import numpy as np
from nltk.corpus import stopwords
import nltk
import json
import stanza
import pandas as pd 
from nltk.probability import FreqDist
pd.set_option("display.max_colwidth", 200) 
import numpy as np 
import re 
import spacy 
import gensim 
from gensim import corpora
import pyLDAvis 
import pyLDAvis.gensim 
import matplotlib.pyplot as plt 
import seaborn as sns
from os.path import isfile, join
from os import listdir
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.preprocessing import normalize

flask_app = Flask(__name__)

app = Api(app = flask_app, 
		  version = "2.0", 
		  title = "Classificador de Assuntos de Acórdãos do TCU", 
		  description = "Prediz o assunto de acórdãos do TCU")

name_space = app.namespace('prediction', description='Prediction APIs')

model = app.model('Prediction params', 
				  {'sepalLength': fields.Float(required = True, 
				  							   description="Sepal Length", 
    					  				 	   help="Sepal Length cannot be blank"),
				  'sepalWidth': fields.Float(required = True, 
				  							   description="Sepal Width", 
    					  				 	   help="Sepal Width cannot be blank"),
				  'petalLength': fields.Float(required = True, 
				  							description="Petal Length", 
    					  				 	help="Petal Length cannot be blank"),
				  'petalWidth': fields.Float(required = True, 
				  							description="Petal Width", 
    					  				 	help="Petal Width cannot be blank")})

classifier = joblib.load('classifier.joblib')
df = joblib.load('df.jolib')
tf_idf_array = joblib.load('tf_idf_array.joblib')
textos = joblib.load('data.joblib')

@name_space.route("/")
class MainClass(Resource):

	def remove_stopwords(self, rev, stop_words):
		rev_new = " ".join([i for i in rev if i not in stop_words])
		return rev_new

	def process_text(self, texto):
		cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
		texto = re.sub(cleanr, '', texto)
		texto = re.sub('[^A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]', '', texto)

		nltk.download('stopwords') 
		stop_words = stopwords.words('portuguese')
		#stop_words.extend(['body', 'class', 'text', 'tcu', 'item', 'linha', 'table', 'contas', 'art', 'n', 'união', 'i', 'ii', 'iii'])

		texto = texto.lower()

		texto = self.remove_stopwords(texto.split(), stop_words)

		textos_temp = textos.copy()

		textos_temp.append(texto)

		tf_idf_vectorizor = TfidfVectorizer(stop_words=stop_words)
		tf_idf = tf_idf_vectorizor.fit_transform(textos_temp)
		tf_idf_norm = normalize(tf_idf)
		new_tf_idf_array = tf_idf_norm.toarray()

		if(len(new_tf_idf_array.T) == len(tf_idf_array.T)):
			return True, new_tf_idf_array[len(new_tf_idf_array) - 1]
		else:
			return False, []


	def options(self):
		response = make_response()
		response.headers.add("Access-Control-Allow-Origin", "*")
		response.headers.add('Access-Control-Allow-Headers', "*")
		response.headers.add('Access-Control-Allow-Methods', "*")
		return response

	@app.expect(model)		
	def post(self):
		try: 
			formData = request.json
			data = [val for val in formData.values()]

			numacordao = data[0]
			anoacordao = data[1]
			colegiado = data[2]
			conteudo = data[3]
			count = 0
			indice = 0

			if conteudo != '(Opcional)':
				verify, predict_input = self.process_text(conteudo)

				if(verify):
					prediction = classifier.predict([predict_input])
					types = { 0: "Resultados de Acordos", 1: "Jurisdição em geral", 2: "Irregularidade nas contas"}
					response = jsonify({
						"statusCode": 200,
						"status": "Prediction made",
						"result": "O Acórdão consultado tem grande chances de falar de: " + types[prediction[0]]
						})
					response.headers.add('Access-Control-Allow-Origin', '*')
					return response
				else:
					response = jsonify({
						"statusCode": 200,
						"status": "Could not make prediction",
						"result": "O Acórdão contém palavras que não estão presentes em nosso vocabulário :(."
						})
					response.headers.add('Access-Control-Allow-Origin', '*')
					return response
			else:
				for i in range(0, len(df)):
					if str(anoacordao) == df['ANOACORDAO'][i] and str(numacordao) == df['NUMACORDAO'][i] and colegiado == df['COLEGIADO'][i]:
						count = 1
						indice = i

				if(count == 0):
					print('Acórdão não encontrado')

				print('Predicting index: ', indice)

				if count == 1:
					count = 0

					prediction = classifier.predict([tf_idf_array[indice]])
					
					types = { 0: "Resultados de Acordos", 1: "Jurisdição em geral", 2: "Irregularidade nas contas"}
					response = jsonify({
						"statusCode": 200,
						"status": "Prediction made",
						"result": "O Acórdão consultado tem grande chances de falar de: " + types[prediction[0]]
						})
					response.headers.add('Access-Control-Allow-Origin', '*')
					return response
				else:
					response = jsonify({
						"statusCode": 200,
						"status": "Could not make prediction",
						"result": "O Acórdão consultado não existe na base."
						})
					response.headers.add('Access-Control-Allow-Origin', '*')
					return response
		except Exception as error:
			return jsonify({
				"statusCode": 500,
				"status": "Could not make prediction",
				"error": str(error)
			})