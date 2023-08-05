import json
import numpy as np
import pandas as pd

 
def create_dictionary(json_list,list_json_loc,dict_mapping):

    list_json_loc=list_json_loc

    dict_mapping=dict_mapping

 

    def uni_val_dict_init(list_json_loc, dict_mapping) :

 

        unique_val_dict = dict()

        for i in list_json_loc :

            unique_val_dict[dict_mapping[i]] = []

 

        return unique_val_dict

 

    # function to split the paths for each key

    def string_splitter(path_string, key) :

        if key == "subscriberId" :

            path_list = path_string.split(".")[:-1]

            path_list[-1] = path_list[-1][:-2]

 

            return path_list

 

        else :

            return path_string.split(".")

 

    # function to generate val from json

    def generate_val(json_data ,path_string , key ) :

 

        path_list = string_splitter(path_string,key)

 

        for index,value in enumerate(path_list):

            if json_data[value] == None :

                 return None

 

            else :

                json_data= json_data[value]

 

                if len(path_list) -1 == index :

                    return json_data

 

    # function to create the final val dict

    def creating_val_dict(json_list) :

 

        unique_val_dict = uni_val_dict_init(list_json_loc, dict_mapping)

 

        for str_data in json_list :

 

            # converting str into dict

            json_data = json.loads(str_data)

 

            for index,val in enumerate(list_json_loc) :

 

                # calling generate_val to fetch the values

                str_val = generate_val(json_data , val , dict_mapping[val])

 

 

                if str_val is not None :

 

                    if dict_mapping[val] == "subscriberId" :

                        unique_val_dict[dict_mapping[val]].append(str_val[0]['identifier'])

 

                    else :

                        unique_val_dict[dict_mapping[val]].append(str_val)

 

        return unique_val_dict 

    

    

    unique_val_dict = creating_val_dict(json_list)

   

    return unique_val_dict
