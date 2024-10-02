import os
import praw
from dotenv import load_dotenv
from langchain_community.document_loaders import RedditPostsLoader

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")


# if __name__ == "__main__":

#     reddit = praw.Reddit(
#         client_id=REDDIT_CLIENT_ID,
#         client_secret=REDDIT_CLIENT_SECRET,
#         user_agent=f"testscript by u/{REDDIT_USERNAME}",
#         username=REDDIT_USERNAME,
#         password=REDDIT_PASSWORD,
#     )

#     for submission in reddit.subreddit("openai").hot(limit=20):
#         # print(submission.title)
#         # print("id", submission.id)
#         # print("is_self", submission.is_self)
#         # print("name", submission.name)
#         # print("num_comments", submission.num_comments)
#         # print("author_flair_text", submission.author_flair_text)
#         # print("link_flair_text", submission.link_flair_text)
#         # print("permalink", f"https://www.reddit.com{submission.permalink}")
#         # print("url", submission.url)
#         # print("created_utc", submission.created_utc)
#         # print("score", submission.score)
#         # print("upvote_ratio", submission.upvote_ratio)
#         # print(submission.selftext)

#         for comment in submission.comments:
#             print(comment.cre)
#             print(comment.author)
#             print(comment.body)
#         print("==============")


if __name__ == "__main__":
    # load using 'subreddit' mode
    loader = RedditPostsLoader(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent="extractor by u/Master_Ocelot8179",
        categories=["new", "hot"],  # List of categories to load posts from
        mode="subreddit",
        search_queries=[
            "openai",
        ],  # List of subreddits to load posts from
        number_posts=20,  # Default value is 10
    )
    documents = loader.load()
    # documents[:5]
    for d in documents:
        print(d)

    # # or load using 'username' mode
    # loader = RedditPostsLoader(
    #     client_id="YOUR CLIENT ID",
    #     client_secret="YOUR CLIENT SECRET",
    #     user_agent="extractor by u/Master_Ocelot8179",
    #     categories=['new', 'hot'],
    #     mode = 'username',
    #     search_queries=['ga3far', 'Master_Ocelot8179'],         # List of usernames to load posts from
    #     number_posts=20
    #     )

    # Note: Categories can be only of following value - "controversial" "hot" "new" "rising" "top"