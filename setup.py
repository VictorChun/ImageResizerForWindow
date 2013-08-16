from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
	options = {'py2exe':{'bundle_files':1, 'dll_excludes':['MSVCP90.dll']}},
	windows = [{'script':'image_resizer.py'}],
	zipfile = None)
