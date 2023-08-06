# This file is placed in the Public Domain.


import os


from setuptools import setup


def read():
    return open("README.rst", "r").read()


def uploadlist(dir):
    upl = []
    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if os.path.isdir(d):   
            upl.extend(uploadlist(d))
        else:
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)
    return upl


setup(
    name='gcide',
    version='2',
    url='https://github.com/bthate/gcide',
    author='Bart Thate',
    author_email='operbot100@gmail.com', 
    description="ICC. Prosecutor. Reconsider OTP-CR-117/19.",
    long_description=read(),
    long_description_content_type='text/x-rst',
    license='Public Domain',
    packages=["gcide"],
    zip_safe=True,
    include_package_data=True,
    data_files=[
                ("share/gcide", ["files/gcide.service",]),
                ("share/doc/gcide/", uploadlist("docs")),
                ("share/doc/gcide/pdf/", uploadlist("docs/pdf")),
                ("share/doc/gcide/_static/", uploadlist("docs/_static")),
                ("share/doc/gcide/_templates/", uploadlist("docs/_templates")),
               ],
    scripts=["bin/gcide", "bin/gcidecmd", "bin/gcidectl", "bin/gcided"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
