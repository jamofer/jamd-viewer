from jamd import shell


GITHUB_MARKDOWN_CSS_PATH = shell.path(shell.folder_from(__file__), 'github-markdown-css.min.css')


class GithubMarkdownTemplate(object):
    header = '''
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        .markdown-body {
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px;
        }
    
        @media (max-width: 767px) {
            .markdown-body {
                padding: 15px;
            }
        }
    </style>
    '''

    github_markdown_css = f'''
    <style>
        {shell.read_file(GITHUB_MARKDOWN_CSS_PATH)}
    </style>
    '''

    def __init__(self, markdown_html):
        self.markdown_html = markdown_html

    @property
    def html(self):
        content = f'''
        <article class="markdown-body">
            {self.markdown_html}
        </article>
        '''

        return self.header + self.github_markdown_css + content
