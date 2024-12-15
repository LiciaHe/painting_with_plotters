import markdown,re
from markdown import markdown
from bs4 import BeautifulSoup


from copy_util import *

from web_md_utils import *
def load_soups(original_name,template_loc):
    with open(f'{template_loc}.html',"r",encoding="utf-8") as basesf:
        template_soup=BeautifulSoup(basesf.read(), "html.parser")

    with open(f'{input_loc}{original_name}.md', 'r', encoding='utf-8') as input_file:
        markdown_text = input_file.read().replace("Â "," ").replace(" "," ")
    return template_soup,BeautifulSoup(markdown(markdown_text),"html.parser")







    #make sure the font href is correct
def create_title(template_soup,content_soup):
    title_tag=template_soup.find("title")
    title_content_tag=content_soup.find("h1")

    title_tag.string=title_content_tag.string
    container=template_soup.find(id="container")
    container.append(title_content_tag)

    content_soup.extract(title_content_tag)
    # content_soup.remove(title_content_tag)
    return container

def create_navigation(container):
    '''
    add the navigation tag
    Args:
        template_soup:
        container:
        content_soup:

    Returns:
    '''
    default_nav_tag=BeautifulSoup(markdown(default_nav),"html.parser")
    container.append(default_nav_tag)




def process_images(template_soup):
    # produce images
    img_tag=template_soup.findAll("img")
    for img in img_tag:
        if "src" in img.attrs:
            continue
        if debug:
            loc=f'{local_asset_loc}{img.attrs["name"]}'
        else:
            loc=f'{web_asset_loc}{img.attrs["name"]}'
        img.attrs["src"]=loc


def make_module_page(original_name,template_loc,template_name,export_name):
    '''

    Args:
        original_name:
        template_loc:
        template_name:
        export_name:

    Returns:

    '''
    template_soup, content_soup=load_soups(original_name,template_loc+template_name)
    process_links(template_soup,template_loc,level=3)
    container=create_title(template_soup,content_soup)

    create_navigation(container)

    container.append(content_soup)
    process_images(template_soup)
    process_hrefs(template_soup)


    with open(f'{export_loc}{export_name}.html',"w",encoding="utf-8") as exf:
        exf.write(template_soup.prettify())






input_loc="../Course_Material/"
export_loc="../website/"



template_loc="templates/"
template_name="front_page_template"
local_asset_loc="../assets/local/"
web_asset_loc="https://eyesofpandaweb.s3.us-east-2.amazonaws.com/website_public/projects/painting_with_plotters/" #aws
debug=False

default_nav='<h2 class="author">Part of  <a href="https://www.eyesofpanda.com/project/painting_with_plotters/" target="_blank">The Painting with Plotters Course</a> by <a href="http://eyesofpanda.com" target="_blank">Licia He</a></h2>'


export_loc=f'{export_loc}module_0/'
mkdir(export_loc)

make_module_page(
    "0_Introduction",
    template_loc,
    template_name,
    "index"
)


