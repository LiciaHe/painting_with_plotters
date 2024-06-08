import sys
sys.path.insert(1,"../")

from PWP.Generator.SettingAndStorageGenerator import SettingAndStorageGenerator

settings={
    "name":"0_s_s_tester",
    "parameters":{
        "test_rg":[3,5]
    },
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

for i in range(3):
    print(generator.get_random_value_from_parameters("test_rg"))