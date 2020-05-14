#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import section, should be at the beginning of the file
# import standard packages
import logging
import os
import sys

# import everything from MyScript
import scripts.MyScript as MS
# import everything only print_func from MyPackages
from packages.MyPackage.MyPackageScripts import print_func


def SetLogging():
	gettrace = getattr(sys, 'gettrace', None)

	_debug = True
	if gettrace is None:
		_debug = False
		print('No sys.gettrace')
	elif gettrace():
		_debug = True
		print('Debug mode detected')

	if _debug:
		logging.basicConfig(
			stream=sys.stdout,
			format='%(asctime)s %(name)s %(levelname)s %(message)s\n',
			datefmt='%H:%M:%S',
			level='INFO'
		)

	else:
		logfile = os.path.join(os.getcwd(), 'logs', 'logfile.log')
		logging.basicConfig(
			filename=logfile,
			filemode='w+',
			format='%(asctime)s %(name)s %(levelname)s %(message)s\n',
			datefmt='%Y-%m-%d %H:%M:%S',
			level='INFO'
		)

	return _debug


def print_main(*, text='No text provided'):
	DEBUG = SetLogging()
	# call my script via MS
	MS.print_func(text)
	# call package function directly
	print_func(text)


print_main(text='test')
