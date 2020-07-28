from flask import Flask, Blueprint, render_template
from bankingApp import create_app

main = Blueprint('main', __name__)

