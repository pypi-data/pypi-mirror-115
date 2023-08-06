from setuptools import setup
import sys

if sys.version_info[0] < 3:
    with open('README.md') as f:
        long_description = f.read()
else:
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()

setup(name="clever_chat",
version="1.0.0",
description="An API Wrapper for clever-chat (chatbot) in Python",
long_description=long_description,
long_description_content_type='text/markdown',
author="Pr0methium",
url="https://github.com/XPr0methiumX/Clever-chat",
packages=['clever_chat'],
install_requires=['aiohttp', 'requests'],
keywords=['python', 'chatbot', 'chat'],
classifiers=['Development Status :: 5 - Production/Stable',
"Intended Audience :: Developers",
"Programming Language :: Python :: 3",
"Operating System :: OS Independent"],
license="MIT")