from distutils.core import setup
setup(
  name = 'test_package_badr_moufad',      
  packages = ['test_package_badr_moufad'],
  version = '0.1',
  license='MIT', 
  description = 'A test repo to publish a python package to PyPI',
  author = 'Badr MOUFAD',
  author_email = 'Badr.MOUFAD@emines.um6p.ma',
  url = 'https://github.com/Badr-MOUFAD/test_package_badr_moufad',
  download_url = 'https://github.com/Badr-MOUFAD/test_package_badr_moufad/archive/refs/tags/v0.1.tar.gz',
  keywords = ['Example', 'test_package'],
  install_requires=[
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)