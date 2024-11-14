from assistant.core.agent import Agent
from assistant.agents.feeds.reddit import RedditFeeds, init_reddit_client


class FeedsAgent(Agent):
    def __init__(self, sources, auths_config) -> None:
        self.sources = []

        for source in sources:
            if source['source'] == "reddit":

                reddit_client = init_reddit_client(auths_config['feeds']['reddit'])

                for subreddit in source['subreddits']:
                    self.sources.append(RedditFeeds(reddit_client, subreddit))

    def get_feeds(self):
        for source in self.sources:
            source.get_feeds()

    def run_task(self):
        self.get_feeds()
