import re
from datetime import datetime


content_template = '''# [{title}]({link})

author: {author} / publish time: {publish_date}

# Content
{content}'''


class News:
    default_format_keys = ['title', 'author', 'publish_date', 'content', 'comments']

    def __init__(self, 
                 id: str,
                 title: str = None, 
                 author: str = None, 
                 link: str = None,
                 publish_time: int = None,
                 content: str = None, 
                 comments: list['NewsComment'] = None
        ) -> None:
        self.id = id

        self.title = title
        self.author = author
        self.link = link
        self.publish_time = publish_time
        self.content = content
        self.comments = comments

    def summarize(self):
        pass

    def pack_contents(self, template: str = None):
        if template is None:
            template = content_template

        publish_date = datetime.fromtimestamp(self.publish_time).strftime('%Y-%m-%d %H:%M')

        self.content = template.format(
            title=self.title,
            link=self.link,
            author=self.author,
            publish_date=publish_date,
            content=self.content
        )

        if len(self.comments) > 0:
            self.content += "\n\n# Comments"
            for i, comment in enumerate(self.comments):
                self.content += f"\n\n--- comment {i+1} ---"
                self.content += self.get_comment_content(comment, depth=0)
                
        # 按照content中的image url, png/jpg/webp/gif，分割文本
        image_urls = re.findall(r'(http[s]?:\/\/.*\.(?:png|jpg|jpeg|webp|gif))', self.content)

        contents = []
        for image_url in image_urls:
            _contents = self.content.split(image_url)
            for _content in _contents[:-1]:
                if _content != "":
                    contents.append({"type": "text", "text": _content})

                contents.append({"type": "image_url", "image_url": {"url": image_url, "detail": "high"}})

            if _contents[-1] != "":
                contents.append({"type": "text", "text": _contents[-1]})

        return contents
    
    def get_comment_content(self, comment, depth: int = 0):
        comment_content = f"\n\n{'> '*depth}{comment.content}"
        if comment.replies is not None:
            for reply in comment.replies:
                # comment_content += f"\n\n{reply.content}"
                comment_content += self.get_comment_content(reply, depth=depth+1)

        return comment_content

        
comment_template = '''author: {author} / publish time: {publish_time}

{content}'''

class NewsComment:
    default_format_keys = ['author', 'publish_date', 'content', 'replies']

    def __init__(self, 
                 author: str = None, 
                 publish_time: int = None, 
                 content: str = None,
                 replies: list['NewsComment'] = None
        ) -> None:

        self.author = author
        self.publish_time = publish_time
        self.content = content
        self.replies = replies

    def pack_comment(self, template: str = None):
        content = template.format(
            author=self.author,
            publish_date=datetime.fromtimestamp(self.publish_time).strftime('%Y-%m-%d %H:%M'),
            content=self.content,
        )

        return content
