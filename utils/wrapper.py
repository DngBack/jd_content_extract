from textwrap import wrap

def skipwrap(text):
    """Check if the paragraph should be skipped for wrapping."""
    return False  # Always wrap the paragraph

def onlywhite(text):
    """Check if the paragraph contains only whitespace."""
    return text.strip() == ''

class Wrapper:
    def __init__(self, body_width):
        """
        Initialize the Wrapper class.

        Parameters:
        body_width (int): The width to which the text should be wrapped.
        """
        self.body_width = body_width

    def optwrap(self, text):
        """Wrap all paragraphs in the provided text with custom formatting."""
        if not self.body_width:
            return text
        assert wrap, "Requires Python 2.3."
        result = ''
        level = 1  # Start with level 1
        for para in text.split("\n"):
            if len(para) > 0:
                # Custom formatting logic based on the content
                if "://" in para:  # URLs
                    result += f"level {level}:    * {para}\n"
                    level += 1
                elif "■" in para or "■" in para:  # Bullet points
                    result += f"level {level + 1}:        {para}\n"
                elif "###" in para:  # Section headings
                    level = 1
                    result += f"level {level}:  {para.replace('###', '').strip()}\n"
                    level += 1
                else:
                    if not skipwrap(para):
                        result += f"level {level}:  {para}\n"
                        level += 1
                    else:
                        result += f"level {level + 1}:      {para}\n"
                        level += 1
            else:
                # Add a blank line to separate paragraphs
                result += "\n"
        return result
