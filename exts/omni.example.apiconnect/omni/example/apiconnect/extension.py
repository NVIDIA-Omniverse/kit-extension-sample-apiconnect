# SPDX-License-Identifier: Apache-2.0

import asyncio
import aiohttp
import carb
import omni.ext
import omni.ui as ui


class APIWindowExample(ui.Window):
    def __init__(self, title: str, **kwargs) -> None:
        """
        Initialize the widget.

        Args:
           title : Title of the widget. This is used to display the window title on the GUI.
        """
        super().__init__(title, **kwargs)
        self.frame.set_build_fn(self._build_fn)

    # async function to get the color palette from huemint.com and print it
    async def get_colors_from_api(self, color_widgets):
        """
        Get colors from HueMint API and store them in color_widgets.

        Args:
           color_widgets : List of widgets to
        """
        # Create the task for progress indication and change button text
        self.button.text = "Loading"
        task = asyncio.create_task(self.run_forever())

        # Create a aiohttp session to make the request, building the url and the data to send
        # By default it will timeout after 5 minutes.
        # See more here: https://docs.aiohttp.org/en/latest/client_quickstart.html
        async with aiohttp.ClientSession() as session:
            url = "https://api.huemint.com/color"
            data = {
                "mode": "transformer",  # transformer, diffusion or random
                "num_colors": "5",  # max 12, min 2
                "temperature": "1.2",  # max 2.4, min 0
                "num_results": "1",  # max 50 for transformer, 5 for diffusion
                "adjacency": ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0",
                ],  # nxn adjacency matrix as a flat array of strings
                "palette": ["-", "-", "-", "-", "-"],  # locked colors as hex codes, or '-' if blank
            }
            # make the request
            try:
                async with session.post(url, json=data) as resp:
                    # get the response as json
                    result = await resp.json(content_type=None)

                    # get the palette from the json
                    palette = result["results"][0]["palette"]

                    # apply the colors to the color widgets
                    await self.apply_colors(palette, color_widgets)

                    # Cancel the progress indication and return the button to the original text
                    task.cancel()
                    self.button.text = "Refresh"
            except Exception as e:
                carb.log_info(f"Caught Exception {e}")
                # Cancel the progress indication and return the button to the original text
                task.cancel()
                self.button.text = "Connection Timed Out \nClick to Retry"

    # apply the colors fetched from the api to the color widgets
    async def apply_colors(self, palette, color_widgets):
        """
        Apply the colors to the ColorWidget. This is a helper method to allow us to get the color values 
        from the API and set them in the color widgets

        Args:
           palette : The palette that we want to apply
           color_widgets : The list of color widgets
        """
        colors = [palette[i] for i in range(5)]
        index = 0
        # This will fetch the RGB colors from the color widgets and set them to the color of the color widget.
        for color_widget in color_widgets:
            await omni.kit.app.get_app().next_update_async()

            # we get the individual RGB colors from ColorWidget model
            color_model = color_widget.model
            children = color_model.get_item_children()
            hex_to_float = self.hextofloats(colors[index])

            # we set the color of the color widget to the color fetched from the api
            color_model.get_item_value_model(children[0]).set_value(hex_to_float[0])
            color_model.get_item_value_model(children[1]).set_value(hex_to_float[1])
            color_model.get_item_value_model(children[2]).set_value(hex_to_float[2])
            index = index + 1

    async def run_forever(self):
        """
        Run the loop until we get a response from omni.
        """
        count = 0
        dot_count = 0
        # Update the button text.
        while True:
            # Reset the button text to Loading
            if count % 10 == 0:
                # Reset the text for the button
                # Add a dot after Loading.
                if dot_count == 3:
                    self.button.text = "Loading"
                    dot_count = 0
                # Add a dot after Loading
                else:
                    self.button.text += "."
                    dot_count += 1
            count += 1
            await omni.kit.app.get_app().next_update_async()

    # hex to float conversion for transforming hex color codes to float values
    def hextofloats(self, h):
        """
        Convert hex values to floating point numbers. This is useful for color conversion to a 3 or 5 digit hex value

        Args:
          h : RGB string in the format 0xRRGGBB

        Returns:
           float tuple of ( r g b ) where r g b are floats between 0 and 1 and b
        """
        # Convert hex rgb string in an RGB tuple (float, float, float)
        return tuple(int(h[i : i + 2], 16) / 255.0 for i in (1, 3, 5))  # skip '#'

    def _build_fn(self):
        """
        Build the function to call the api when the app starts.
        """
        with self.frame:
            with ui.VStack(alignment=ui.Alignment.CENTER):
                # Get the run loop
                run_loop = asyncio.get_event_loop()
                ui.Label("Click the button to get a new color palette", height=30, alignment=ui.Alignment.CENTER)

                with ui.HStack(height=100):
                    color_widgets = [ui.ColorWidget(1, 1, 1) for i in range(5)]

                def on_click():
                    """
                    Get colors from API and run task in run_loop. This is called when user clicks the button
                    """
                    run_loop.create_task(self.get_colors_from_api(color_widgets))

                # create a button to trigger the api call
                self.button = ui.Button("Refresh", clicked_fn=on_click)

                # we execute the api call once on startup
                run_loop.create_task(self.get_colors_from_api(color_widgets))


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.

    def on_startup(self, ext_id):
        """
        Called when the extension is started.

        Args:
          ext_id - id of the extension
        """
        print("[omni.example.apiconnect] MyExtension startup")

        # create a new window
        self._window = APIWindowExample("API Connect Demo - HueMint", width=260, height=270)

    def on_shutdown(self):
        """
        Called when the extension is shut down. Destroys the window if it exists and sets it to None
        """
        print("[omni.example.apiconnect] MyExtension shutdown")
        # Destroys the window and releases the reference to the window.
        if self._window:
            self._window.destroy()
            self._window = None
