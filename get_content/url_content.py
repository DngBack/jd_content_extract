"""
convert_to_md module
"""
import html2text
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests

def convert_to_md(html: str, url: str = None) -> str:
    """ Convert HTML to Markdown.
    This function uses the html2text library to convert the provided HTML content to Markdown 
    format.
    The function returns the converted Markdown content as a string.

    Args: html (str): The HTML content to be converted.

    Returns: str: The equivalent Markdown content.

    Example: >>> convert_to_md("<html><body><p>This is a paragraph.</p>
    <h1>This is a heading.</h1></body></html>") 
    'This is a paragraph.\n\n# This is a heading.'

    Note: All the styles and links are ignored during the conversion. """

    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.body_width = 0
    if url is not None:
        parsed_url = urlparse(url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        h.baseurl = domain
    
    return h.handle(html)

source = 'https://www.rakus.co.jp/company/map/'

response = requests.get(source)
soup = BeautifulSoup(response.text, 'html.parser')

parsed_content = response.text

parsed_content = convert_to_md(parsed_content, source)
print(parsed_content)
