from setuptools import setup


setup(
    name='bshlib',
    version='1.0.0',
    description="Bashiron's personal utilities",
    long_description='<detailed description>',
    author='bashiron',
    mantainer='bioshiron@gmail.com',
    url='<future github url>',
    # python_requires='<?>',
    package_dir={'': 'lib'},
    packages=['bshlib'],
    # py_modules=[],
    install_requires=[
        'pandas==2.0.1',
        'more-itertools==9.0.0',
        'loguru==0.7.2',
        'opencv-python==4.7.0.72'
    ],
)
