import pandas as pd
import numpy as np
import reticker
import sys
import praw

re = reticker.TickerExtractor()

reddit = praw.Reddit(
    client_id=sys.argv[1],
    client_secret=sys.argv[2],
    password=sys.argv[3],
    user_agent=sys.argv[4],
    username=sys.argv[5],
)

columns = ['title', 'score', 'id', 'url']

df = pd.DataFrame(columns=columns)

expand = lambda a : {item:getattr(a, item) for item in columns} #[a.title, a.score, a.id, a.url]
# Output score for the first 256 items on the frontpage
for submission in reddit.subreddit("Shortsqueeze").new(limit=200):
    post_dict = expand(submission)
    tickers = re.extract(post_dict['title'])
    if tickers == []:
        print(post_dict['title'])
    df = df.append(post_dict, ignore_index = True)

df.to_pickle('./data/dump')

print(df.head())