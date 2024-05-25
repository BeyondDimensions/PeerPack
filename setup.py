from setuptools import setup, find_packages

setup(
    name='peerpack',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'peerpack=peerpack.cli:main'
        ]
    },
    install_requires=[
        # List your dependencies here
    ],
    author='Peer Pack',
    author_email='info@peerpack.io',
    description='Decentralized package manager for Python',
    url='https://github.com/BeyondDimensions/PeerPack',
    license='MIT',
)
