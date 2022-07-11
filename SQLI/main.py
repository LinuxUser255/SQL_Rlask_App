#!/usr/bin/env python3

# Building a flask SQLite database web app using Jinja template engine
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3#step-4-setting-up-the-database

import re
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

# You will need to comment out one of the get_db(): functions before running this script

# Correct/safe
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# Bad: Vulnerable to SQL Injection
def get_db_connection():
    conn = get_db_connection()
 """
  problem with the regex the provided value begins and ends with only numbers as indicated by \d
  also, re.M indicates a multi-line regex evaluation
  so, only one line needs to match, you could make a value of 123, new line,
  UNION SELECT Passwords from users..this leads to SQLI below in the post variable
  the post id is catted to the remaining query
"""
    num_format = re.compile(r'^\d+$', re.M) # weak regex
        if re.match(num_format,post_id):
        # SQLI vuln, passes user input to string
            post = conn.execute('SELECT * FROM posts WHERE id = '+post_id).fetchone()
            conn.close()
            if post is None:
                abort(404)
            return post
        else:
            abort(404)





# Vulnerable to SQL Injection
# def get_post(post_id):
#     conn = get_db_connection()
#     # file paths that contain numerical digits, exe: /1 throw an error, but not if prefixed with a letter /?id=1 works
#     num_format = re.compile(r'^\d+$', re.M) # 127.0.0.1:5000/?id=1 refreshes the page only /?=1 also works
#     if re.match(num_format, post_id):
#         post = conn.execute('SELECT * FROM posts WHERE id = ' + post_id).fetchone()
#         conn.close()
#         if post is None:
#             abort(404)
#             return
#         else:
#             abort(404)


def get_post(post_id):
    conn = get_db_connection()  # SQL configured to schema.sql
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qwerty12345'


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

# @app.route('/create', methods=('GET', 'POST'))
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form
#
#         if title:
#             conn = get_db_connection()
#             conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
#                          (title, content))
#             conn.commit()
#             conn.close()
#             return redirect(url_for('index'))
#         else:
#             flash('Title is required')
#
#     return render_template('create.html')


# def get_post(post_id):
# Vulnerable to SQLi
# def get_post(post_id):
#     conn = get_db_connection()
#     num_format = re.compile(r'^\d+$', re.M)  # regex begins and ends with only numbers & multiline
#     if re.match(num_format, post_id):  # and the lack of filtering passes input to post_id
#         post = conn.execute('SELECT * FROM posts WHERE id = ' + post_id).fetchone()
#         conn.close()
#         if post is None:
#             abort(404)
#         return post
#     else:
#         abort(404)

# CORRECT SAFE CODE
# conn = get_db_connection()
# post = conn.execute('SELECT * FROM posts WHERE id = ?',
#                     (post_id,)).fetchone()
# conn.close()
# if post is None:
#     abort(404)
# return post


# could injecting ' comas and or <> escape the param and lead to exploit?


# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=8080, debug=True)

# if __name__ == '__main__':
#     main()
