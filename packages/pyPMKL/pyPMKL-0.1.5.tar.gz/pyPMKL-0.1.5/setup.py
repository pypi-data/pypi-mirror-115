from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='pyPMKL',
    version='0.1.5',
    description='Tessellated Kernels SVM',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='AT',
    author_email='atalitck@asu.edu',
    keywords=['Kernel learning', 'SVM', 'Multiple Kernel Learning'],
    url='https://github.com/Talitsky/PMKL',
    download_url='https://pypi.org/project/pyPMKL/'
)

install_requires = [
    'numpy',
    'scikit-learn',
    'matplotlib',
    'scipy',
    'libsvm'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)