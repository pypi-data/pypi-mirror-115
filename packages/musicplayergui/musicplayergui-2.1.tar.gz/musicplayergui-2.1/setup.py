from setuptools import setup, find_packages
 
classifiers = []
 
setup(
  name='musicplayergui',
  version='2.1',
  description='Random Music Player In form of GUI (So terrible GUI.)',
  long_description=open('README.md').read() + "\n",
  long_description_content_type='text/markdown',
  url='https://github.com/I-make-python-module-and-bots-stuff/Music-player',  
  author='Rukchad Wongprayoon',
  author_email='contact@biomooping.tk',
  license='MIT', 
  classifiers=classifiers,
  keywords='Tools', 
  packages=find_packages(),
  install_requires=["pygame"],
  entry_points={'console_scripts':'musicplayergui=musicplayergui:launch'}
)
