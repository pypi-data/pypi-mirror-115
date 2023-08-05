import abc
import json


class Message(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def to_json(self):
        pass


class TextMessage(Message):
    def __init__(self):
        self._title = None
        self._content = None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value: str):
        self._content = value

    def to_json(self):
        if self.title is None or self.content is None:
            raise AttributeError("title or content is null")
        return json.dumps({"msg_type": "text", "content": {"title": self.title, "text": self._content}})


class MarkdownMessage(Message):
    def __init__(self):
        self._title = None
        self._content = None
        self._template = "red"

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, template: str):
        self._template = template

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value: str):
        self._content = value

    def to_json(self):
        if self.title is None or self.content is None:
            raise AttributeError("title or content is null")
        return json.dumps({"msg_type": "interactive",
                           "card": {
                               "header": {
                                   "title": {
                                       "tag": "plain_text",
                                       "content": self.title
                                   },
                                   "template": self.template
                               },
                               "elements": [{
                                   "tag": "markdown",
                                   "content": self.content
                               }]
                           }
                           })
