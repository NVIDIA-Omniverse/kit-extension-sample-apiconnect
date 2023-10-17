# SPDX-License-Identifier: Apache-2.0

import omni.ext
import omni.ui as ui
import asyncio
import aiohttp

   
class APIWindowExample(ui.Window):
    def __init__(self, title: str, **kwargs) -> None:
        super().__init__(title, **kwargs)
        self.frame.set_build_fn(self._build_fn)

    #async function to get the color palette from huemint.com and print it
    async def get_colors_from_api(self, color_widgets):
        # Create the task for progress indication and change button text
        self.button.text = "Loading"
        task = asyncio.create_task(self.run_forever())

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
                await self.apply_colors(palette, color_widgets)

                # Cancel the progress indication and return the button to the original text
                task.cancel()
                self.button.text = "Refresh"

    #apply the colors fetched from the api to the color widgets
    async def apply_colors(self, palette, color_widgets):
        colors = [palette[i] for i in range(5)]
        index = 0
        for color_widget in color_widgets:
            await omni.kit.app.get_app().next_update_async()

            #we get the individual RGB colors from ColorWidget model
            color_model = color_widget.model
            children = color_model.get_item_children()
            hex_to_float = self.hextofloats(colors[index])
            
            #we set the color of the color widget to the color fetched from the api
            color_model.get_item_value_model(children[0]).set_value(hex_to_float[0])
            color_model.get_item_value_model(children[1]).set_value(hex_to_float[1])
            color_model.get_item_value_model(children[2]).set_value(hex_to_float[2])
            index = index + 1

    async def run_forever(self):
        count = 0
        dot_count = 0
        while True:
            if count % 10 == 0:
                # Reset the text for the button
                if dot_count == 3:
                    self.button.text = "Loading"
                    dot_count = 0
                # Add a dot after Loading
                else:
                    self.button.text += "."
                    dot_count += 1
            count += 1
            await omni.kit.app.get_app().next_update_async()

    #hex to float conversion for transforming hex color codes to float values
    def hextofloats(self, h):
        #Convert hex rgb string in an RGB tuple (float, float, float)
        return tuple(int(h[i:i + 2], 16) / 255. for i in (1, 3, 5)) # skip '#'   
    
    def _build_fn(self):
        with self.frame:
            with ui.VStack(alignment=ui.Alignment.CENTER):
                # Get the run loop
                run_loop = asyncio.get_event_loop()
                ui.Label("Click the button to get a new color palette",height=30, alignment=ui.Alignment.CENTER)
                
                with ui.HStack(height=100):

                    color_widgets = [ui.ColorWidget(1,1,1) for i in range(5)]

                def on_click():
                    run_loop.create_task(self.get_colors_from_api(color_widgets))

                #create a button to trigger the api call
                self.button = ui.Button("Refresh", clicked_fn=on_click)

                #we execute the api call once on startup
                run_loop.create_task(self.get_colors_from_api(color_widgets))

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    
    def on_startup(self, ext_id):
        print("[omni.example.apiconnect] MyExtension startup")

        #create a new window        
        self._window = APIWindowExample("API Connect Demo - HueMint", width=260, height=270)

    def on_shutdown(self):
        print("[omni.example.apiconnect] MyExtension shutdown")
        if self._window:
            self._window.destroy()
            self._window = None