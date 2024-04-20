import os
import unittest
from unittest import TestCase, mock
from unittest.mock import patch, mock_open
from wiki.core import clean_url, wikilink, Processor, Page, Wiki


class TestCleanUrl(unittest.TestCase):
    def test_clean_url(self):
        # Test various scenarios
        self.assertEqual(clean_url("  Example Page  "), "example_page")
        self.assertEqual(clean_url("Example    Page"), "example_page")
        self.assertEqual(clean_url("Example\\Page"), "example/page")
        self.assertEqual(clean_url("Example\\\\Page"), "example/page")

class TestWikiLink(unittest.TestCase):
    def test_wikilink_simple(self):
        text = "This is a test [[Page]]"
        with patch('flask.url_for', return_value="/wiki/page"):
            result = wikilink(text)
        self.assertIn('<a href="/wiki/page">Page</a>', result)

class TestPage(unittest.TestCase):
    def setUp(self):
        self.page = Page('/fake/path', 'TestPage')

    @patch('os.open', new_callable=mock_open, read_data="title: Test Page\n\nContent")
    def test_load(self, mock_file):
        self.page.load()
        self.assertIn('Content', self.page.content)

    @patch('os.makedirs')
    @patch('os.open', new_callable=mock_open)
    def test_save(self, mock_file, mock_makedirs):
        self.page.save()
        mock_file().write.assert_called_with("\nContent")

class TestWiki(unittest.TestCase):
    def setUp(self):
        self.wiki = Wiki('/fake/root')

    @patch('os.path.exists', return_value=True)
    def test_exists(self, mock_exists):
        result = self.wiki.exists('TestPage')
        self.assertTrue(result)

    @patch('os.walk')
    def test_index(self, mock_walk):
        mock_walk.return_value = [('/fake/root', ('dir',), ['TestPage.md'])]
        result = self.wiki.index()
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Page)

    @patch('os.rename')
    @patch('os.makedirs')
    def test_move(self, mock_makedirs, mock_rename):
        self.wiki.move('oldurl', 'newurl')
        mock_rename.assert_called_once()

if __name__ == '__main__':
    unittest.main()
