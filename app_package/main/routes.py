from flask import Blueprint, render_template, request, jsonify, url_for, redirect, make_response, current_app
from flask_login import current_user, login_required
from app_package import db
from app_package.models import State, User, Picture

import secrets
import os

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template("index.html")
 
@main.route("/showMap")
@login_required
def showMap():
    return render_template("us_map.html")

@main.route("/updateMap", methods=["POST", "GET"])
@login_required
def updateMap():
    if request.method =="POST":
        stateAbr = request.form["stateId"]
        stateClicked = State.query.filter_by(abreviation=stateAbr).first_or_404()
        # Check if this user has already visited the state clicked. If so, remove it from their list of visited states. Otherwise  dd it to their list of visited states. 
        if db.session.query(User).join(User.statesVisited).filter(State.id == stateClicked.id, User.id == current_user.id).count() == 0:
            current_user.statesVisited.append(stateClicked)
            db.session.commit()
        else:
            current_user.statesVisited.remove(stateClicked)
            db.session.commit()
        # 
        return redirect(url_for('main.updateMap'))

    else:
        # Get list of abreviations for all states this user has visited
        statesVisitedList = [state.abreviation for state in current_user.statesVisited]

        return jsonify(statesVisitedList)

@main.route("/queryStateInfo", methods=["GET"])
@login_required
def queryStateInfo():
    stateAbr = request.args['stateId']

    stateDbObject = State.query.filter_by(abreviation=stateAbr).first_or_404()
    
    userPicsAtState = Picture.query.filter_by(user_id=current_user.id, state_id=stateDbObject.id)

    for pic in userPicsAtState:
        print(pic.fileName)

    # Check if this user has already visited the state clicked.
    if db.session.query(User).join(User.statesVisited).filter(State.id == stateDbObject.id, User.id == current_user.id).count() == 0:
        stateVisited = False
    else:
        stateVisited = True

    stateInfo = {
        "StateAbreviation": stateDbObject.abreviation,
        "StateName" : stateDbObject.name,
        "StateVisited" : stateVisited
    }

    # Package the response as json
    res = make_response(jsonify(stateInfo), 200)

    return res


@main.route("/uploadPhotos", methods=["POST"])
@login_required
def uploadPhotos():
    if request.method == "POST":
        stateName = request.form['stateName']
        if request.files:
            image = request.files['image']
            f_name, f_ext = os.path.splitext(image.filename)
            photoName = secrets.token_hex(8) + f_ext
            photoPath = os.path.join(current_app.root_path, 'static/images/uploaded/' + photoName)
            image.save(photoPath) 

            stateDbObject = State.query.filter_by(name=stateName).first_or_404()

            pic = Picture(fileName=photoName, filePath=photoPath, user_id=current_user.id, state_id=stateDbObject.id)
            db.session.add(pic)
            db.session.commit()
            #current_user.pictures.append(stateClicked)

    return "200"


"""
@main.route(
    "/<pathname>"
)  # This function will pass whatever text is entered after '/' to this function as a parameter, in this case 'pathname'
def generic(pathname):
    return f"Hello, {pathname}"
 """