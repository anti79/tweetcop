# tweetcop
A tool to scan Twitter profiles find tweets that contain hate speech/insults/threats using Perspective API. Sves dadta to a csv file.
# Setup
To use the tool, you will have to obtain API keys for both Perpective API:
  - perspectiveapi.com

  
then paste them into the source code (line 24 of scan.py)
and do `pip install -r requirements.txt` to install the dependencies.

# Usage
```
scan.py [-h] [-u USERNAME] [-n NUMBER] [--csv] [--nort]

Find reportable tweets by username.

options:
  -h, --help           show this help message and exit
  -u USERNAME, --username USERNAME, --user USERNAME
                        The Twitter handle of the account you want to search.
  -n NUMBER, --number NUMBER
                        Number of tweets to scan.
  --nort               Exclude retweets from the scan
```
