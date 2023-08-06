from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='trtimeextractor',
      version='0.1.2',
      description='Time Extractor NLP project - locate dates and times in text documents',
      long_description=readme(),
      keywords='NLP text extraction time date',
      url='https://github.com/westeropsml/time-extractor-tr',
      author='WesterOps',
      author_email='ml@westerops.com',
      license='WesterOps',
      install_requires=[
          'pyjnius==1.1.1',
      ],
      packages=['trtimeextractor'],
      include_package_data=True,
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
