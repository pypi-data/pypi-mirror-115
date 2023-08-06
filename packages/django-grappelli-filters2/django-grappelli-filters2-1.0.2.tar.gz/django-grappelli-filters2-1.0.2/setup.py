from setuptools import setup, find_packages

setup(
    name='django-grappelli-filters2',
    version='1.0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django', 'django-grappelli'],
    license='Unlicense',
    description='Additional filters for Djagno Grappelli admin',
    url='https://github.com/frnhr/django-grappelli-filters/',
    author='Fran Hrzenjak',
    author_email='fran@changeset.hr',
    package_data={'grappelli_filters': [
        'templates/grappelli_filters/*.html',
        'static/grappelli_filters/*.*',
    ]},
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: Freeware',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
