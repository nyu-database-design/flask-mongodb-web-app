import os

# load the credentials from the .env file
def get():
    """
    Load the configuration settings from the .env file.
    :returns: a dictionary of credentials and configuration settings
    """
    # open the .env configuration file
    APP_ROOT = os.path.join(os.path.dirname(__file__))   # refers to application_top
    dotenv_path = os.path.join(APP_ROOT, '.env')
    # loop through each line and add to dictionary
    f = open(dotenv_path, encoding='utf_8')
    config = {} # empty dictionary
    for line in f:
        # split by =
        line=line.strip() # remove line break
        # remove any comment from the line
        if '#' in line:
            line = line[:line.find('#')]
        setting = line.split('=') # split key and value apart
        if len(setting) == 2:
            key, value = setting
            config[key] = value
    return config
