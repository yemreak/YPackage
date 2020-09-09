"""Kompleks metot testleri
"""

import pytest

from ...ypackage.model.markdown import Comment, Header, Indent, Link

# https://github.com/szabgab/slides/blob/main/python-programming/examples/pytest/test_class.py


class TestLink:

    def setup_class(self):
        self.content = "[name1](path1) [name2](path2)"

    def test_str(self):
        link = Link('name', 'path')
        expected = "[name](path)"

        assert str(link) == expected
        assert link.to_str() == expected

    def test_repr(self):
        link = Link('name', 'path')
        expected = "Link(name='name', path='path')"

        assert repr(link) == expected

    def test_map(self):
        content = Link.map(self.content, TestLink.do)
        expected = "[name1a](path1b) [name2a](path2b)"
        assert content == expected

    def test_find_all(self):
        links = Link.find_all(self.content)
        assert links == [Link('name1', 'path1'), Link('name2', 'path2')]

    def test_find_first(self):
        link = Link.find_first(self.content)
        assert link == Link('name1', 'path1')

    @staticmethod
    def do(link: Link):
        link.name += "a"
        link.path += "b"


class TestHeader():

    def setup_class(self):
        self.content = "# YEmreAk\n## YPackage\n"

    def test_error(self):
        with pytest.raises(TypeError):
            Header(0, "Name")

    def test_str(self):
        header = Header(1, "Name")
        expected = "# Name"

        assert str(header) == expected
        assert header.to_str() == expected

        header = Header(1, "Name")
        expected = "# Name"

        assert str(header) == expected
        assert header.to_str() == expected

        header = Header(2, "hey")
        expected = "## hey"

        assert str(header) == expected
        assert header.to_str() == expected

    def test_repr(self):
        header = Header(2, 'Name')
        expected = "Header(level=2, name='Name')"

        assert repr(header) == expected

    def test_map(self):
        content = Header.map(self.content, TestHeader.do)
        expected = "## YEmreAkY\n### YPackageY\n"
        assert content == expected

    def test_find_all(self):
        headers = Header.find_all(self.content)
        assert headers == [Header(1, 'YEmreAk'), Header(2, 'YPackage')]

    def test_find_first(self):
        header = Header.find_first(self.content)
        assert header == Header(1, 'YEmreAk')

    @staticmethod
    def do(header: Header):
        header.level += 1
        header.name += "Y"


class TestComment():

    def setup_class(self):
        self.content = "<!--Help--><!--Hi-->"

    def test_error(self):
        with pytest.raises(ValueError):
            Comment("-->")

    def test_str(self):
        comment = Comment("Name")
        expected = "<!--Name-->"

        assert str(comment) == expected
        assert comment.to_str() == expected

    def test_repr(self):
        comment = Comment('Name')
        expected = "Comment(content='Name')"

        assert repr(comment) == expected

    def test_map(self):
        content = Comment.map(self.content, TestComment.do)
        expected = "<!--HelpC--><!--HiC-->"
        assert content == expected

    def test_find_all(self):
        comments = Comment.find_all(self.content)
        assert comments == [Comment('Help'), Comment('Hi')]

    def test_find_first(self):
        comment = Comment.find_first(self.content)
        assert comment == Comment('Help')

    @staticmethod
    def do(comment: Comment):
        comment.content += "C"


class TestIndent():

    def setup_class(self):
        self.content = "    Selam\n    Hey   "

    def test_error(self):
        with pytest.raises(ValueError):
            Indent(-1)

        with pytest.raises(TypeError):
            Indent(1.1)

        with pytest.raises(TypeError):
            Indent((1, 2))

    def test_str(self):
        indent = Indent(1)
        expected = "  "

        assert str(indent) == expected
        assert indent.to_str() == expected

        indent = Indent(2)
        expected = "    "

        assert str(indent) == expected
        assert indent.to_str() == expected

        indent = Indent(3)
        expected = "      "

        assert str(indent) == expected
        assert indent.to_str() == expected

    def test_repr(self):
        indent = Indent(2)
        expected = "Indent(level=2)"

        assert repr(indent) == expected

    def test_map(self):
        with pytest.raises(NotImplementedError):
            Indent.map(self.content, TestIndent.do)
        # expected = "      Selam\n      Hey   "
        # assert content == expected

    def test_find_all(self):
        indents = Indent.find_all(self.content)
        assert indents == [Indent(2), Indent(2)]

    def test_find_first(self):
        indent = Indent.find_first(self.content)
        assert indent == Indent(2)

    @staticmethod
    def do(indent: Indent):
        indent.level += 1
