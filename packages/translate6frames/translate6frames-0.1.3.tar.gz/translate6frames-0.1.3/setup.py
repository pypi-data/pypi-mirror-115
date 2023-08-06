from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='translate6frames',
    version='0.1.3',
    description='translate genes RNA/DNA to proteins (all 6 frames)',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Ehdieh Khaledian',
    author_email='khaledianehdieh@gmail.com',
    keywords=['Translate genes', '6 frame', 'gene to protein', 'python DNA to protein', 'python', 'RNA to protein'],
    url='https://github.com/khaledianehdieh/translate6frames',
    download_url='https://pypi.org/project/translate6frames/'
)

install_requires = []

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
