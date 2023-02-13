from flask import render_template, request, redirect, url_for
from flask import current_app as app
from app.database import db
from app.models import User, List, Card
from datetime import datetime
from app.forms import RegisterForm, LoginForm, AddListForm, EditListForm, AddCardForm, EditCardForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


# home route
@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    user_id = current_user.id
    lists = List.query.filter_by(user=user_id).all()
    return render_template('home.html', title="Kanban - Home", lists=lists)


# summary route
@app.route("/summary", methods=["GET", "POST"])
@login_required
def summary():
    user_id = current_user.id
    lists = List.query.filter_by(user=user_id).all()
    counts = {}
    today = datetime.today().date()
    for list in lists:
        date_count = []
        d = {}
        counts[list.list_id] = {"total": len(
            list.cards), "total_completed": 0, "total_incomplete": 0, "d_passed": 0, "date_count": None}
        for card in list.cards:
            if card.completed == 1:
                counts[list.list_id]["total_completed"] += 1 # calculate how many tasks are completed
                date_count.append(card.completed_datetime.date())
            else:
                counts[list.list_id]["total_incomplete"] += 1 # calculate how many tasks are incomplete
                if today > card.deadline:
                    counts[list.list_id]["d_passed"] += 1 # Out of the total incomplete tasks, calculate how many have passed the deadline

        for i in date_count:
            if i in d.keys():
                d[i] +=1
            else:
                d[i] = 1
        

        n=len(d.keys())
        r = np.arange(n)
       
        width = 0.25

        plt.clf()
        plt.bar(r, d.values(), color=["cornflowerblue"],
                width = width, edgecolor = 'black')
        plt.xlabel("Date of completion")
        plt.ylabel("No. of tasks completed")
        plt.title("No. of tasks completed vs Date of completion")

        max_el = 0
        if len(d.values()) > 0:
            max_el = max(d.values())
        
        y_ticks_labels = [i for i in range(max_el+1)]

        plt.xticks(r+width//2, d.keys())
        plt.yticks(y_ticks_labels, y_ticks_labels)

        if len(date_count) > 0:
            plt.savefig(f'static/png/{list.list_id}.png')
        
        counts[list.list_id]["date_count"] = date_count

    return render_template("summary.html", title="Kanban - Summary", lists=lists, counts=counts)


# register route
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(meta={'csrf': False})

    if request.method == "GET":
        return render_template("register.html", title="Kanban - Sign up", form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = form.password.data

            check_user = User.query.filter_by(email=email).first()

            if check_user:
                return render_template("error.html", message="User already exists with this email address!", form=form, extras="Sign in", name="login")

            hashed = generate_password_hash(password, method='sha256')
            new_user = User(email=email, name = name, password=hashed)

            db.session.add(new_user)
            db.session.commit()

            print(new_user.created_at)
            print(new_user.updated_at)

            return redirect(url_for('login'))
        else:
            return render_template("error.html", message = "", form=form, extras="Go back", name="register")


# login route
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(meta={'csrf': False})

    if request.method == "GET":
        return render_template("login.html", title="Kanban - Sign in", form=form)

    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()

            if not user:
                return render_template("error.html", message="Incorrect email or password", form=form, extras="Retry", name="login")

            hashed = user.password

            check_password = check_password_hash(hashed, password)

            if not check_password:
                return render_template("error.html", message="Incorrect email or password", form=form, extras="Retry", name="login")
            
            login_user(user)

            return redirect(url_for("home"))
        else:
            return render_template("error.html", message="", form=form, extras="Go back", name="login")



# logout route
@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))



# add list route
@app.route("/list/add", methods=["GET", "POST"])
@login_required
def add_list():
    form = AddListForm(meta={'csrf': False})

    if request.method == "GET":
        return render_template("add_list.html", title="Kanban - Add a List", form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data

            user_id = current_user.id

            lists = List.query.filter_by(user=user_id).all()

            if len(lists) > 4:
                return render_template("error.html", message="Cannot create more than 5 lists!", form=form, extras="Go back", name="home")

            new_list = List(name=name, user=user_id)
            db.session.add(new_list)
            db.session.commit()

            return redirect(url_for('home'))
        else:
            return render_template("error.html", message="", form=form, extras="Go back", name="add_list")


# edit list route
@app.route("/list/edit/<int:list_id>", methods=["GET", "POST"])
@login_required
def edit_list(list_id):
    form = EditListForm(meta={'csrf': False})
    list = List.query.get(list_id)


    if request.method == "GET":
        return render_template("edit_list.html", title="Kanban - Edit a List", list=list, form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
    
            list = List.query.get(list_id)

            list.name = name

            db.session.add(list)
            db.session.commit()

            return redirect(url_for('home'))
        else:
            return render_template("error.html", message="", form=form, extras="Go back", name="home")



# delete list route
@app.route("/list/delete/<int:list_id>", methods=["GET"])
@login_required
def delete_list(list_id):
    list = List.query.get(list_id)

    db.session.delete(list)
    db.session.commit()

    return redirect(url_for("home"))


# add card route
@app.route("/card/add/<int:list_id>", methods=["GET", "POST"])
@login_required
def add_card(list_id):
    form = AddCardForm(meta={'csrf': False}, completed=0)

    if request.method == "GET":
        return render_template("add_card.html", title="Kanban - Add a Card", list_id=list_id, form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            deadline = form.deadline.data
            completed  = form.completed.data
            list_id = list_id

            completed_datetime = None

            if form.completed.data == '1':
                completed_datetime = datetime.now()

            new_card = Card(title=title, content=content,
                            deadline=deadline, completed=completed, completed_datetime=completed_datetime, list=list_id)

            db.session.add(new_card)
            db.session.commit()

            return redirect(url_for("home"))
        else:
            return render_template("error.html", message="", form=form, extras="Go back", name="home")



# edit card route
@app.route("/card/edit/<int:card_id>", methods=["GET", "POST"])
@login_required
def edit_card(card_id):
    user_id = current_user.id
    card = Card.query.get(card_id)
    lists = List.query.filter_by(user=user_id).all()


    form = EditCardForm(meta={'csrf': False}, completed=card.completed, list=card.list)
    form.list.choices = [(list.list_id, list.name) for list in lists]


    if request.method == "GET":
        return render_template("edit_card.html", title="Kanban - Edit a Card", lists=lists, card=card, form = form)
    if request.method == "POST":
        if form.validate_on_submit():
            list_id = form.list.data

            title = form.title.data
            content = form.content.data
            deadline = form.deadline.data
            completed = form.completed.data
            list_id = list_id

            completed_datetime = None

            if form.completed.data == '1':
                completed_datetime = datetime.now()

            card.title = title
            card.content = content
            card.deadline = deadline
            card.completed = completed
            card.completed_datetime = completed_datetime
            card.list = list_id

            db.session.add(card)
            db.session.commit()

            return redirect(url_for("home"))
        else:
            return render_template("error.html", message="", form=form, extras="Go back", name="home")


# delete card route
@app.route("/card/delete/<int:card_id>", methods=["GET"])
@login_required
def delete_card(card_id):
    card = Card.query.get(card_id)

    db.session.delete(card)
    db.session.commit()

    return redirect(url_for("home"))