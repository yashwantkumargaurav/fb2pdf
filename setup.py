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
      scripts=['scripts/fbmerge','scripts/fb2pdf_queue_send','scripts/fb2pdf_queue_clear','scripts/fb2pdf_queue_receive','scripts/fbdaemon','scripts/fb2tex','scripts/fb2pdf_mixpng'],
      data_files=[('share/texmf-local/', ['src/TeX/verse.sty', 'src/TeX/epigraph.sty','src/TeX/sectsty.dtx', 'src/TeX/sectsty.ins']),('share/fb2pdf',['etc/broken-image.png','lib/epubgen-0.5.0.jar'])]
     )
