# This is obsolete due to a breaking change in the Twitter API.
----------
# tweetcop

A tool to scan Twitter profiles find tweets that contain hate speech/insults/threats using Perspective API. Saves data to a csv file.
# Setup
To use the tool, you will have to obtain an API key for Perpective API:
  - perspectiveapi.com

  
then paste it into the source code (line 23 of scan.py)
and do `pip install -r requirements.txt` to install the dependencies.

# Usage
```
scan.py [-h] [-u USERNAME] [-n NUMBER] [--nort]

Find reportable tweets by username.

options:
  -h, --help           show this help message and exit
  -u USERNAME, --username USERNAME, --user USERNAME
                        The Twitter handle of the account you want to search.
  -n NUMBER, --number NUMBER
                        Number of tweets to scan.
  --nort               Exclude retweets from the scan
```
