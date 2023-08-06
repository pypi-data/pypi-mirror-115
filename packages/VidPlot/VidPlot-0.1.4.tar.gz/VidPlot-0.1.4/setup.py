from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 2 - Pre-Alpha',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='VidPlot',
  version='0.1.4',
  description='Create and Display mp4 file from matplotlib figure',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Silvano Rosenau',
  author_email='silvano.rosenau@studium.uni-hamburg.de',
  license='MIT',
  classifiers=classifiers,
  keywords='video',
  packages=find_packages(),
  install_requires=['numpy', ['imageio'], ['IPython'], ['imageio-ffmpeg']]
)
