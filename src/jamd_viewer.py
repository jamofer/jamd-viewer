import os
from argparse import ArgumentParser

from flask import Flask
from flask_desktop_ui import FlaskDesktopUI

import markdown_parser


app = Flask(__name__)


def run(path):
    markdown_contents = ''

    if os.path.exists(path):
        with open(path) as file:
            markdown_contents = file.read()

    @app.route('/')
    def markdown_in_html_endpoint():
        return markdown_parser.to_html(markdown_contents)

    FlaskDesktopUI(app).run()


def parse_arguments():
    arguments = ArgumentParser()
    arguments.add_argument('path', help='Markdown file to be opened')

    return arguments.parse_args()


if __name__ == '__main__':
    arguments = parse_arguments()
    run(arguments.path)
