from setuptools import setup, find_packages

setup(name="has_auth_client",
      version="0.1.6",
      description="auth middleware client",
      author="Florian Baier",
      author_email="f.baier1@gmail.com",
      packages=find_packages(),
      install_requires=['requests'])