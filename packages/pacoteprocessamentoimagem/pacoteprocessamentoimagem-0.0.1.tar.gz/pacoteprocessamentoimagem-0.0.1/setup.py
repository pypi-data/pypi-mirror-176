from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='pacoteprocessamentoimagem',
    version='0.0.1',
    url='https://github.com/isabela-rossetti/pacote_python',
    license='MIT License',
    author='Isabela Rossetti',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='isabelarossetti.ir@gmail.com',
    keywords='Imagem',
    description=u'Pacote de leitura e processamento de imagens em python',
    packages=['pacoteprocessamentoimagem'])