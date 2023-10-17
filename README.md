# API Connect Sample Omniverse Extension

![preview.png](/exts/omni.example.apiconnect/data/preview.png)

### About
This Sample Omniverse Extension demonstrate how connect to an API. 

In this sample, we create a palette of colors using the [HueMint.com](https://huemint.com/) API.

### [README](exts/omni.example.apiconnect)
See the [README for this extension](exts/omni.example.apiconnect) to learn more about it including how to use it.

## [Tutorial](exts/omni.example.apiconnect/docs/tutorial.md)
Follow a [step-by-step tutorial](exts/omni.example.apiconnect/docs/tutorial.md) that walks you through how to use omni.ui.scene to build this extension.

## Adding This Extension

To add a this extension to your Omniverse app:
1. Go into: Extension Manager -> Hamburger Icon -> Settings -> Extension Search Path
2. Add this as a search path: `git://github.com/NVIDIA-Omniverse/kit-extension-sample-apiconnect.git?branch=main&dir=exts`

Alternatively:
1. Download or Clone the extension, unzip the file if downloaded
2. Copy the `exts` folder path within the extension folder
    - i.e. home/.../kit-extension-sample-apiconnect/exts (Linux) or C:/.../kit-extension-sample-apiconnect/exts (Windows)
3. Go into: Extension Manager -> Hamburger Icon -> Settings -> Extension Search Path
4. Add the `exts` folder path as a search path

## Linking with an Omniverse app

For a better developer experience, it is recommended to create a folder link named `app` to the *Omniverse Kit* app installed from *Omniverse Launcher*. A convenience script to use is included.

Run:

```bash
# Windows
> link_app.bat
```

```shell
# Linux
~$ link_app.sh
```

If successful you should see `app` folder link in the root of this repo.

If multiple Omniverse apps is installed script will select recommended one. Or you can explicitly pass an app:

```bash
# Windows
> link_app.bat --app code
```

```shell
# Linux
> link_app.sh --app code
```

You can also just pass a path to create link to:

```bash
# Windows
> link_app.bat --path "C:/Users/bob/AppData/Local/ov/pkg/create-2022.1.3"
```

```shell
# Linux
> link_app.sh --path "home/bob/.local/share/ov/pkg/create-2022.1.3"
```

## Attribution & Acknowledgements

This Extensions uses the [Huemint.com API](https://huemint.com/about/). Huemint uses machine learning to create unique color schemes. 

Special thanks to Jack Qiao for allowing us to use the Huemint API for this demonstration.

Check out [Huemint.com](https://huemint.com/)

## Contributing
The source code for this repository is provided as-is and we are not accepting outside contributions.