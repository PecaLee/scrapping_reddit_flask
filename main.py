from db import add_subreddit
from flask import Flask, render_template, request, redirect

app = Flask("DayEleven")

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

db_all = {}


@app.route("/")
def root_page():
    return render_template("home.html", subreddits=subreddits)


@app.route("/add", methods=['POST'])
def add_page():
    post = request.form["new_subreddit"]
    result = ""
    if "r/" in post:
        result = "r"
    else:
        if add_subreddit(post) != None:
            subreddits.append(post)
            db_all[post] = add_subreddit(post)
            return redirect("/")
        else:
            result = None
    return render_template("add.html", submits=post, result=result)


@app.route("/read")
def read_page():
    selecteds = []
    list_db = []
    for subreddit in subreddits:
        init_page = request.args.get(subreddit)
        if init_page == "on":
            selecteds.append(subreddit)
    for selected in selecteds:
        if selected not in db_all:
            db_all[selected] = add_subreddit(selected)
        for inner_db in db_all[selected]:
            list_db.append(inner_db)
    sorted_db = sorted(list_db, key=(lambda listed: int(
        listed["vote"].replace(".", "").replace("k", "000"))), reverse=True)

    return render_template("read.html", selecteds=selecteds, db_all=sorted_db)


app.run()
