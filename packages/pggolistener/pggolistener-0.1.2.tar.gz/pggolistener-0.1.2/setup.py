from distutils.core import setup

setup(
    name='pggolistener',
    version="0.1.2",
    packages=['pggolistener'],
    package_dir={'': '.'},
    package_data={'': ['sub.dll', 'sub.so']},
    long_description='python call golang postgres sub ',
)
