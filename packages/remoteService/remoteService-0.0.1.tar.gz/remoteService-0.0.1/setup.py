# the setup.py file is used to build the package
# contain information about your package, specifically the name of the package,
# its version, platform-dependencies and a whole lot more.
from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Remote Service Package'
LONG_DESCRIPTION = '''Remote Service Package to help build remote services like Recommendation
engines, insight engines, and analytics pipelines'''

# Setting up
setup(
       # the name must match the folder name 'remoteService'
        name="remoteService",
        version=VERSION,
        author="Subhasish Sarkar",
        author_email="subhasish.sarkar@gada.io",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['numpy',\
                          'pandas',\
                          'matplotlib',\
                          'sklearn',\
                          'flask',\
                          'Flask-SQLAlchemy',\
                          'Flask-Marshmallow',\
                          'Marshmallow-SQLAlchemy',\
                          'mpld3',\
                          'wordcloud'], # add any additional packages that
        # needs to be installed along with your package.
        keywords=['python', 'remote service'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
