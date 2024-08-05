from html2text import HTML2Text
import re


class HTML2TextWithTiers(HTML2Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tier = 1
        self.output_lines = []

    def o(self, data, puredata=1, preserve_space=False):
        """Override the original `o` method to include tier information."""
        if not self.quiet:
            clean_data = data.strip()
            if clean_data:
                if self.pre or preserve_space:
                    line = "Tier {}: {}".format(self.tier, clean_data)
                else:
                    line = "Tier {}: {}".format(self.tier, re.sub(r'\s+', ' ', clean_data))
                self.output_lines.append(line)
        if puredata and not self.pre and not self.quiet:
            self.outcount += 1

    def handle_starttag(self, tag, attrs):
        """Handle the start of a tag and possibly increase the tier."""
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'th']:
            self.tier = 1
        elif tag in ['ol', 'ul', 'li', 'dd', 'td', 'p']:
            self.tier += 1
        super().handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        """Handle the end of a tag and possibly decrease the tier."""
        if tag in ['ol', 'ul', 'li', 'dd', 'td', 'p']:
            self.tier -= 1
        super().handle_endtag(tag)

    def p(self):
        """Override the `p` method to add a line break."""
        if self.p_p == 0:
            self.p_p = 1
        elif self.p_p == 1:
            self.p_p = 0

    def get_output(self):
        """Get the processed output."""
        return "\n".join(self.output_lines)

# Usage
# converter = HTML2TextWithTiers()
# converter.feed(your_html_input)
# output = converter.get_output()
