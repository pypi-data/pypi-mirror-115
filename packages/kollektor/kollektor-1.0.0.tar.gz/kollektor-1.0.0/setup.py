from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='kollektor',
    version='1.0.0',
    description='📦 Collection utility for Python.',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    url='https://github.com/kremayard/kollektor/',
    author='kremayard',
    author_email='',
    license='MIT',
    project_urls={
        "Bug Tracker": "https://github.com/kremayard/kollektor/issues",
    },
    classifiers=classifiers,
    keywords=["python", "collector", "krema", "collection"],
    packages=find_packages(),
    python_requires='>=3.6.0',
    install_requires=[]
)