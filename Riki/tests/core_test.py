import unittest
from wiki.core import clean_url, wikilink, Processor, Page, Wiki


class TestWikiCore(unittest.TestCase):

    def test_clean_url(self):
        self.assertEqual(clean_url(" Hello  World \\Test "), "hello_world_/test")
        self.assertEqual(clean_url("multiple    spaces"), "multiple_spaces")
        self.assertEqual(clean_url("No Change Needed"), "no_change_needed")

    def test_wikilink(self):
        url_formatter = lambda endpoint, **values: f"/wiki/{values['url']}"
        input_text = "Check out this [[Wiki Link]] and this [[example/page|Example Page]]."
        expected_output = ("Check out this <a href='/wiki/wiki_link'>Wiki Link</a> "
                           "and this <a href='/wiki/example/page'>Example Page</a>.")
        self.assertEqual(wikilink(input_text, url_formatter), expected_output)

    def test_processor_full_cycle(self):
        text = "Meta: Value\n\n# Heading\nContent goes here."
        processor = Processor(text)
        final_output, markdown, meta = processor.process()
        self.assertIn('<h1>Heading</h1>', final_output)
        self.assertEqual(meta['meta'], 'Value')

    def test_page_load_render(self):
        page = Page(path='path/to/test.md', url='test-url', new=True)
        page.content = "Meta: Value\n\n# Heading\nContent goes here."
        page.render()
        self.assertIn('<h1>Heading</h1>', page.html)

    def test_wiki_page_management(self):
        wiki = Wiki(root='/fake/dir')
        wiki.get_or_404("nonexistent")
        self.assertRaises(FileNotFoundError)


if __name__ == "__main__":
    unittest.main()
