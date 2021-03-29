# Flash-MongoDB Example Web App

Project currently hosted at https://i6.cims.nyu.edu/~ab1258/flask-mongodb-example/flask.cgi

## Database credentials

The credentials for logging into a MongoDB database must be stored in a file named `.env`, which is not included in this repository for security reasons.

1. make a copy of the file named `.env.example` and save it as `.env`
1. edit the `.env` file and enter your own database credentials into each of the variables where indicated

## Run locally

To run this app locally, do the following:

### Set up a Python virtual environment

This command creates a new virtual environment with the name `.venv`:

```bash
python3 -m venv .venv
```

#### Activate the virtual environment

To activate the virtual environment named `.venv`...

On Windows, run:

```bash
.venv\Scripts\activate.bat
```

On Mac, run:

```bash
source .venv/bin/activate
```

#### Install the dependencies into the virtual environment

The file named, `requirements.txt` contains a list of dependencies - other software modules that this app depends upon to run.

To install the dependencies into the currently-active virtual environment, use `pip`, the default Python "package manager" - software that takes care of installing the correct version of any module into your in the correct place for the current environment.

```bash
pip3 install -r requirements.txt
```

### Run the app

1. define two environment variables from the command line: `export FLASK_APP=myapp` and `export FLASK_ENV=development`
1. start flask with `flask run` - this will output an address at which the app is running locally, e.g. https://127.0.0.1:5000. Visit that address in a web browser.

## Host on a web server

The following steps outline how to host this application on NYU's **i6**.cims.nyu.edu web server. Other servers may vary.

1. Familiarize yourself with web hosting steps on a CIMS server from the link: https://cims.nyu.edu/webapps/content/systems/userservices/webhosting.
2. Use a file transfer program, such as Cyberduck, to copy your entire project directory to the `/home/$USER/public_html/` directory, where `$USER` is replaced by your own username.
3. In the root directory of your project, create a file, named `flask.cgi`, and paste the following contents into it, where `myapp` is replaced with your own app's main file name.

```
#!/usr/bin/python3
import sys
sys.path.insert(0, '/misc/linux/centos7/x86_64/local/stow/python-3.6/lib/python3.6/site-packages/')
from wsgiref.handlers import CGIHandler
from myapp import app
CGIHandler().run(app)
```

4. Your app should now be live at https://i6.cims.nyu.edu/~$USER/$flask-app-directory/flask.cgi, where `$USER` is replaced with your own **i6** username and `$flask-app-directory` is replaced with the name of the sub-directory within `public_html` where your flask app code resides.
