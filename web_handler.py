from flask import Flask, render_template, request, redirect, url_for
from shorturldb import execute_sql, update_url_record, delete_url_record_by_rid, insert_url_record


app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return redirect(url_for('display_all_shortcuts'))


@app.route("/<string:short_url>")
def go_to_link(short_url):
    url_records = execute_sql("SELECT * FROM url WHERE short = '{}'".format(short_url))
    if len(url_records) != 0:
        rid, short, link = url_records[0]
        return redirect(link)
    else:
        return "your short cut /" + short_url + " doesn't exist."

#READ
@app.route("/display_all_shortcuts")
def display_all_shortcuts():
    url_records = execute_sql("SELECT * FROM url") # read sql
    return render_template("display_all_shortcuts.html", records=url_records)

#UPDATE    
@app.route("/edit_short_link/<string:rid>", methods=['GET', 'POST'])
def edit_short_link(rid):

    url_records = execute_sql("SELECT * FROM url WHERE rid = '{}'".format(rid))
    if len(url_records) != 0:
        rid, short, link = url_records[0]
        if request.method == 'POST':
            update_url_record((request.form['short'], request.form['link'], rid))
            return redirect(url_for('display_all_shortcuts'))
        else:
            return render_template("edit_short_link.html", rid=rid, short=short, link=link)


#DELETE
@app.route("/delete_short_link/<string:rid>")
def delete_short_link(rid):

    url_records = execute_sql("SELECT * FROM url WHERE rid = '{}'".format(rid))
    if len(url_records) != 0:
        delete_url_record_by_rid(rid)
    return redirect(url_for('display_all_shortcuts'))


#CREATE
@app.route("/new_short_link/", methods=['GET', 'POST'])
def new_short_link():
    if request.method == 'POST':
        insert_url_record((request.form['short'], request.form['link']))
        return redirect(url_for('display_all_shortcuts'))
    else:
        return render_template("new_short_link.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
