import re

def hello():
  return "hello"

def removeHashtag(tweetText: str) -> str:
  return re.sub(r'#.*', "", tweetText)

def removeUrl(tweetText: str) -> str:
  return re.sub(r'(https?)(:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)', "", tweetText)

def removeMention(tweetText: str) -> str:
  return re.sub(r'@[0-9a-zA-Z_:]*', "", tweetText)

# TODO
# def removeRetweet(tweetText: str) -> str: