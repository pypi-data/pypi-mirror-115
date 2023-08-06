from setuptools import setup


setup(name='ask_me_something',
version='0.1.1',
description="""A speech to text library.""",
long_description="""
# Ask Me Something
A speech to text library.
# Install
```
pip3 install ask-me-something
```
# Using
The ask function prints and returns the recognized content
## In another script
```python
from ask_me_something import ask

# ask(text = "Say something to mic", language = "en-en")

ask()
```
## In command line
```console
  -h, --help            show this help message and exit
  -l LANGUAGE, --language LANGUAGE
                        Language
```

```console
ask
```
""",
long_description_content_type='text/markdown',
url='https://github.com/onuratakan/ask_me_something',
author='Onur Atakan ULUSOY',
author_email='atadogan06@gmail.com',
license='MIT',
packages=["ask_me_something"],
package_dir={'':'src'},
install_requires=[
    "SpeechRecognition==3.8.1",
    "PyAudio==0.2.11",
],
entry_points = {
    'console_scripts': ['ask=ask_me_something.ask_me_something:ask'],
},
python_requires=">= 3, < 3.7",
zip_safe=False)
