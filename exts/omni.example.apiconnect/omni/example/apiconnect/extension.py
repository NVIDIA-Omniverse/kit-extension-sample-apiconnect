
from ctypes import alignment
import omni.ext
import omni.ui as ui
import asyncio
import aiohttp
from omni.ui import style_utils


# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[omni.example.apiconnect] some_public_function was called with x: ", x)
    return x ** x


async def get_colors_from_api(color_widgets):

    #async function to get the color palette from http://colormind.io/api/ and print it
    async with aiohttp.ClientSession() as session:
        url = 'http://colormind.io/api/'
        data = {
            "model": "default",
            # "input": [[0,0,0],[111,111,111]]
        }
        async with session.post(url, json=data) as resp:
            palette = await resp.json(content_type=None)
            apply_colors(palette, color_widgets)
            

def apply_colors(palette, color_widgets):
            colors = [None]*5
            
            colors[0] = palette['result'][0]
            colors[1] = palette['result'][1]
            colors[2] = palette['result'][2]
            colors[3] = palette['result'][3]
            colors[4] = palette['result'][4]

            print(colors)
           
            i =0
            for color_widget in color_widgets:
                children = color_widget.model.get_item_children()
                color_widget.model.get_item_value_model(children[0]).set_value(colors[i][0]/255)
                color_widget.model.get_item_value_model(children[1]).set_value(colors[i][1]/255)
                color_widget.model.get_item_value_model(children[2]).set_value(colors[i][2]/255)
                i=i+1
            
            # print(str(color_widget.model.get_item_value_model(children[0]).get_value()))

   


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[omni.example.apiconnect] MyExtension startup")

                

        self._window = ui.Window("API Connect Demo - PaletteGen", width=260, height=270)
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

                
                def on_click():
                    asyncio.ensure_future(get_colors_from_api(color_widgets))
                
                ui.Button("Refresh", clicked_fn=on_click)

                asyncio.ensure_future(get_colors_from_api(color_widgets))

                

                
                

                
                

    def on_shutdown(self):
        print("[omni.example.apiconnect] MyExtension shutdown")

    
