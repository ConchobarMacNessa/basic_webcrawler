from unittest import mock, TestCase, main
import requests
import crawler


class TestCrawlerFunctions(TestCase):

    def test_form_url_returns_url(self):
        crawler.base_url = 'http://testurl.com'
        actual = crawler.form_url('/blog')
        expected = 'http://testurl.com/blog'
        self.assertEqual(actual, expected)

    def test_form_url_returns_base_url_if_passed_in(self):
        crawler.base_url = 'http://testurl.com'
        actual = crawler.form_url('http://testurl.com')
        expected = 'http://testurl.com'
        self.assertEqual(actual, expected)

    def test_parse_html_links_returns_empty_list_on_bad_url(self):
        actual = crawler.parse_html_links('broken link')
        expected = []
        self.assertEqual(actual, expected)

    def test_filter_visited_links(self):
        crawler.visited_links = {'/', '/shop'}
        links = ['/', '/shop', '/blog', '/about']
        actual = crawler.filter_visited_links(links)
        expected = ['/blog', '/about']
        self.assertEqual(actual, expected)

    def test_add_to_site_map(self):
        crawler.site_map = {'endpoint1': []}
        crawler.add_to_site_map('endpoint2', ['link1', 'link2'])
        expected = {'endpoint1': [], 'endpoint2': ['link1', 'link2']}
        self.assertEqual(crawler.site_map, expected)


if __name__ == '__main__':
    main()
