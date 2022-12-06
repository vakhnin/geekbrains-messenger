from setuptools import setup, find_packages

setup(name='geekbrains-messenger-client',
      version='0.2.0',
      description='geekbrains-messenger-client',
      author='Sergey Vakhnin',
      author_email='test@test.ru',
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy']
      )
