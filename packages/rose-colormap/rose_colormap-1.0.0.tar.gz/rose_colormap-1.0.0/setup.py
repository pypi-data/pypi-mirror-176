from setuptools import setup, find_packages


setup(
    name='rose_colormap',
    version='1.0.0',
    license='MIT',
    author="Zihao Zhou",
    author_email='ziz244@github.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Rose-STL-Lab/rose_colormap',
    keywords='visualization',
    install_requires=[
          'matplotlib', 'plotly', 'numpy'
      ],

)
