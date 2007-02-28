#!/usr/bin/env python2.4

from distutils.core import setup

setup(name='fb2pdf',
      version='1.0',
      description='FictionBook2 to PDF conversion tools',
      author='Vadim Zaliva, et. al.',
      author_email='lord@crocodile.org',
      url='http://code.google.com/p/fb2pdf/',
      packages=['fb2pdf'],
      package_dir={'fb2pdf': 'src/fb2pdf'},
      package_data={'fb2pdf': ['src/TeX/*.sty']},
     )
