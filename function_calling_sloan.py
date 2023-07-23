import openai
import os
from langchain import OpenAI
from langchain import SQLDatabase
from langchain import SQLDatabaseChain
import sqlite3
import pandas as pd
import numpy as np
import json
# %matplotlib inline
import matplotlib.pyplot as plt
from astroquery.sdss import SDSS
from astropy import coordinates as coords
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.table import Table
from function_descriptions import *
from astropy.visualization import astropy_mpl_style
import matplotlib.pyplot as plt
import json
from function_descriptions_2 import *
openai_api =  os.environ.get("OPENAI_API")
print(open)
openai.api_key = openai_api
def sample_test_fn(): 
    pos = coords.SkyCoord('0h8m05.63s +14d50m23.3s', frame='icrs')
    xid = SDSS.query_region(pos, radius='5 arcsec', spectro=True)
    sp = SDSS.get_spectra(matches=xid)
    im = SDSS.get_images(matches=xid, band='g')
    img = SDSS.get_images(matches = xid)
    plt.style.use(astropy_mpl_style)

# Extract the image data from the 'img' object
    image_data = img[0][0].data

    # Display the image using Matplotlib's imshow
    plt.imshow(image_data, cmap='gray', origin='lower')

    # Add labels, titles, or any other desired plot elements

    # Show the plot
    # x = plt.show()
    plt.savefig('sample_plot.png')

    # Close the Matplotlib figure to release resources
    plt.close()

def function_call(question) :
    # question = "Retrieve the PhotoObjAll table for the run number 94, rerun number 301, camcol 6, and field 94."
    model_name = "gpt-3.5-turbo-0613"
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {"role" : "system", "content" : "Only use the functions you have been provided with. If the function does not satisfy the parameters of the input function or does not meet the description do not do anything"},
            {"role": "user", "content": question},
        ],
        functions=functions_2,
        function_call="auto",
    )
    message = response["choices"][0]["message"]
    print(response)
    function_name = message["function_call"]["name"]
    arguments = json.loads(message["function_call"]["arguments"])
    print(check_funcs(function_name, arguments))


def check_funcs(function_name, arguments):
    if function_name == 'query_photoobj':
        # Define a dictionary with the provided arguments and their values
        arguments_from_json = {
            key: value
            for key, value in arguments.items()
            if key in ["run", "rerun", "camcol", "field", "fields", "timeout", "field_help", "get_query_payload", "data_release", "cache"]
        }
        # Call the function using dictionary unpacking (**) to pass the specific arguments
        return SDSS.query_photoobj(**arguments_from_json)

    elif function_name == 'query_photoobj_async':
        # Define a dictionary with the provided arguments and their values
        arguments_from_json = {
            key: value
            for key, value in arguments.items()
            if key in ["run", "rerun", "camcol", "field", "fields", "timeout", "field_help", "get_query_payload", "data_release", "cache"]
        }

        # Call the function using dictionary unpacking (**) to pass the specific arguments
        return SDSS.query_photoobj_async(**arguments_from_json)

    elif function_name == 'get_images':
        arguments_from_json = {
            key: value
            for key, value in arguments.items()
            if key in ["coordinates", "radius", "matches", "run", "rerun", "camcol", "field", "band", "timeout", "get_query_payload", "cache", "data_release", "show_progress"]
        }
        return SDSS.get_images(**arguments_from_json)

    elif function_name == 'get_spectra':
        arguments_from_json = {
            key: value
            for key, value in arguments.items()
            if key in ["coordinates", "radius", "matches", "plate", "fiberID", "mjd", "timeout", "get_query_payload", "data_release", "cache", "show_progress"]
        }
        return SDSS.get_spectra(**arguments_from_json)

    elif function_name == 'query_region':
        arguments_from_json = {
            key: value
            for key, value in arguments.items()
            if key in ["coordinates", "radius", "width", "height", "timeout"]
        }
        return SDSS.query_region(**arguments_from_json)

    elif function_name == 'query_crossid_async':
        arguments_from_json = {
            key: value
            for key, value in arguments.items()
            if key in ["coordinates", "radius", "timeout", "fields", "photoobj_field"]
        }
        return SDSS.query_crossid_async(**arguments_from_json)

    elif function_name == 'get_spectral_template':
        arguments_from_json = {
            key: value
            for key, value in arguments.items()
            if key in ["kind", "timeout", "show_progress"]
        }
        return SDSS.get_spectral_template(**arguments_from_json)

    elif function_name == 'query_specobj':
        arguments_from_json = {
            key: value
            for key, value in arguments.items()
            if key in ["plate", "mjd", "fiberID", "fields"]
        }
        return SDSS.query_specobj(**arguments_from_json)

    elif function_name == 'query_specobj_async':
        arguments_from_json = {
            key: value
            for key, value in arguments.items()
            if key in ["plate", "mjd", "fiberID", "fields"]
        }
        return SDSS.query_specobj_async(**arguments_from_json)

    elif function_name == 'query_crossid':
        arguments_from_json = {
            key: value
            for key, value in arguments.items()
            if key in ["coordinates", "radius", "timeout", "fields", "photoobj_field"]
        }
        return SDSS.query_crossid(**arguments_from_json)

    else:
        print("No function found")
        return " "

    # Continue with the rest of the functions...

    # return x
# C:\Users\eklav\function_calling _sloan.py
question = "Find galaxies within 1' of a given point (radius=185.0, declination=-0.5)."
function_call(question)
# def function_call(question) :
#   for function in functions :
#     model_name = "gpt-3.5-turbo-0613"
#     response = openai.ChatCompletion.create(
#     model=model_name,
#     messages=[
#         {"role" : "system", "content" : "Only use the functions you have been provided with. If the function does not satisfy the parameters of the input function or does not meet the description do not do anything"},
#         {"role": "user", "content": question},
#     ],
#     functions=function,
#     function_call="auto",
#     )
#     print(response)
#     message = response["choices"][0]["message"]
#     print("here")
#     if message.get("function_call") :
#       function_name = message["function_call"]["name"]
#       arguments = json.loads(message["function_call"]["arguments"])
#       print(check_funcs(function_name, arguments))
#       return check_funcs(function_name, arguments)
#     #   break
#     else : this one is not working as intended because it tends to pick the wrong functions
#       continue
