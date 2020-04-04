"""Kompleks metot testleri
"""

import unittest

import pytest

from ...ypackage.model.markdown import Comment, Header, Indent, Link


class LinkTest(unittest.TestCase):

    def setUp(self):
        self.content = "[name1](path1) [name2](path2)"

    def test_str(self):
        link = Link('name', 'path')
        expected = "[name](path)"

        self.assertEqual(str(link), expected)
        self.assertEqual(link.to_str(), expected)

    def test_repr(self):
        link = Link('name', 'path')
        expected = "Link(name='name', path='path')"

        self.assertEqual(repr(link), expected)

    def test_map(self):
        content = Link.map(self.content, LinkTest.do)
        expected = "[name1a](path1b) [name2a](path2b)"
        self.assertEqual(content, expected)

    def test_find_all(self):
        links = Link.find_all(self.content)
        self.assertEqual(links, [Link('name1', 'path1'), Link('name2', 'path2')])

    def test_find_first(self):
        link = Link.find_first(self.content)
        self.assertEqual(link, Link('name1', 'path1'))

    @staticmethod
    def do(link: Link):
        link.name += "a"
        link.path += "b"


class HeaderTest(unittest.TestCase):

    def setUp(self):
        self.content = "# YEmreAk\n## YPackage\n"

    def test_error(self):
        with pytest.raises(TypeError):
            Header(0, "Name")

    def test_str(self):
        header = Header(1, "Name")
        expected = "# Name"

        self.assertEqual(str(header), expected)
        self.assertEqual(header.to_str(), expected)

        header = Header(1, "Name")
        expected = "# Name"

        self.assertEqual(str(header), expected)
        self.assertEqual(header.to_str(), expected)

        header = Header(2, "hey")
        expected = "## hey"

        self.assertEqual(str(header), expected)
        self.assertEqual(header.to_str(), expected)

    def test_repr(self):
        header = Header(2, 'Name')
        expected = "Header(level=2, name='Name')"

        self.assertEqual(repr(header), expected)

    def test_map(self):
        content = Header.map(self.content, HeaderTest.do)
        expected = "## YEmreAkY\n### YPackageY\n"

        self.assertEqual(content, expected)

    def test_find_all(self):
        headers = Header.find_all(self.content)

        self.assertEqual(headers, [Header(1, 'YEmreAk'), Header(2, 'YPackage')])

    def test_find_first(self):
        header = Header.find_first(self.content)
        self.assertEqual(header, Header(1, 'YEmreAk'))

    @staticmethod
    def do(header: Header):
        header.name += "Y"
        header.level += 1


class CommentTest(unittest.TestCase):

    def setUp(self):
        self.content = "<!--Help--><!--Hi-->"

    def test_error(self):
        with pytest.raises(ValueError):
            Comment("-->")

    def test_str(self):
        comment = Comment("Name")
        expected = "<!--Name-->"

        self.assertEqual(str(comment), expected)
        self.assertEqual(comment.to_str(), expected)

    def test_repr(self):
        comment = Comment('Name')
        expected = "Comment(content='Name')"

        self.assertEqual(repr(comment), expected)

    def test_map(self):
        content = Comment.map(self.content, CommentTest.do)
        expected = "<!--HelpC--><!--HiC-->"

        self.assertEqual(content, expected)

    def test_find_all(self):
        comments = Comment.find_all(self.content)

        self.assertEqual(comments, [Comment('Help'), Comment('Hi')])

    def test_find_first(self):
        comment = Comment.find_first(self.content)
        self.assertEqual(comment, Comment('Help'))

    @staticmethod
    def do(comment: Comment):
        comment.content += "C"


class IndentTest(unittest.TestCase):

    def setUp(self):
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

        self.assertEqual(str(indent), expected)
        self.assertEqual(indent.to_str(), expected)

        indent = Indent(2)
        expected = "    "

        self.assertEqual(str(indent), expected)
        self.assertEqual(indent.to_str(), expected)

        indent = Indent(3)
        expected = "      "

        self.assertEqual(str(indent), expected)
        self.assertEqual(indent.to_str(), expected)

    def test_repr(self):
        indent = Indent(2)
        expected = "Indent(level=2)"

        self.assertEqual(repr(indent), expected)

    def test_map(self):
        with pytest.raises(NotImplementedError):
            Indent.map(self.content, IndentTest.do)
        # expected = "      Selam\n      Hey   "
        # self.assertEqual(content, expected)

    def test_find_all(self):
        indents = Indent.find_all(self.content)
        self.assertEqual(indents, [Indent(2), Indent(2)])

    def test_find_first(self):
        indent = Indent.find_first(self.content)
        self.assertEqual(indent, Indent(2))

    @staticmethod
    def do(indent: Indent):
        indent.level += 1
