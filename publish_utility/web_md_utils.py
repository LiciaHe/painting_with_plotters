import markdown,re
from markdown import markdown
from bs4 import BeautifulSoup

def load_soup(soup_loc):
    with open(f'{soup_loc}',"r",encoding="utf-8") as basesf:
        template_soup=BeautifulSoup(basesf.read(), "html.parser")
    return template_soup

def name_treat(text):
    names=text.split("_")
    name=" ".join([v[0].upper()+v[1:].lower() for v in names])
    return name

def applyAttrs(tag,attrs):
    for key in attrs:
        tag.attrs[key]=attrs[key]

def create_and_append_tag(soup,parent,name,attr):
    tag=soup.new_tag(name)
    applyAttrs(tag,attr)
    parent.append(tag)
    return tag

def process_hrefs(template_soup):
    a_coll=template_soup.findAll("a")
    for a in a_coll:
        a.attrs["target"]="_blank"


def convert_md_to_html(md_text):
    # Convert bold (**text** or __text__) to <strong>
    md_text = re.sub(r"(\*\*|__)(.*?)\1", r"<strong>\2</strong>", md_text)
    # Convert italic (*text* or _text_) to <em>
    md_text = re.sub(r"(\*|_)(.*?)\1", r"<em>\2</em>", md_text)
    # Convert links [text](url) to <a href="url">text</a>
    md_text = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a target="_blank" href="\2">\1</a>', md_text)
    return md_text

def process_links(soup,template_loc,level=2):
    links=soup.find_all("link")
    for link in links:
        href=link["href"]
        if not href.startswith(template_loc):
            href=template_loc+href

        style_tag=soup.new_tag("style")
        with open(href,"r") as css_file:
            style_string=css_file.read()


        level_text = "../" * level

        correct_font = f'src: url(\'{level_text}Straightline_full.woff\') format(\'woff\');'
        font_reg = r'src: url.*?;'

        style_string = re.sub(font_reg, correct_font, style_string)

        style_tag.string = style_string

        link_parent=link.parent
        link_parent.append(style_tag)
        # link_parent.extract(link)
        link.extract()
