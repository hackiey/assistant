import praw
from datetime import datetime

from assistant.agents.feeds.utils import Feeds, FeedsArticle, FeedsComment


reddit_content_template = '''subreddit: r/{subreddit}

# {title}

author: {author} / publish time: {publish_date} / flair: {flair} / upvotes: {votes}

# Content

{content}'''

reddit_comment_template = '''@{author} {reply_info} / publish date: {publish_date} / votes: {votes}
{content}'''


class RedditArticle(FeedsArticle):
    def __init__(self,
                 submission, 
                 comments_limit: int = 10,
                 replies_limit: int = 5,
                 depth_limit: int = 5
        ) -> None:

        self.submission = submission

        self.comments_limit = comments_limit
        self.replies_limit = replies_limit
        self.depth_limit = depth_limit

        link = f"https://www.reddit.com{submission.permalink}"

        content = self.get_content()
        
        format_keys = {
            "subreddit": submission.subreddit,
            "flair": submission.link_flair_text,
            "votes": submission.score,
            "content": content,
        }
        format_keys.update({key: f"{{{key}}}" for key in self.default_format_keys})
        template = reddit_content_template.format(**format_keys)

        self.comments_str = ""
        comments = []
        for comment in submission.comments[:self.comments_limit]:
            comment = self.get_comment(comment, depth=0)
            comments.append(comment)

        super().__init__(
            id=link,
            title=submission.title,
            author=submission.author,
            link=link,
            publish_time=int(submission.created_utc),
            content=content,
            comments=comments
        )

        self.contents = self.pack_contents(template)

    def get_comment(self, comment, depth: int = 0) -> 'RedditComment':
        replies = []

        if comment.replies is None:
            return RedditComment(comment, None)
        
        if depth >= self.depth_limit:
            return RedditComment(comment, None)
        
        for reply in comment.replies[:self.replies_limit]:
            reply = self.get_comment(reply, depth=depth+1)
            replies.append(reply)

        return RedditComment(comment, replies)

    def get_content(self) -> str:
        content = self.submission.selftext
        if self.submission.url != "":
            content += self.submission.url
        return content
    
    def __str__(self) -> str:
        return f"[{self.submission.subreddit}] {self.submission.title} {self.link}\n\n{self.content}"


class RedditComment(FeedsComment):
    def __init__(self,
                 comment: praw.models.Comment,
                 replies: list['RedditComment'] = None
        ) -> None:

        self.comment = comment
        self.replies = replies

        format_keys = {
            "votes": comment.score,
            "reply_info": f"reply to @{comment.parent().author}"
        }
        format_keys.update({key: f"{{{key}}}" for key in self.default_format_keys})
        template = reddit_comment_template.format(**format_keys)

        super().__init__(author=comment.author, 
                         publish_time=int(comment.created_utc), 
                         content=comment.body,
                         replies=replies)
        
        self.content = self.pack_comment(template)


class RedditFeeds(Feeds):
    def __init__(self, reddit_client, subreddit: dict):
        self.subreddit = subreddit['name']
        self.filters = subreddit['filters'] if 'filters' in subreddit else None

        self.comments_limit = 10
        self.replies_limit = 5
        self.replies_depth = 3

        self.reddit_client = reddit_client

    def get_feeds(self, limit: int = 20):
        for submission in self.reddit_client.subreddit(self.subreddit).hot(limit=limit):
            print(f"https://www.reddit.com{submission.permalink}")
            feeds = RedditArticle(submission)
            print(feeds)
        
        import ipdb;ipdb.set_trace()


def init_reddit_client(config):
    return praw.Reddit(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        user_agent=f"testscript by u/{config['username']}",
        username=config["username"],
        password=config["password"],
    )
