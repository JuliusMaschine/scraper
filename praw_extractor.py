import praw
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Create a reddit instance
data = {}
reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'),
                     client_secret=os.getenv('CLIENT_SECRET'),
                     user_agent='watcherbot')

# Get the top posts from the subreddit
subreddit = reddit.subreddit('SUBREDDIT')
hot_list = subreddit.hot(limit=100)
data['patterns'] = []
data['responses'] = []

# Loop through the posts
def scrape():
    for submissions in hot_list:
        num_title = 1

        # Get the title of the post and exclude the stickied post
        if not submissions.stickied:

            num_title += 1
            num_com = 0
            data['patterns'].append(submissions.selftext)
            comments = submissions.comments.list()[:10]

            # Loop through the comments
            for comment in comments:
                num_com += 1

                # Ignores the MoreComments object
                if isinstance(comment, praw.models.MoreComments):
                    continue

                # Get the comment text and append it to the list as responses to the submission
                data['responses'].append(comment.body)

scrape()

# write the data to a json file
if __name__ == '__main__':
    with open("training.json", "w") as outfile:
        json.dump(data, outfile)
