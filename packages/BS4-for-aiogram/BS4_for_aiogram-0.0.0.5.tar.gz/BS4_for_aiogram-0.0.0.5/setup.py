from setuptools import setup, find_packages

setup(
      name='BS4_for_aiogram',
      version='0.0.0.5',
      description='I delete chardet code from dammit.py in BS4 library',
      long_description="Original project: https://pypi.org/project/beautifulsoup4/",
      keywords='BS4 aiogram BeautifulSoup4',
      license='No',
      packages=find_packages(),
      install_requires=[
          'soupsieve'
      ],
      include_package_data=True,
      zip_safe=False
      )