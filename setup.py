from setuptools import setup

setup(
    name='GFaker',
    version='0.1',
    description='Generates fake gmails and inbox.',
    url='https://github.com/Otherwolf/GFaker',
    author='otherWolf',
    author_email='vpe304@gmail.com',
    packages=['tools', 'tools.mail'],
    install_requires=[
        'requests',
        'urllib3',
        'requests-toolbelt'
    ]
)