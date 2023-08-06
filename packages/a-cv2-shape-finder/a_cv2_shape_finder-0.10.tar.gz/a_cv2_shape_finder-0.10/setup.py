from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.10'
DESCRIPTION = "Detecting shapes with OpenCV, and getting all the important information in a DataFrame"

# Setting up
setup(
    name="a_cv2_shape_finder",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/a_cv2_shape_finder',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['a_cv_imwrite_imread_plus', 'flatten_everything', 'more_itertools', 'numpy', 'opencv_python', 'pandas'],
    keywords=['opencv', 'cv2', 'pandas', 'DataFrame', 'shapes', 'object detection', 'shape'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.9', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Text Editors :: Text Processing', 'Topic :: Text Processing :: General', 'Topic :: Text Processing :: Indexing', 'Topic :: Text Processing :: Filters', 'Topic :: Utilities'],
    install_requires=['a_cv_imwrite_imread_plus', 'flatten_everything', 'more_itertools', 'numpy', 'opencv_python', 'pandas'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*