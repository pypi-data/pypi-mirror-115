from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='krema',
    version='1.0.0',
    description='🚀 A fast, flexible and lightweight Discord API wrapper for Python.',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    url='https://github.com/kremayard/krema/',
    author='kremayard',
    author_email='',
    license='MIT',
    project_urls={
        "Bug Tracker": "https://github.com/kremayard/krema/issues",
    },
    classifiers=classifiers,
    keywords=["python", "krema", "discord", "discord-api", "api-wrapper"],
    packages=find_packages(),
    python_requires='>=3.8.0',
    install_requires=["kollektor"]
)