from flask import Flask,render_template,request,Blueprint

newtool_app = Blueprint('newtool',__name__)

@newtool_app.route('/')
def home():
    return render_template('new_tool.html')



