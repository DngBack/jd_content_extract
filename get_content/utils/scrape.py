import html2text

def scrape_html(html_str: str = "",
                ignore_links: bool = True,
                ignore_images: bool = True) -> str:
    """
    Converts an HTML string into string text while 
        optionally ignoring links and images.

    Parameters:
    html_str (str): The HTML content to be converted to plain text.
    ignore_links (bool): Links in the HTML content will be ignored.
    ignore_images (bool): Images in the HTML content will be ignored.

    Returns:
    str: The plain text content extracted from the HTML string.

    Example:
    >>> html_content = "<p>Hello, <a href='https://example.com'>click here</a> to visit our site.</p>"
    >>> scrape_html(html_content, ignore_links=True, ignore_images=True)
    'Hello, click here to visit our site.'
    """
    get_html_content = html2text.HTML2Text()
    get_html_content.ignore_images = ignore_images
    get_html_content.ignore_links = ignore_links

    content_html = get_html_content.handle(html_str)
    return content_html