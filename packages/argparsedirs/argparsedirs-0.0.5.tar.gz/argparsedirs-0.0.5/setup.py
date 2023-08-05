import setuptools


setup_args = dict(
    name='argparsedirs',
    version='0.0.5',
    description='Readable and Writeable dir type for argparse',
    license='MIT',
    packages=setuptools.find_packages(),
    author="Martin 'Kvík' Baláž",
    author_email='martin.balaz@trojsten.sk',
    keywords=['argparse', 'directories'],
    url='https://github.com/sesquideus/argparsedirs',
    download_url='https://pypi.org/project/argparser/',
    include_package_data=True,
)

install_requires = [
    'argparse',
]

if __name__ == '__main__':
    setuptools.setup(**setup_args, install_requires=install_requires)
