from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='inspector-python',
    version='0.1.6',
    description='Connect your Python applications with Inspector.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Antonio Bruno',
    author_email='antoniobruno82@gmail.com',
    url='https://inspector.dev/',
    extras_require=dict(tests=['pytest']),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    license='MIT'
)
