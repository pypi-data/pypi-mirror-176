from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='package-test99',
    version='0.0.1',
    url='https://github.com/nataliaweni/package-test99',
    license='MIT License',
    author='Natália de Assis',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='natalia.assis@weni.ai',
    keywords='Pacote',
    description=u'Exemplo de pacote PyPI',
    packages=['package-test99'],
    install_requires=['numpy'],)