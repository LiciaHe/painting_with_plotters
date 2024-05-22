import markdown,re
from markdown import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from bs4 import BeautifulSoup
def load_soups(original_name,template_loc):
    with open(f'{template_loc}.html',"r",encoding="utf-8") as basesf:
        template_soup=BeautifulSoup(basesf.read(), "html.parser")

    with open(f'{input_loc}{original_name}.md', 'r', encoding='utf-8') as input_file:
        markdown_text = input_file.read()

        html = markdown(markdown_text.replace(" "," "))
        content_soup = BeautifulSoup(html, "html.parser")
    return template_soup,content_soup

def name_treat(text):
    names=text.split("_")
    name=" ".join([v[0].upper()+v[1:].lower() for v in names])
    return name
def make_front_page(original_name,template_loc):
    template_soup, content_soup=load_soups(original_name,template_loc)
    #update title
    title_text=name_treat(original_name)
    title_tag=template_soup.find("title")
    title_tag.string=title_text





input_loc="../Course_Material/"
export_loc="../website/"
template_loc="front_page_template"
ori_name="00_Course_Overview"

make_front_page(
    "00_Course_Overview",
    template_loc
)


