from distutils.core import setup
from pkgutil import walk_packages

import django_inline_sass


def find_packages(path, prefix=""):
    yield prefix
    prefix = prefix + "."
    for _, name, ispkg in walk_packages(path, prefix):
        if ispkg:
            yield name


setup(
  name = 'django-inline-sass',
  packages = list(find_packages(django_inline_sass.__path__, django_inline_sass.__name__)),
  version = '0.1.0',
  description = 'Django Inline SASS',
  author = 'Matt Roberts',
  author_email = 'contact@maleero.com',
  url = 'https://github.com/malero/django-inline-sass',
  download_url = 'https://github.com/malero/django-inline-sass/archive/v0.1.0.tar.gz',
  keywords = ['django', 'sass', 'seo'],
  classifiers = [],
  install_requires=['libsass==0.21.0',],
)
