"""
Author: Jonathan Grenz
Created: July 2019
Title: Learning Journal with Flask
Description:

Create an interface for a learning journal web application. The main
(index) page lists journal entry titles and dates. Each journal entry
title links to a detail page that displays the title, date, time spent,
the journal entry, and resources related to the learning.

The application lets the user add or edit journal entries. When adding
or editing a journal entry, the application prompts the user for title,
date, time spent, what they learned, and resources to remember. The
results for these entries are stored in a database and displayed in a
blog style website. The HTML/CSS for this site has been supplied for
you.

"""
from flask import (Flask, g, render_template, flash, redirect, url_for,
                   abort, request)

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'auoesh.bouoastuh.43,uoausoehuosth3ououea.auoub!'


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route('/')
@app.route('/entries')
def index():
    """index is the main page which lists all journal entries."""
    entries = models.Entry.select().limit(100)
    return render_template('index.html', entries=entries)


@app.route('/entries/new', methods=('GET', 'POST'))
def new_entry():
    '''new_entry allows the user to create a new journal entry'''
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.create(
            title=form.title.data.strip(),
            timestamp=form.timestamp.data,
            time_spent=form.time_spent.data.strip(),
            content=form.content.data.strip(),
            resources=form.resources.data.strip()
        )
        print('success')
        flash("Entry posted!", "success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/entries/<int:id>')
def view_entry_detail(id):
    '''
    view_entry_detail allows the user to view the details of the
    selected journal.
    '''
    entry = models.Entry.select().where(models.Entry.id == id)
    if entry.count() == 0:
        abort(404)
    return render_template('detail.html', entry=entry)


# I adapted portions of the following edit_entry code from Mike at:
# http://www.blog.pythonlibrary.org/2017/12/14/flask-101-adding-editing
# -and-displaying-data/
#
# and Brian Weber at:
# https://github.com/brianweber2/project5_learning_journal_flask/blob/m
# aster/app.py
@app.route('/entries/<int:id>/edit', methods=('GET', 'POST'))
def edit_entry(id):
    '''edit_entry enables the user to edit/update a journal entry.'''
    try:
        entry = models.Entry.select().where(models.Entry.id == id).get()
    except models.DoesNotExist:
        abort(404)
    else:
        form = forms.EntryForm(obj=entry)
        if request.method == 'POST' and form.validate():
            entry.title = form.title.data
            entry.timestamp = form.timestamp.data
            entry.time_spent = form.time_spent.data
            entry.content = form.content.data
            entry.resources = form.resources.data
            entry.save()
            flash("Your edit has been saved!", "success")
            return redirect("/")
    return render_template("edit.html", form=form, entry=entry)


@app.route('/entries/<int:id>/delete', methods=('GET', 'POST'))
def delete_entry(id):
    '''delete_entry allows the user to delete journal entries.'''
    try:
        entry = models.Entry.select().where(models.Entry.id == id).get()
    except models.DoesNotExist:
        abort(404)
    else:
        entry.delete_instance()
        flash("Your Journal Entry Has Been Deleted!", "success")
    return redirect('/')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
    
