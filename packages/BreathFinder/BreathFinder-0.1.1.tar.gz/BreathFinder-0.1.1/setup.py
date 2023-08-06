from distutils.core import setup
setup(
    name='BreathFinder',
    packages=['BreathFinder'],
    install_requires=[
          'numpy',
          'sklearn',
          'scipy'
    ],
    version='0.1.1',
    description='''Algorithm designed to find locations of
    individual breaths in a PSG''',
    author='Benedikt Holm Thordarson',
    license='MIT',
    author_email = 'b@spock.is',
    url = 'https://github.com/benedikthth/BreathFinder',
    download_url = 'https://github.com/benedikthth/BreathFinder/archive/refs/tags/v0.1.0.tar.gz',
    keywords = ['Adaptive segmentation', 'Sleep research', 'RIP belts'],   # Keywords that define your package best
    classifiers=[
        'Development Status :: 3 - Alpha',      
        'Intended Audience :: Developers',      
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',      
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
  ],
)
