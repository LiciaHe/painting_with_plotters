import markdown,re
from markdown import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from bs4 import BeautifulSoup
def load_soups(original_name,template_loc):
    with open(f'{template_loc}.html',"r",encoding="utf-8") as basesf:
        template_soup=BeautifulSoup(basesf.read(), "html.parser")

    with open(f'{input_loc}{original_name}.md', 'r', encoding='utf-8') as input_file:
        markdown_text = input_file.read().replace("Â "," ").replace(" "," ")
        module_starter=markdown_text.find("MODULE START")
        module_end=markdown_text.find("MODULE END")
        start=markdown_text[:module_starter]
        module=markdown_text[module_starter+len("MODULE START"):module_end]
        end=markdown_text[module_end+len("MODULE END"):]

        content_soup=[
            BeautifulSoup(markdown(string),"html.parser") for string in [start,module,end]
        ]
    return template_soup,content_soup

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
def make_front_page(original_name,template_loc,export_name):
    template_soup, (start,module,end)=load_soups(original_name,template_loc)
    #update title
    title_text=name_treat(original_name)
    title_tag=template_soup.find("title")
    title_tag.string=title_text

    container=template_soup.find(id="container")
    container.append(start)
    ## producing a header
    header_text=BeautifulSoup('''
            <div class="course-module">
            <h3 class="module">Module</h3>
            <h3 class="topic">Topic</h3>
            <h3 class="material">Material</h3>
            </div>
    ''',"html.parser")
    container.append(header_text)
    #work on module
    current_div=None
    for tag in module:
        if tag.name in ["h3"]:
            #start a div
            current_div=create_and_append_tag(
                template_soup,
                container,
                "div",
                {"class":"course-module"}
            )
            #append content of the div
            applyAttrs(tag, {"class": "module"})
            current_div.append(tag)
        elif tag.name in [None,"li"]:
            continue
        elif tag.name =='ol':
            applyAttrs(tag,{"class":"topic"})
            current_div.append(tag)
            #append closing div
            resource=create_and_append_tag(
                template_soup,
                current_div,
                "div",
                {"class": "material"}
            )
            place_holder=create_and_append_tag(
                template_soup,
                resource,
                "p",
                {}
            )
            # print(place_holder)
            place_holder.string="Coming Soon"

    container.append(end)

    # produce images
    img_tag=template_soup.findAll("img")
    for img in img_tag:
        if "src" in img.attrs:
            continue
        if debug:
            loc=f'{local_asset_loc}/{img.attrs["name"]}'
        else:
            loc=f'{web_asset_loc}/{img.attrs["name"]}'
        img.attrs["src"]=loc

    with open(f'{export_loc}{export_name}.html',"w",encoding="utf-8") as exf:
        exf.write(template_soup.prettify())






input_loc="../Course_Material/"
export_loc="../website/"
template_loc="front_page_template"
ori_name="00_Course_Overview"
local_asset_loc="../assets/local/"
web_asset_loc="#todo" #aws
debug=True

make_front_page(
    "00_Course_Overview",
    template_loc,
    "index"
)


