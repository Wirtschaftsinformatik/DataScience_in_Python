# laden benötigter Bibliotheken
# komplettes Laden der Bibliotheken
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
# laden eigener "Libraries"
import myLibrary as my
# spezifiches Laden der Teilbbliotheken
from sklearn.datasets import load_iris  # Laden eingebauten Irisdatensatz
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler


# Definition einer Klasse für Objekt orientierten Programmierung
class setup():
	__doc__ = '''
	Hier kann ein Hilfetext eingetragen werden....
	'''

	# definition einer Methode die EINMALIG bei der initialisierung der Klasse durchgeführt wird
	def __init__(self):
		pass

	# Definition einer Methode/ Funktion der obigen Klasse
	def load(self):
		# try/ except ermöglicht einen Befehl auszuprobieren und auf den Fehler zu reagieren
		# das Programm stürzt NICHT ab
		try:
			self.X, self.y = load_iris(return_X_y=True, as_frame=True)
			self.labels_ = self.X.columns
			success = True
		except:
			success = False
			pass
		return success

	def explore(self):
		print('X\n')
		# Zeige X, welches in meinem Klassenobjekt "self" definiert ist (durch die Methode load()),
		# nutze dabei die vererbte pandas Basis Methode "head()" (load_iris Funktion liefert ein Pandas Objekt!)
		print(self.X.head())
		# percentile Liste
		perc = [.20, .40, .60, .80]
		# Liste von dtypes die einbezogen werden sollen
		include = ['object', 'float', 'int']
		print('Basis Überblick \n')
		print(self.X.describe(percentiles=perc, include=include))
		print('y \n')
		print(self.y.head())

		data = pd.concat([self.X, self.y], axis=1)
		my.plot_in_2_dims(data=data, title="Data Understanding")


# Definition einer Methode/ Funktion der prozeduralen Programmierung
# parameter werden per NAmen übergeben alles was nach (*, ... kommt, sind "Named Parameter"

def data_preparation(*, x=None, y=None):
	# Aufteilen der Daten in Test und Training Set
	# Naming Convention: großes X -> Matrix, kleines y -> Vektor
	X_train, X_test, y_train, y_test = train_test_split(x,
	                                                    y,
	                                                    train_size=.66,
	                                                    random_state=666)

	# scaler instanziert ein Object der Klasse StandardScaler aus der Bibliothek sklearn
	scaler = StandardScaler()
	# fit und transform Model auf X_train!
	X_train = scaler.fit_transform(X_train)
	# Test Datensatz wird nur transformiert, die Parameter kommen vom fit auf X_train
	X_test = scaler.transform(X_test)

	return X_train, X_test, y_train, y_test


# parameter werden per Position übergeben alles
def modeling(x_train, y_train):
	X = x_train
	y = y_train
	# instanziere Algorithmus
	knn = KNeighborsClassifier()
	# definiere mögliche Parameterwerte als Liste -> []!
	parameter = {'n_neighbors': list(np.arange(3, 20, 2))
	             }
	model = GridSearchCV(estimator=knn,
	                     param_grid=parameter,
	                     cv=5,
	                     return_train_score=True)
	model.fit(X, y)
	return model


def evaluate(*, model=None, X_test=None, y_test=None):
	y_predict = model.predict(X_test)
	# manual scoring
	score = np.mean(y_test == y_predict)
	# provided scoring method
	score = model.score(X_test, y_test)
	print('Best score {:.2f} with following parameters: {}'.format(score, model.best_estimator_))

	visualise_accuracy(model=model)

	# Fehlqualifizierungen als -1
	y_predict[y_test != y_predict] = -1
	y_predict = y_predict.reshape(len(y_predict), 1)
	feature_names = list(
		data.X.columns)  # never ever do so!, Variables sollten inhärent sein oder direkt übergeben werden
	feature_names.append('target')
	# X und y_predict sind numpy arrays!
	# werden arrays vebunden (append), dann haben alle den gleichen Datentyp!
	X_y = pd.DataFrame(np.append(X_test, y_predict, axis=1), columns=feature_names)
	# ändert den Datentyp für die Klasse zu int -> "mehr" kategorial....
	X_y['target'] = X_y['target'].astype(int)
	visualise_prediction(data=X_y)

	return score


def visualise_accuracy(*, model=None):
	cv_results = model.cv_results_
	scores_mean = cv_results['mean_test_score']
	scores_train = cv_results['mean_train_score']

	x = model.param_grid['n_neighbors']
	plt.plot(x, scores_mean)
	plt.xlabel('n_neighbors')
	plt.xticks(x)
	plt.ylabel('accuracy')
	plt.title('Entwicklung Accuracy')
	plt.show()


def visualise_prediction(*, data=None):
	my.plot_in_2_dims(data=data, title="Data Understanding")
	fig = px.parallel_coordinates(data, color='target')
	fig.show()


# Programm Start
'''
vordefinierte Variable __name__ enthält '__main__' wenn das script direkt aufgerufen wird
'''
if __name__ == '__main__':
	# Objekt orientierter Ansatz
	data = setup()
	data.load()
	data.explore()

	# prozeduraler Ansatz
	X_train, X_test, y_train, y_test = data_preparation(x=data.X, y=data.y)
	model = modeling(X_train, y_train)
	evaluate(model=model, X_test=X_test, y_test=y_test)
