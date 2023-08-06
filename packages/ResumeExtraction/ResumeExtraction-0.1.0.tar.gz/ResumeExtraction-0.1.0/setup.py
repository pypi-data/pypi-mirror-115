from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='ResumeExtraction',
    version='0.1.0',
    url="",
    description='An ML based resume parser used for extracting information from resumes',
    author='Octonava Private Limited',
    author_email='info@octonava.com',
    license='GPL-3.0',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(),
    install_requires=[
        'attrs>=21.2.0',
        'blis>=0.2.4',
        'certifi>=2021.5.30',
        'chardet>=3.0.4',
        'cymem>=2.0.5',
        'docx2txt>=0.7',
        'idna>=3.2',
        'jsonschema>=3.0.2',
        'nltk>=3.5',
        'numpy>=1.21.1',
        'pandas>=1.2.2',
        'pdfminer.six>=20181108',
        'preshed>=2.0.1',
        'pycryptodome>=3.4.3',
        'pyrsistent>=0.18.0',
        'python-dateutil>=2.8.2',
        'pytz>=2021.1',
        'requests>=2.22.0',
        'six>=1.16.0',
        'sortedcontainers>=2.4.0',
        'spacy>=2.1.4',
        'srsly>=1.0.5',
        'thinc>=7.0.8',
        'tqdm>=4.51.0',
        'urllib3>=1.26.6',
        'wasabi>=0.8.2'
    ],
    zip_safe=False,
    entry_points = {
        'console_scripts': ['ResumeExtraction=ResumeExtraction.command_line:main'],
    }
)