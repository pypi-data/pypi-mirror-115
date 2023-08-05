#!/usr/bin/env python
#
# setup.py for flashbake
from setuptools import setup, find_packages



setup(name='flashbake',
        version='0.30.0',
        author="Thomas Gideon",
        author_email="cmdln@thecommandline.net",
        maintainer="Thomas Gideon",
        maintainer_email="cmdln@thecommandline.net",
        description="Automation to feed lifelog data into a version control message stream.",
        long_description="Flashbake is designed to help technically savvy writers use version control in their workflow. It compiles information from the user's lifelog including recent social media posts, blog posts, music listening, current weather, location, and more. It then automates the inclusion of that information in each commit message.",
        long_description_content_type='text/markdown',
        platforms=[ "noarch" ],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Topic :: Artistic Software'
        ],
        url="http://thecommandline.net",
        download_url="https://github.com/commandline/flashbake/downloads",
        license="GPLv3",
        package_dir={'': 'src'},
        packages=find_packages(where='./src/', exclude=('./test/')),
        install_requires='''
            enum34 >=1.0.3
            feedparser >=4.1
            requests >=2.23.0
            ''',
        entry_points={
                'console_scripts': [ 'flashbake = flashbake.console:main',
                                     'flashbakeall = flashbake.console:multiple_projects' ]
                },
        include_package_data = True,
        exclude_package_data = { '' : [ 'test/*' ] },
        test_suite="test",
        )
