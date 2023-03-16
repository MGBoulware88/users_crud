from flask import Flask, render_template, request, redirect, session
from user import User
from datetime import datetime
app = Flask(__name__)
secret_key = "CHANGEME"

@app.route("/")
def index():
    # call the get_all_users(cls, data) classmethod to populate the HTML
    users = User.get_all_users()
    print(users)
    for user in users:
        print(user.first_name, user.last_name)
    return render_template("index.html", users = users)


@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/users/create", methods=['POST'])
def create_user():
    User.create(request.form)
    return redirect("/")

@app.route("/users/<int:id>")
def read_one(id):
    user_list = User.get_one_user(id)
    user = user_list[0]
    created_date = datetime.strptime(str(user["created_at"]), "%Y-%m-%d %H:%M:%S")
    user["created_at"] = created_date.strftime("%B %d, %Y")
    updated_date = datetime.strptime(str(user["updated_at"]), "%Y-%m-%d %H:%M:%S")
    user["updated_at"] = updated_date.strftime("%B %d, %Y")
    return render_template("read_one.html", user=user)

@app.route("/users/<int:id>/edit")
def edit(id):
    user_list = User.get_one_user(id)
    user = user_list[0]
    return render_template("edit.html", user=user)

@app.route("/users/<int:id>/edit_user", methods=["POST"])
def edit_user(id):
    data = {
        **request.form,
        'id' : id
    }
    User.update_user(data)
    return redirect(f"/users/{id}")

@app.route("/users/<int:id>/destroy")
def delete_user(id):
    data = {
        'id':id
    }
    User.delete_user(data)
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)