class Message(object):
    pass


class TextMessage(Message):
    def __init__(self):
        self._title = ""
        self._content = ""
        self._at_all = False

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def at_all(self):
        return self._at_all

    @at_all.setter
    def at_all(self, value):
        self._at_all = value


class MarkdownMessage(Message):

    def __init__(self):
        self._title = ""
        self._content = ""
        self._template = "red"
        self._at_all = False

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def at_all(self):
        return self._at_all

    @at_all.setter
    def at_all(self, value):
        self._at_all = value

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template = value
