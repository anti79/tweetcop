from googleapiclient import discovery
import json
import twint
from time import sleep
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Find reportable tweets by username.')

parser.add_argument('-u', '--username', '--user', action="store", type=str, dest="username",
                    default=False, help="The Twitter handle of the account you want to search.")

parser.add_argument('-n', '--number', action="store", type=int, dest="number",
                    default=False, help="Number of tweets to scan.")

parser.add_argument('--csv', action="store_true", dest="csv",
                    default=False, help="Save data to a .csv file")

parser.add_argument('--nort', action="store_true", dest="nort",
                    default=False, help="Exclude retweets from scanning")

args = parser.parse_args()

#Enter your API keys here:
API_KEY = ''  # perspective
TW_API_KEY = '' #twitter
TW_SECRET = ''
TW_BEAR = ''
TW_AT = ''
TW_AT_SECRET = ''




# models:
# TOXICITY SEVERE_TOXICITY IDENTITY_ATTACK INSULT PROFANITY THREAT
# LIKELY_TO_REJECT INFLAMMATORY ATTACK_ON_AUTHOR ATTACK_ON_COMMENTER


def eval_text(text: str, models: list):

		attributes = {}
		for model in models:
			attributes[model] = {}

		analyze_request = {
			'comment': {'text': text},
			'requestedAttributes': attributes
		}

		response = client.comments().analyze(body=analyze_request).execute()
		results = {}
		for attr in response["attributeScores"]:
			results[attr] = round(response["attributeScores"][attr]["summaryScore"]["value"], 4)
		return results

username = args.username
if not args.username:
	print("No username provided.")
	quit()

rated_tweets = []

client = discovery.build(
	"commentanalyzer",
	"v1alpha1",
	developerKey=API_KEY,
	discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
	static_discovery=False,
)

def get_tweets(username:str):
	c = twint.Config()
	c.Limit = args.number
	#c.Since = '2017-12-27'
	c.Retweets = not args.nort
	c.Username = username
	c.Store_object = True
	c.Hide_output = True
	twint.run.Search(c)
	#twint.run.Profile(c)
	return twint.output.tweets_list


def shorten_link(link:str):
	arr = link.split('/')
	arr[3] = 't'
	return '/'.join(arr)


user_tweets = get_tweets(username)
user_tweets = user_tweets[:args.number]
for i, tweet in enumerate(user_tweets):
	rated_tweet = {}
	rated_tweet["tweet"] = tweet
	print(f"Evaluating tweet {i} of {len(user_tweets)}")
	if tweet.user_rt_id != '' and args.nort:
		continue
	try:
		rated_tweet["results"] = eval_text(tweet.tweet, ['TOXICITY', 'IDENTITY_ATTACK', 'SEVERE_TOXICITY', 'THREAT'])
	except Exception as e:
		print("An exception occured during proccessing: ")
		print(e)
		print("Continuing...")
		sleep(1)
		continue
	total = 0
	for key in rated_tweet["results"]:
		total += rated_tweet["results"][key]
	rated_tweet["results"]["TOTAL"] = round(total, 4)
	rated_tweets.append(rated_tweet)
	sleep(0.7)

print("Done.")
sorted_results = sorted(rated_tweets, key=lambda x: x["results"]['TOTAL'], reverse=True)

# prepare for conversion
dic = {'Text':[], 'Link':[]}
for attr in sorted_results[0]["results"]:
	dic[attr] = []
for i, res in enumerate(sorted_results):
	dic['Text'].append(res["tweet"].tweet)
	dic['Link'].append(shorten_link(res["tweet"].link))
	for attr in res["results"]:
		dic[attr].append(res["results"][attr])

pd.options.display.max_colwidth = 60
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', None)
df = pd.DataFrame(dic)
print(df)

if args.csv:
	df.to_csv(
		path_or_buf=f'{args.username}.csv',
		sep=',',
		header=True,
		index=True
	)
	print("Exported to " + f'{args.username}.csv')

