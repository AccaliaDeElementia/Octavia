from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

#BEGIN: CONFIGURATION
DEBUG = True
SECRET_KEY = 'dugedr3+e$9ebr*@a3e49q+xuseBu$u_raw8da&e=e8ta$a+aphewe!rethuz#sw'

APP_NAME = 'Octavia'
APP_VERSION = '0.0.0Alpha'
APP_MAINTAINER = 'Accalia.de.Elementia'
APP_URL = 'https://github.com/AccaliaDeElementia/Octavia'
APP_LICENSE = 'Creative Commons Attribution 3.0 Unported'
APP_LICENSE_URL = 'http://creativecommons.org/licenses/by/3.0'
#END: CONFIGURATION

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    return render_template('status.html')
