## tweet preprocesser

## install
```
$ pip install tweet-preprocesser
```

## usage

```python
from tweet_preprocesser import preprocesser

print(preprocesser.removeHashtag("hogehoge #huga"))
# " hogehoge"

print(preprocesser.removeUrl("hogehoge http://example.com/?user=1#hoge https://example.com/?user=1#hoge"))
# "hogehoge  "

print(preprocesser.removeMention("@taro hello"))
# " hello"

```