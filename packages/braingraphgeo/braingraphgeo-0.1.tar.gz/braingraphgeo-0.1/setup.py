from setuptools import setup

DEPENDENCIES = ['numpy', 'pandas', 'matplotlib==3.4.2',
                'scipy', 'seaaborn', 'networkx', 'fury']

setup(name='braingraphgeo',
      version='0.1',
      description='Python package for performing analysis on structural brain networks using random geometric surrogate graphs',
      author='Scott Trinkle',
      author_email='tscott.trinkle@gmail.com',
      license='MIT',
      install_requires=DEPENDENCIES,
      url='https://github.com/scott-trinkle/braingraphgeo',
      download_url='https://github.com/scott-trinkle/braingraphgeo/archive/refs/tags/v_0.1.tar.gz',
      keywords=['tractography', 'brain network', 'graph theory'],
      packages=['braingraphgeo'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9'
      ]
      )
