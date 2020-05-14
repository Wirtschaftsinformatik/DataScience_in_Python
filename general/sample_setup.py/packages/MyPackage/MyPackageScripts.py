import logging


def print_func(text):
	try:
		logging.info('Print_func called')
		print('This is a package ')
		print(text)
		return 0

	except:
		logging.error('So would be an error log')
		return 1
