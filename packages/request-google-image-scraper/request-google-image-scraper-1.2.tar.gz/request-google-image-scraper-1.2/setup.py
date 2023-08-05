from distutils.core import setup
setup(
  name = 'request-google-image-scraper',
  packages = ['requestgoogleimagescraper'],
  version = '1.2',
  license='MIT',
  description = 'Scrape results from Google Images fastly via Requests, without using any Google API.',
  author = 'Lucas Enríquez',
  author_email = 'Animations468@gmail.com', 
  url = 'https://github.com/AlvinIsCrack/request-google-image-scraper',
  download_url = 'https://github.com/AlvinIsCrack/request-google-image-scraper/archive/refs/tags/v1.2.tar.gz',
  keywords = ['SCRAPER', 'SCRAPE', 'IMAGE', 'SEARCH', 'DOWNLOAD', 'GOOGLE', 'RESULTS', 'SCRAPE', 'REQUEST'],
  install_requires=[
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)