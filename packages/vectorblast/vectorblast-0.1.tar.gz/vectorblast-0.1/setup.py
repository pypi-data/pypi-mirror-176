from setuptools import setup, find_packages


setup(
    name='vectorblast',
    version='0.1',
    license='MIT',
    author="Mario Ceresa",
    author_email='mrceresa@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/jrcf7/vector_blast',
    keywords='blast dna embeddings search fast',
          entry_points = {
              'console_scripts': [
                  'vecb = vecb.vecb:main',                  
              ],              
          },

)