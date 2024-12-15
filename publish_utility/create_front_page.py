import markdown,re
from markdown import markdown
from bs4 import BeautifulSoup

from web_md_utils import *
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







    #make sure the font href is correct
def create_title(original_name,template_soup):
    #update title
    # title_text=name_treat(original_name)
    title_tag=template_soup.find("title")
    title_tag.string="Painting With Plotters"

def step_2_create_table(container, module,template_soup):
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
    resource_div=None
    for tag in module:
        if tag.name in ["h3"]:
            #start a div
            current_module_id=tag.string[:tag.string.find(":")]
            current_div=create_and_append_tag(
                template_soup,
                container,
                "div",
                {
                    "class":"course-module",
                    "id":f'module_{current_module_id}'
                }
            )
            #append content of the div
            applyAttrs(tag, {"class": "module"})
            current_div.append(tag)
        elif tag.name in [None,"li"]:
            continue
        elif tag.name =='ol':
            applyAttrs(tag,{"class":"topic"})
            current_div.append(tag)
            resource_div = create_and_append_tag(
                    template_soup,
                    current_div,
                    "div",
                    {"class": "material",
                     "id":f'material_{current_module_id}'
                     }
            )
            material_place_holder = create_and_append_tag(
                    template_soup,
                    resource_div,
                    "p",
                    {}
            )
            material_place_holder.string = "Coming Soon"
        elif "courseinfo" in str(tag):
            resource_div=template_soup.find(id=f'material_{current_module_id}')
            resource_div.clear()
            tags_within_info=list(tag.children)[0].children
            for c in tags_within_info:
                resource_div.append(c)
            # print(list())
            # resource_div.append(tag.children)

    # #append course info
    # if "courseinfo" in str(module):
    #     # print()
    #     course_info=module.find("courseinfo")
    #     resource_div.clear()
    #     resource_div.append(course_info)
    #     print(resource_div,course_info)



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


def make_front_page(original_name,template_loc,template_name,export_name):
    '''

    Args:
        original_name:
        template_loc:
        template_name:
        export_name:

    Returns:

    '''
    template_soup, (start,module,end)=load_soups(original_name,template_loc+template_name)
    #replace css
    process_links(template_soup,template_loc)
    create_title(original_name,template_soup)


    container=template_soup.find(id="container")
    container.append(start)
    step_2_create_table(container,module,template_soup)
    container.append(end)
    process_images(template_soup)
    process_hrefs(template_soup)


    with open(f'{export_loc}{export_name}.html',"w",encoding="utf-8") as exf:
        exf.write(template_soup.prettify())






input_loc="../Course_Material/"
export_loc="../website/"


template_loc="templates/"
template_name="front_page_template"
ori_name="00_Course_Overview"
local_asset_loc="../assets/local/"
web_asset_loc="https://eyesofpandaweb.s3.us-east-2.amazonaws.com/website_public/projects/painting_with_plotters/" #aws
debug=False

make_front_page(
    "00_Course_Overview",
    template_loc,
    template_name,
    "index"
)


