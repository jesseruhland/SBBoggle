from flask import Flask, request, redirect, render_template, flash, session
from boggle import Boggle

from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "sdklfjno9023u4"

debug = DebugToolbarExtension(app)


