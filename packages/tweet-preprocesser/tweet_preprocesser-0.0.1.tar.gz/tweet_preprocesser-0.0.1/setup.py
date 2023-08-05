from setuptools import setup
from codecs import open
from os import path
package_name = "tweet_preprocesser"
root_dir = path.abspath(path.dirname(__file__))
# requiwements.txtの中身を読み込む
def _requirements():
    return [name.rstrip() for name in open(path.join(root_dir, 'requirements.txt')).readlines()]
# README.mdをlong_discriptionにするために読み込む
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
setup(
    name=package_name,
    version='0.0.1',
    description='tweet preprocesser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/onyanko-pon/tweet_preprocesser',
    author='onyanko-pon',
    author_email='engineer.tsukasa@gmail.com',
    license='MIT',
    keywords='twitter,tweet',
    packages=[package_name],
    install_requires=_requirements(),
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
)