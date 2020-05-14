import logging


def print_func(text):
	try:
		logging.info('Print_func called')
		print('This is a script function call')
		print('{}'.format(text))
		return 0

	except:
		logging.error('So would be an error log')
		return 1
