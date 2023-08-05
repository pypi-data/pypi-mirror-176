from setuptools import setup

with open('README.md') as fp:
    long_description = fp.read()

setup(
    name = 'Elite-Multiprocessing',
    version = '1.0.1',
    author = 'Muhammad Imran Liaqat Ali',
    author_email = 'CEO@xprojecthub.com.com',
    description = 'Elite-Multiprocessing is a package that supports spawning processes using an API similar to the threading module. The multiprocessing package offers both local and remote concurrency, effectively side-stepping the Global Interpreter Lock by using subprocesses instead of threads.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    python_requires = '>=3',
    install_requires = ['ecdsa', 'PyCryptodome'],
    url = 'https://github.com/imran9217',
    packages = ['Elite-Multiprocessing']
    )
