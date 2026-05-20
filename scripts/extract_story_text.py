"""Extract plain story text from HTML files and save as markdown for TTS."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class StoryParser(HTMLParser):
    SKIP_CLASSES = {"divider", "ending", "scene-break", "coda"}

    def __init__(self):
        super().__init__()
        self.in_story = False
        self.in_element = False
        self.skip_depth = 0
        self.current_tag = None
        self.current_text = []
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = set(attrs_dict.get("class", "").split())

        if tag == "section" and "story" in classes:
            self.in_story = True
            return

        if not self.in_story:
            return

        if classes & self.SKIP_CLASSES:
            self.skip_depth += 1
            return

        if self.skip_depth:
            return

        if tag in ("p", "h2"):
            self.in_element = True
            self.current_tag = tag
            self.current_text = []

    def handle_endtag(self, tag):
        if not self.in_story:
            return

        if tag == "section":
            self.in_story = False
            return

        if tag == "div" and self.skip_depth:
            self.skip_depth -= 1
            return

        if tag in ("p", "h2") and self.in_element:
            self.in_element = False
            text = "".join(self.current_text).strip()
            if text:
                if self.current_tag == "h2":
                    self.parts.append(f"\n## {text}\n")
                else:
                    self.parts.append(text)

    def handle_data(self, data):
        if self.in_element and not self.skip_depth:
            self.current_text.append(data)


def html_to_markdown(html: str) -> str:
    parser = StoryParser()
    parser.feed(html)
    return "\n\n".join(p for p in parser.parts if p.strip())


def main():
    root = Path(__file__).parent.parent
    stories_dir = root / "stories"
    src_dir = root / "src"
    src_dir.mkdir(exist_ok=True)

    pattern = sys.argv[1] if len(sys.argv) > 1 else "a2-part*.html"
    files = sorted(stories_dir.glob(pattern))

    if not files:
        print(f"No files matched: {stories_dir / pattern}")
        return

    for html_path in files:
        stem = html_path.stem  # e.g. a2-part1
        md_path = src_dir / f"{stem}.md"
        text = html_to_markdown(html_path.read_text())
        md_path.write_text(text + "\n")
        print(f"  wrote: {md_path.relative_to(root)}")


if __name__ == "__main__":
    main()
