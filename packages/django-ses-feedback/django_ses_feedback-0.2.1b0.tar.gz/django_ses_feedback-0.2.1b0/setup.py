import os

from setuptools import find_packages, setup

project_name = 'django_ses_feedback'

if os.path.exists('README.rst'):
    long_description = open('README.rst', 'r').read()
else:
    long_description = (
        'See https://hg.code.netlandish.com/~netlandish/django-ses-feedback/'
    )


setup(
    name=project_name,
    version=__import__(project_name).get_version(),
    packages=find_packages(),
    description='Process Amazon SES Feedback',
    author='Netlandish Inc.',
    author_email='hello@netlandish.com',
    url='https://hg.code.netlandish.com/~netlandish/django-ses-feedback/',
    long_description=long_description,
    platforms=['any'],
    install_requires=['Django>=1.8', 'boto3'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Environment :: Web Environment',
    ],
    include_package_data=True,
)
