import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name='SqlalchemyMixin',
    version="0.0.35",
    author="Yaşar Özyurt",
    author_email="blueromans@gmail.com",
    description='Active Record, Django-like queries, nested eager load '
                'and beauty __repr__ for SQLAlchemy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/blueromans/SqlalchemyMixin.git',
    project_urls={
        "Bug Tracker": "https://github.com/blueromans/SqlalchemyMixin/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "SQLAlchemy >= 1.0",
        "six",
        "python-slugify",
        "phonenumbers",
        "arrow",
        "typing; python_version < '3.5'"
    ],
    keywords=['sqlalchemy', 'active record', 'activerecord', 'orm',
              'django-like', 'django', 'eager load', 'eagerload', 'repr',
              '__repr__', 'mysql', 'postgresql', 'pymysql', 'sqlite'],
    packages=['sqlalchemy_mixins', 'sqlalchemy_mixins.extra'],
    python_requires=">=3.6",
)
