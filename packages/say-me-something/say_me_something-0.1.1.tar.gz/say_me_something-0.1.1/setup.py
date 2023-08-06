from setuptools import setup

from setuptools import setup



setup(name='say_me_something',
version='0.1.1',
description="""A text to speak library with embedded cache system.""",
long_description="""
# Say Me Something
A text to speak library with embedded cache system.
# Install
```
pip3 install say-me-something
```
# Using
## In another script
```python
from say_me_something import say

# say(text = None, language = "en", no_cache = False, reset = False, no_speak = False)

say("Hello")
```
## In command line
```console
  -h, --help            show this help message and exit
  -t TEXT [TEXT ...], --text TEXT [TEXT ...]
                        Text
  -l LANGUAGE, --language LANGUAGE
                        Language
  -nc, --nocache        No cache
  -r, --reset           Reset (removing the caches)
  -ns, --nospeak        No speak
```

```console
say -t Hello
```
""",
long_description_content_type='text/markdown',
url='https://github.com/onuratakan/say_me_something',
author='Onur Atakan ULUSOY',
author_email='atadogan06@gmail.com',
license='MIT',
packages=["say_me_something"],
package_dir={'':'src'},
package_data={
    "say_me_something" : ["cache/*.mp3"],
},
install_requires=[
    "click==8.0.1",
    "gTTS==2.2.3",
    "playsound==1.3.0",
    "pyttsx3==2.90",
],
entry_points = {
    'console_scripts': ['say=say_me_something.say_me_something:say'],
},
python_requires='>=3',
zip_safe=False)
