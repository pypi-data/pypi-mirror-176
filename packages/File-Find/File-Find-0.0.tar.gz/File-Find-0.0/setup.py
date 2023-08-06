from setuptools import setup

setup(
    name='File-Find',
    version='0.0',
    packages=['File-Find'],
    url='https://gitlab.com/Pixel-Mqster/File-Find',
    license='GNU GPL v3.0',
    author='Pixel Master',
    author_email='',
    description='A macOS UI Utility for finding Files',
    keywords=['gui', 'executable'],
    include_package_data=True,
    install_requires=['pyqt6', 'pyperclip'],
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: MacOS",
    ]
    
)
