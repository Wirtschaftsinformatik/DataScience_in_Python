#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest import TestSuite
from unittest import TextTestRunner


class TestDataPlot(TestCase):
	def setUp(self) -> None:
		pass

	def tearDown(self) -> None:
		pass

	def test_tasks(self):
		print('Start Test')

		# script to test from script library....
		import scripts.MyScript as MS
		# call aggregated tasks
		result = MS.print_func('called from test')
		print(result)

		# script to test from script library....
		from packages.MyPackage import MyPackageScripts as MP
		# call aggregated tasks
		result = MP.print_func('called from test')
		print(result)


# self.fail()


class test():
	def suite(*, num=1):
		# create TestSuite object
		suite = TestSuite()
		# call test via TestDataPlot in script, could be done dirctly
		suite.addTest(TestDataPlot('test_tasks'))
		return suite


# create TextTestRunner environment

runner = TextTestRunner()
# call test definitions
result = runner.run(test.suite(num=5))
print(result)

# for detail see: https://docs.python.org/3.6/library/unittest.html?highlight=unittest#module-unittest
