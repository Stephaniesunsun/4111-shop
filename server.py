#!/usr/bin/env python

"""
Columbia's COMS W4111.003 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import mimetypes
import os
from re import M
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, json

tmpl_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of:
#
# postgresql://USER:PASSWORD@104.196.152.219/proj1part2
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.152.219/proj1part2"
#
DATABASEURI = "postgresql://ws2614:7391@35.211.155.104/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute(
    """INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
    """
    This function is run at the beginning of every web request 
    (every time you enter an address in the web browser).
    We use it to setup a database connection that can be used throughout the request.

    The variable g is globally accessible.
    """
    try:
        g.conn = engine.connect()
    except:
        print('uh oh, problem connecting to database')
        import traceback
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't, the database could run out of memory!
    """
    try:
        g.conn.close()
    except Exception as e:
        pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    request is a special object that Flask provides to access web request information:

    request.method:   "GET" or "POST"
    request.form:     if the browser submitted a form, this contains the data in the form
    request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2
comm
    See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
    """

    # DEBUG: this is debugging code to see what request looks like
    print(request.args)
    username = ''
    password = ''

    if request.method == 'POST':
        username = request.form['email_cu']
        password = request.form['password_cu']

    print(username, password)

#
    # example of a database query
    #
    #cursor = g.conn.execute("SELECT name FROM test")
    #names = []
    # for result in cursor:
    #   names.append(result['name'])  # can also be accessed using result[0]
    # cursor.close()

    #
    #context = dict(data=names)

    #
    # render_template looks in the templates/ folder for files.
    # for example, the below file reads template/index.html
    #
    return render_template("index.html"), 200


@app.route('/customer', methods=['GET'])  # fetch all products
def customer():
    cursor = g.conn.execute("SELECT * FROM product")
    products = []

    for result in cursor:
        row_as_dict = dict(result)
        products.append(row_as_dict)
    cursor.close()
    return render_template("customer.html", products=products)


@app.route('/product/<id>', methods=['GET'])  # fetch all products
def product(id=0):
    print('haha', id)
    sql = text("SELECT * FROM product WHERE product_id=:pid")

    cursor = g.conn.execute(sql, pid=id)
    row = cursor.fetchone()
    print(row)

    return render_template("product.html")


@app.route('/employee', methods=['GET', 'POST'])
def employee():
    args = request.args
    print(args)

    return render_template("employee.html")

# Example of adding new data to the database


@app.route('/add', methods=['POST'])
def add():
    id = request.form['add_id']
    name = request.form['add_name']
    price = request.form['add_price']
    brand = request.form['add_brand']
    stock = request.form['add_stock']
    stockid = request.form['add_stockid']
    size = request.form['add_size']

    sql = text('INSERT INTO product(product_id,product_name,price,stock_id,stock_num,cloth_size,brand) VALUES (:pid,:pname,:pprice,:pstockid,:pstock,:psize,:pbrand)')
    g.conn.execute(sql, pid=id, pname=name, pprice=price,
                   pbrand=brand, pstock=stock, pstockid=stockid, psize=size)
    return redirect('/employee')


@app.route('/delete', methods=['POST'])
def delete():
    id = request.form['delete_id']
    name = request.form['delete_name']

    sql = text('DELETE FROM product WHERE product_id=:pid')
    cursor = g.conn.execute(sql, pid=id)
    return redirect('/employee')


@app.route('/update', methods=['POST'])
def update():
    id = request.form['update_id']
    field = request.form['options']
    value = request.form['update_field']

    if field == 'product_name':
        sql = text(
            'UPDATE product SET product_name=:pvalue WHERE product_id=:pid')
        cursor = g.conn.execute(sql, pid=id, pvalue=value)
        return redirect('/employee')
    elif field == 'price':
        sql = text('UPDATE product SET price=:pvalue WHERE product_id=:pid')
        cursor = g.conn.execute(sql, pid=id, pvalue=value)
        return redirect('/employee')
    elif field == 'brand':
        sql = text('UPDATE product SET brand=:pvalue WHERE product_id=:pid')
        cursor = g.conn.execute(sql, pid=id, pvalue=value)
        return redirect('/employee')
    elif field == 'stock_num':
        sql = text('UPDATE product SET stock_num=:pvalue WHERE product_id=:pid')
        cursor = g.conn.execute(sql, pid=id, pvalue=value)
        return redirect('/employee')
    elif field == 'stock_id':
        sql = text('UPDATE product SET stock_id=:pvalue WHERE product_id=:pid')
        cursor = g.conn.execute(sql, pid=id, pvalue=value)
        return redirect('/employee')
    elif field == 'cloth_size':
        sql = text('UPDATE product SET cloth_size=:pvalue WHERE product_id=:pid')
        cursor = g.conn.execute(sql, pid=id, pvalue=value)
        return redirect('/employee')


@app.route('/readcustomer', methods=['POST'])
def readcustomer():
    id = request.form['update_id']
    field = request.form['options']
    value = request.form['update_field']

    sql = text('UPDATE product SET :pfield=:pvalue WHERE product_id=:pid')
    cursor = g.conn.execute(sql, pid=id, pfield=field, pvalue=value)
    return redirect('/employee', customer=customer)


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        Run the server using:

            python server.py

        Show the help text using:

            python server.py --help

        """

        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

    run()
