# API Connect Sample Omniverse Extension

![preview.png](/exts/omni.example.apiconnect/data/preview.png)

### About
This Sample Omniverse Extension demonstrates how connect to an API. 

In this sample, we create a palette of colors using the [HueMint.com](https://huemint.com/). API.

### [README](exts/omni.example.apiconnect)
See the [README for this extension](exts/omni.example.apiconnect) to learn more about it including how to use it.

## [Tutorial](exts/omni.example.apiconnect/docs/tutorial.md)
Follow a [step-by-step tutorial](exts/omni.example.apiconnect/docs/tutorial.md) that walks you through how to build this extension using [asyncio](https://docs.python.org/3/library/asyncio.html) and [aiohttp](https://docs.aiohttp.org/en/stable/).

## Adding This Extension

To add this extension to your app:

1. Download or Clone the extension, unzip the file if downloaded

2. Create a New Extension

**Linux:**
```bash
./repo.sh template new
```

**Windows:**
```powershell
.\repo.bat template new
```

3. Follow the prompt instructions:
- **? Select with arrow keys what you want to create:** Extension
- **? Select with arrow keys your desired template:**: Python UI Extension
- **? Enter name of extension [name-spaced, lowercase, alphanumeric]:**: omni.example.apiconnect
- **? Enter extension_display_name:**: API Connect
- **? Enter version:**: 0.1.0

4. Add the Extension to an Application

In the newly created extension, **copy and paste** the `omni.example.apiconnect` folder that was cloned into `kit-app-template/sources/extensions/omni.example.apiconnect`.

You will be prompted if you want to replace files, **select** `Replace All`.

To add your extension to an application, declare it in the dependencies section of the application's `.kit` file:

```toml
[dependencies]
"omni.example.apiconnect" = {}
```

5. Build with New Extensions
After a new extension has been added to the `.kit` file, the application should be rebuilt to ensure extensions are populated to the build directory.

**Linux:**
```bash
./repo.sh build
```

**Windows:**
```powershell
.\repo.bat build
```


## Attribution & Acknowledgements

This extension uses the [Huemint.com API](https://huemint.com/about/). Huemint uses machine learning to create unique color schemes. 

Special thanks to Jack Qiao for allowing us to use the Huemint API for this demonstration.

Check out [Huemint.com](https://huemint.com/)

## Contributing
The source code for this repository is provided as-is and we are not accepting outside contributions.