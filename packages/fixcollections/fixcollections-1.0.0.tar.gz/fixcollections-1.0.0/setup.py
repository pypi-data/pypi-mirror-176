# ah the irony, we need to use library itself to use old setuptools
import fixcollections
fixcollections.monkeypatch()

from setuptools import setup

setup(name='fixcollections',
      version='1.0.0',
      description='Compatibility fix for collections.abc api break made in Python 3.10',
      author='Ville M. Vainio',
      author_email='ville.vainio@basware.com',
      url='https://github.com/vivainio/fix-py-collections',
      modules=['fixcollections']
     )
