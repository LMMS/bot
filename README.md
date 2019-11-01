# LmmsBot
Github webhook that posts comments to pull requests, providing artifacts retrieved from CI services.   

# Quickstart
This webhook was designed to run on the google cloud platform AppEngine's standard environment. 
However, it should be very easy to set it up on every machine with python and flask. 

To get started, set the `GITHUB_USERNAME` and `GITHUB_TOKEN` using environment variables or using an `.env` file:
```.env
GITHUB_USERNAME = "LmmsBot"
GITHUB_TOKEN = "<retracted>"
```

Then, either upload deploy it to GCP or manually install the `requirements.txt` file and run the `main.py` flask module.

## Github configuration
Add a webhook, check only `statuses` event, and change `payload type` for `json`.

# Documentation 
## How to add additional artifact titles
Currently, we use file names in order to detect relevant artifacts and display the right title.
To add additional artifacts, simply edit the `settings.py` file as following: 
```python
platform = Settings.Platform(
    name="Windows",
    extension_to_title={
        "exe": "Windows Executable"
    }
)
```
and add this platform:
```python
settings.platforms.append(platform)
```
## Duplicate comments
Since this script does not use any atomic storage it is no possible to detect if while preparing a new comment, another instance already posted a new comment. Resulting two comments posted, instead of one (the second instance would have to edit the first comment, that was posted after it has checked for comment). Also, CircleCI sends two updates instead of one. 

Currently, we solved that by limiting the amount of concurrent requests to 1 (See `app.yaml`). 

## Supported CI Services
- CircleCI (Without github checks)
- AppVeyor
