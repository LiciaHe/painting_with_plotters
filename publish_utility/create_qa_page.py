from web_md_utils import *
import json
import os


def load_all_qa():
    files=[f for f in os.listdir(data_loc) if f.endswith('.json')]
    files.sort(key=lambda f:int(f.split("_")[0]))

    all_data=[]
    for file in files:
        info=json.load(open(f'{data_loc}{file}','r'))
        for i,qa in enumerate(info):
            all_data.append(qa)
            qa["id"]=len(all_data)-1
            for j,tag in enumerate(qa["tags"]):
                qa["tags"][j]=tag.lower()

            #treat q and a
            qa["q"]=convert_md_to_html(qa["q"])
            qa["a"]=convert_md_to_html(qa["a"])

    return all_data

def load_template(data):
    with open(template_file,'r') as f:
        plain_html=f.read()
    html=plain_html.replace("<script>//const_qaData=</script>",f'    <script>const qaData={data}</script>')

    soup=BeautifulSoup(html,"html.parser")
    return soup





qa_loc="../QA/"
data_loc=f'{qa_loc}data/'
template_loc="templates/"
template_file=f'{template_loc}QA_template.html'
data=load_all_qa()
soup=load_template(data)
process_links(soup,template_loc,level=3)

export_loc="../website/QA/"
export_name="index"
with open(f'{export_loc}{export_name}.html', "w", encoding="utf-8") as exf:
    exf.write(soup.prettify())



