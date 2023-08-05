from setuptools import setup
setup(
    name = 'cz_wfcast',
    packages = ['sunnyday'],
    version = '1.0.0',
    license = 'MIT',
    description = 'Weather forecast data',
    author = 'Contrazap',
    author_email = 'contrazap@gmail.com',
    url = 'https://example.com',
    keywords = ['contrazap', 'wfcast'],
    install_requires=[
            'requests',
        ],
    classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.7'
        ],
    )