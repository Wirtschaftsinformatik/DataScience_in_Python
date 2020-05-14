import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris['data'], iris['target'], test_size=0.33, random_state=1)

steps = [('scaler', StandardScaler()), ('knn', KNeighborsClassifier())]
#param_grid = {'knn__k_neighbors': np.arange(3, 25, 2)}

param_grid = {'knn__n_neighbors': np.arange(3, 25, 2),
			  'knn__leaf_size': np.arange(2, 25, 2)}
pipe = Pipeline(steps=steps)
grid = GridSearchCV(pipe, param_grid=param_grid, cv=5)
grid.fit(X_train, y_train)
grid.score(X_test, y_test)
print('Best parameters: {}'.format(grid.best_params_))
print('Best scores: {}'.format(grid.best_score_))
