# LmmsBot
Github webhook that posts comments to pull requests, providing artifacts retrieved from CI services.   

# Quickstart
This webhook was designed to run on the google cloud platform AppEngine's standard environment. 
However, it should be very easy to set it up on every machine with python and flask. 

To get started, edit `settings.edit.py` and change `GITHUB_USER` and `GITHUB_TOKEN`. Then, rename `settings.edit.py` to `settings.py`.

Then, either upload deploy it to GCP or manually install the `requirements.txt` file and run the `main.py` flask module.

# Documentation 
## How to add additional artifact titles
Currently, we use file names in order to detect relevant artifacts and display the right title.
To add additional artifacts, simply edit the `settings.py` file as following: 
```python
EXTENSION_TO_PLATFORM_TITLE = {
    "coolfile": "CoolFile artifact",
    "extension": "Platform Title"
}
```
## Duplicate comments
Since this script does not use any atomic storage it is no possible to detect if while preparing a new comment, another instance already posted a new comment. Resulting two comments posted, instead of one (the second instance would have to edit the first comment, that was posted after it has checked for comment).

Currently, we solved that by limiting the amount of concurrent requests to 1 (See `app.yaml`). 
