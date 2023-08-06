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