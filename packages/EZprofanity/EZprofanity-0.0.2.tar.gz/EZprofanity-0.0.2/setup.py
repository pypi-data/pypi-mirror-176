import setuptools
import os
setuptools.setup(
    name="EZprofanity",
    long_description="""
# EZprofanity

Quickly detect profane, innapropriate and disgusting language!

Example:

```
from ezprofanity import check
text = "I shit a lot."
if check(text):
	for i in check(text):
		print(f"You said {i}! That is profane!")
>> You said shit! That is profane!
```

Try and edit the text to include multiple swear words to test it out if you want.

EZprofanity can also detect multiple variants of a word like:
sh1t
sh i t
etc...

You may also include other words:
```
from ezprofanity import check
text = "censoredword"
if check(text,include=["censoredword"]):
	print("Profane!")
>> Profane!
```

If you want to exclude something, you can also do that:
```
from ezprofanity import check
text = "Sh1t"
if check(text,exclude=["shit"]):
	print("Profane!")
else:
	print("OK!")
>> OK!
```
    """,
    long_description_content_type='text/markdown',
    version="0.0.2",
    author="Victor wolmarans",
    description="Easily check for profane and innapropriate words quickly."
)