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

# def load_template()




qa_loc="../QA/"
data_loc=f'{qa_loc}data/'
data=load_all_qa()
print(data)
