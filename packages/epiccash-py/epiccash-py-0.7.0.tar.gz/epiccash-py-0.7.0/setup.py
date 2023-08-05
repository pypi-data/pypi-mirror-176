import setuptools

setuptools.setup(
    name='epiccash-py',
    version='0.7.0',
    description='EPIC wallet and node API wrapped in Python',
    url='https://github.com/blacktyger/epic-py',
    author='@blacktyg3r',
    author_email='blacktyg3r@gmail.com',
    license='-',
    package_dir={"": "epicpy"},
    packages=setuptools.find_packages(where="epicpy"),
    install_requires=[
        "asn1crypto==1.5.1",
        "coincurve==17.0.0",
        "psutil==5.9.4",
        "pycparser==2.21",
        "pycryptodome==3.15.0",
        "requests==2.28.1",
        "tomlkit==0.11.6",
        "urllib3==1.26.12",
        ],

    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        ],
    )
