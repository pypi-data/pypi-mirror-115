import setuptools

__version__ = '0.0.3'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='easypipe',
    version=__version__,
    author='Khalid Almufti',
    author_email='almufti.khalid@gmail.com',
    description='EasyPipe is a simple tool for developers to build ML applications.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kalmufti/easypipe',
    project_urls={
        'Bug Tracker': 'https://github.com/kalmufti/easypipe/issues',
    },
    install_requires=[
        'mediapipe',
        'opencv-python>=4.5',
    ],
    extras_require={
        'dev': [
            'pytest>=6.2',
        ],
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.6',
    license='Apache 2.0',
    keywords='mediapipe',
)
