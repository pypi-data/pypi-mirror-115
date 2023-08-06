from setuptools import setup
# calling the setup function 
setup(name='hdltobq',
      version='0.0.1',
      description='A Data Migration API for Data Lake to BQ',
	  long_description='Data Migration Utility from DL to BQ',
	  packages=["hdltobq"],
      author='shivam shukla',
      author_email='shivamshukla12@gmail.com',
	  classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
      package_dir = {' ':r'C:\Users\i339715\Desktop\dl2bq\src'}
      )