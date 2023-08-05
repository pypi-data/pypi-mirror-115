# https://bucharjan.cz/blog/using-cython-to-protect-a-python-codebase.html

from setuptools import setup

# https://packaging.python.org/guides/distributing-packages-using-setuptools/
setup(
    name="passk",
    version="1.6",
    description="Keeps things s.",
    author="APC",
    author_email="apc.internet@pm.me",
    license='MIT',
    long_description="",
    packages=['passk'],
    install_requires=['pycryptodome','dropbox','pbkdf2','pyperclip'],
    keywords='',
    #packages=find_packages(),
    python_requires='>=3',
)
