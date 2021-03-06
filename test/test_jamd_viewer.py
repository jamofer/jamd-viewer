from unittest import TestCase

from jamd.github_markdown_template import GithubMarkdownTemplate
from jamd.jamd_viewer import Styles
from mock import patch, MagicMock

from jamd import jamd_viewer
from jamd import markdown_parser


class TestJamdViewer(TestCase):
    def setUp(self):
        self.markdown = patch('markdown.markdown').start()
        self.file_exists = patch('jamd.shell.file_exists').start()
        self.read_file = patch('jamd.shell.read_file').start()

        jamd_viewer.app.testing = True
        self.client = jamd_viewer.app.test_client()
        self.FlaskDesktopUI = patch('jamd.jamd_viewer.FlaskDesktopUI').start()

        self.flask_desktop_ui = MagicMock()
        self.FlaskDesktopUI.return_value = self.flask_desktop_ui

    def tearDown(self):
        patch.stopall()

    def test_it_parses_markdown_file_to_html(self):
        self.markdown.return_value = 'html_result'

        html = markdown_parser.to_html('something in markdown')

        self.markdown.assert_called_once_with('something in markdown', extensions=['extra'])
        assert html == 'html_result'

    def test_it_runs_flask_desktop_ui_serving_a_markdown_file(self):
        self.markdown.return_value = 'html_result'

        jamd_viewer.run('README.md')
        response = self.client.get('/')

        assert response.status_code == 200
        assert response.data == b'html_result'
        self.FlaskDesktopUI.assert_called_once_with(jamd_viewer.app)
        self.flask_desktop_ui.run.assert_called_once()

    def test_it_runs_flask_desktop_ui_serving_a_markdown_file_with_github_style(self):
        self.markdown.return_value = 'html_result'

        jamd_viewer.run('README.md', style=Styles.GITHUB)
        response = self.client.get('/')

        assert response.status_code == 200
        assert response.data.decode('utf-8') == GithubMarkdownTemplate('html_result').html
        self.FlaskDesktopUI.assert_called_once_with(jamd_viewer.app)
        self.flask_desktop_ui.run.assert_called_once()

    def test_it_runs_flask_desktop_ui_showing_file_not_found_error(self):
        self.file_exists.return_value = False
        self.markdown.return_value = 'html_result'

        jamd_viewer.run('non/existing/file.md', style=Styles.GITHUB)
        response = self.client.get('/')

        assert response.status_code == 200
        assert response.data.decode('utf-8') == GithubMarkdownTemplate('html_result').html
        self.FlaskDesktopUI.assert_called_once_with(jamd_viewer.app)
        self.flask_desktop_ui.run.assert_called_once()
        self.markdown.assert_called_once_with('File `non/existing/file.md` does not exist', extensions=['extra'])
