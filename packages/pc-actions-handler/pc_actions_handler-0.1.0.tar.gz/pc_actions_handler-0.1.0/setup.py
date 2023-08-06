from setuptools import setup, find_packages

setup(
    name='pc_actions_handler',
    description='A simple http server to handle desktop actions',
    version='0.1.0',
    author='Filipe Alves',
    author_email='filipe.alvesdefernando@gmail.com',
    install_requires=[
        'Flask',
        'flask_restful',
    ],
    packages=find_packages(),
    scripts=['pc-actions-handler'],
    url='https://github.com/filipealvesdef/pc_actions_handler',
    zip_safe=False,
)
