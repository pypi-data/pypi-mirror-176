import setuptools

def read(path):
    with open(path, encoding = 'utf-8') as f:
        return f.read()

setuptools.setup(
    name="genolearn",
    version="0.0.6",
    author="Jordan Taylor",
    author_email="jt2006@bath.ac.uk",
    description="A machine learning toolkit for genome sequence data",
    url="https://github.com/jordan-wei-taylor/genolearn",
    project_urls={
        "Bug Tracker": "https://github.com/jordan-wei-taylor/genolearn/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        'scipy>=1.8.0',
        'numpy>=1.22.3',
        'psutil>=5.9.0',
        'scikit-learn>=1.1.2',
        'pathos>=0.3.0',
        'click>=8.1.3',
        'pandas>=1.4.2'
    ],
    package = ['genolearn'],
    entry_points='''
        [console_scripts]
        genolearn=genolearn.__main__:cli
        preprocess=genolearn.__main__:preprocess
    '''
)