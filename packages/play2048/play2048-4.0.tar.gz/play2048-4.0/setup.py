from setuptools import setup, find_packages

setup(
    name             = 'play2048',
    version          = '4.0',
    description      = '2048 game',
    long_description = open('README.md').read(),
    author           = '5-23',
    author_email     = 'yhanbyeol6@gmail.com',
    url              = 'https://github.com/objectiveTM/play2048',
    download_url     = 'https://github.com/objectiveTM/play2048',
    install_requires = ['easy_pil'],
    packages         = find_packages(exclude = ['docs', 'example']),
    keywords         = ['game', '2048'],
    python_requires  = '>=3',
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)