import sys
sys.path.insert(1,"../")

from PWP.Generator.SettingAndStorageGenerator import SettingAndStorageGenerator

settings={
    "name":"0_s_s_tester",
    "parameters":{},
    "basic_settings":{
        "export_loc": "output/",
        "batch_name":"test",
        "seed":"1323453"
    }
}
generator=SettingAndStorageGenerator(settings=settings)
print(generator.get_full_save_loc("txt"))
print(generator.get_full_save_loc("csv"))
print(generator.get_full_save_loc("svg"))