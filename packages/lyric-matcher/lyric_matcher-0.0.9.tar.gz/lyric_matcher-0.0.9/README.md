# Lyrics Matcher

## Overview

Lyrics Matcher is for getting the timestamp of the beginning of each lyric section.

## Installation

```sh
$ pip install lyric_matcher
```

## Usage

```python
>>> from lyricsmatcher import lyrics_matcher
>>> t = lyrics_matcher.findTimestamp('YRMU.txt','YRMUwithTime.txt')
>>> print(t)

"""
['[00:14.59]', '[00:45.75]', '[01:59.28]', '[03:01.19]', '[04:07.14]']
"""
```
