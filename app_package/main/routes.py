from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template("index.html")

"""
@main.route(
    "/<pathname>"
)  # This function will pass whatever text is entered after '/' to this function as a parameter, in this case 'pathname'
def generic(pathname):
    return f"Hello, {pathname}"
 """