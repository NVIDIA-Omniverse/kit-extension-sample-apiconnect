# SPDX-License-Identifier: Apache-2.0

import omni.ext
import omni.ui as ui
import asyncio
import aiohttp
from omni.ui import style_utils
from functools import partial


# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[omni.example.apiconnect] some_public_function was called with x: ", x)
    return x ** x

#async function to get the color palette from huemint.com and print it
async def get_colors_from_api(color_widgets):

    #create a aiohttp session to make the request, building the url and the data to send 
    async with aiohttp.ClientSession() as session:
        url = 'https://api.huemint.com/color'
        data = {
            "mode":"transformer", #transformer, diffusion or random
            "num_colors":"5", # max 12, min 2
            "temperature":"1.2", #max 2.4, min 0
            "num_results":"1", #max 50 for transformer, 5 for diffusion
            "adjacency":[ "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"], #nxn adjacency matrix as a flat array of strings
            "palette":["-", "-", "-", "-", "-"], #locked colors as hex codes, or '-' if blank
            }
        #make the request    
        async with session.post(url, json=data) as resp:
            #get the response as json
            result = await resp.json(content_type=None)
            
            #get the palette from the json
            palette=result['results'][0]['palette']
            
            #apply the colors to the color widgets
            apply_colors(palette, color_widgets)
            
            
#apply the colors fetched from the api to the color widgets
def apply_colors(palette, color_widgets):
            colors = [None]*5
            
            colors[0] = palette[0]
            colors[1] = palette[1]
            colors[2] = palette[2]
            colors[3] = palette[3]
            colors[4] = palette[4]

            print(colors)
           
            i =0
            for color_widget in color_widgets:
                #we get the individual RGB colors from ColorWidget model
                children = color_widget.model.get_item_children()
                
                #we set the color of the color widget to the color fetched from the api
                color_widget.model.get_item_value_model(children[0]).set_value(hextofloats(colors[i])[0])
                color_widget.model.get_item_value_model(children[1]).set_value(hextofloats(colors[i])[1])
                color_widget.model.get_item_value_model(children[2]).set_value(hextofloats(colors[i])[2])
                i=i+1
            
           

#hex to float conversion for transforming hex color codes to float values
def hextofloats(h):
    #Convert hex rgb string in an RGB tuple (float, float, float)
    return tuple(int(h[i:i + 2], 16) / 255. for i in (1, 3, 5)) # skip '#'   


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    
    def on_startup(self, ext_id):
        print("[omni.example.apiconnect] MyExtension startup")

        #create a new window        
        self._window = ui.Window("API Connect Demo - HueMint", width=260, height=270)
        with self._window.frame:
            with ui.VStack(alignment=ui.Alignment.CENTER):
                
                ui.Label("Click the button to get a new color palette",height=30)
                
                with ui.HStack():
                    
                    #colorwidget = ui.ColorWidget(0.120,0,0, width=50, height=100)

                    color_widgets = [None] * 5
                    color_widgets[0] = ui.ColorWidget(1,1,1, width=50, height=100)
                    color_widgets[1] = ui.ColorWidget(1,1,1, width=50, height=100)
                    color_widgets[2] = ui.ColorWidget(1,1,1, width=50, height=100)
                    color_widgets[3] = ui.ColorWidget(1,1,1, width=50, height=100)
                    color_widgets[4] = ui.ColorWidget(1,1,1, width=50, height=100)

                #create a button to trigger the api call
                def on_click():
                    asyncio.ensure_future(get_colors_from_api(color_widgets))
                
                ui.Button("Refresh", clicked_fn=on_click)

                #we execute the api call once on startup
                asyncio.ensure_future(get_colors_from_api(color_widgets))

             
                

    def on_shutdown(self):
        print("[omni.example.apiconnect] MyExtension shutdown")

   

    
