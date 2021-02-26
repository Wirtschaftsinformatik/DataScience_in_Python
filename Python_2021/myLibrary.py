def plot_in_2_dims(data=None, title=''):
	'''
	Plotting all features in in 2D combinations
	colors depending on class (-1 reserved for misclassified samples, painted black)
	:param data:
	expects pandas dataframe with features and classes (column named target)
	:return:
	None
	'''
	import matplotlib.pyplot as plt
	import numpy as np
	import pandas as pd
	import itertools

	feature_names = data.columns[data.columns != 'target']

	n_dim = len(feature_names)

	# Black removed and is used for misqualificated instances instead.
	unique_labels = set(pd.unique(data['target']))
	colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]

	# use predefined styles
	plt.style.use('bmh')
	# fig, ax = plt.subplots(n_dim, n_dim, sharey=True, sharexarex=True)
	fig, ax = plt.subplots(n_dim, n_dim)

	# print(plt.style.available)
	fig.set_size_inches(12, 12)
	plt.suptitle(title, fontsize=12)

	l_dim = np.arange(0, n_dim)
	views = list(itertools.product(l_dim, l_dim))

	for view in views:
		for k, col in zip(unique_labels, colors):
			if k == -1:
				# Black used for noise.
				col = [0, 0, 0, 1]
				marker = "D"
				markersize = 4
			else:
				marker = 'o'
				markersize = 2

			class_member_mask = (data['target'] == k)
			xy = data[class_member_mask]
			# plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
			# 		 markeredgecolor='k', markersize=14)
			ax[view[0], view[1]].scatter(xy.iloc[:, view[0]], xy.iloc[:, view[1]], color=tuple(col), marker=marker,
			                             s=markersize)
			plt.plot()

		ax[view[0], view[1]].set_ylabel(feature_names[view[0]], fontsize=8)
		ax[view[0], view[1]].set_xlabel(feature_names[view[1]], fontsize=8)
		ax[view[0], view[1]].tick_params(axis="both", labelsize=4)
	plt.show()
