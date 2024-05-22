import shutil
import os


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def mkdir_multi(file_path,base_address,dest_address):
    file_path_lst = file_path.replace("\\", "/").replace(base_address,"").split("/")
    current_path = file_path_lst[0]+"/"
    if (len(current_path)<2):
        return
    mkdir(dest_address+current_path)
    for i in range(1, len(file_path_lst)):
        current_path += file_path_lst[i]+"/"
        # print(dest_address+current_path)
        mkdir(dest_address+current_path)


def get_source_and_destination(file_name,file_path,destination,base_address):
    additional_address=file_path.replace(base_address,"")
    destination_addr=f'{destination}/{additional_address}/{file_name}'
    source_addr=f'{file_path}/{file_name}'
    return source_addr,destination_addr

def copy_file(file_name,file_path,destination,base_address):
    '''
    make sure the path exist, and move to the new path
    :param file_name:
    :param file_path:
    :return:
    '''
    mkdir_multi(file_path,base_address,destination)

    source_addr, destination_addr=get_source_and_destination(file_name,file_path,destination,base_address)
    shutil.copyfile(source_addr,destination_addr)