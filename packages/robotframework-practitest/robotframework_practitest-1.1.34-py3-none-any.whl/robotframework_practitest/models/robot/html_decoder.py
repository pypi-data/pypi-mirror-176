from __future__ import annotations

import html.parser as html_parser


def extract_html(input_text) -> str:
    return input_text.replace('*HTML*', '')


class HTMLDecoder(html_parser.HTMLParser):
    def __init__(self, *, convert_charrefs=True):
        html_parser.HTMLParser.__init__(self, convert_charrefs=convert_charrefs)
        self._result_text = ''

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reset()

    def __str__(self):
        return self._result_text

    def _append_text(self, text):
        self._result_text += ('' if len(self._result_text) == 0 else ' ') + text

    def reset(self) -> None:
        super(HTMLDecoder, self).reset()
        self._result_text = ''

    def feed(self, data: str) -> None:
        super(HTMLDecoder, self).feed(data.replace('*HTML*', ''))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        print(f"Tag: {tag}; Attr: {attrs}")

    def handle_data(self, data: str) -> None:
        print(f"Data: {data}")
        self._append_text(data)
