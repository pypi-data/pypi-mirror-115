from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'Log/print your status and messages on terminal'
LONG_DESCRIPTION = 'A package that allows to log/print your status and messages for a python application on terminal in a standard yet customizable format.'

# Setting up
setup(
    name="pyshell-msg",
    version=VERSION,
    author="Ellipsion (Ashish Kumawat)",
    author_email="<ellipsion@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'pyshell_msg', 'status', 'shell', 'messages', 'application', 'logs', 'status', 'print', 'format'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)