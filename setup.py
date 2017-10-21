import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'plaster_pastedeploy',
    'pyramid',
    'waitress',
    'google-api-python-client',
    'requests',
    "PyJWT",
    "pyramid-debugtoolbar"
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
]

setup(
    name='gaf_api',
    version='0.0',
    description='GAF API',
    long_description="GAF API" + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='https://github.com/TheNeverEndingGAF',
    author_email='developers@neverendinggaf.com',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
        'debug': ['pyramid_debugtoolbar']
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = gaf_api:main',
        ],
    },
)
