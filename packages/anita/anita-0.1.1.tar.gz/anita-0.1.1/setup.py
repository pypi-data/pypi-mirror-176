from setuptools import setup, find_packages


setup(
    name='anita',
    version='0.1.1',
    license='MIT',
    author="Davi Romero de Vasconcelos",
    author_email='daviromero@ufc.br',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/daviromero/anita',
    keywords='Analytic Tableaux, Teaching Logic, Educational Software', 
    install_requires=[
          'rply',
      ],

)
