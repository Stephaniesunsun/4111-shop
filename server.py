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
from unicodedata import name
from numpy import size
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
engine = create_engine(DATABASEURI)


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


@app.route('/', methods=['GET', 'POST'])  # fetch all products
def index():
    cursor = g.conn.execute("SELECT * FROM product")
    products = []

    for result in cursor:
        row_as_dict = dict(result)
        products.append(row_as_dict)
    cursor.close()

    return render_template("index.html", products=products)


@app.route('/login_customer', methods=['GET'])
def cus_switch():
    args = request.args
    print(args)

    return render_template("customer.html")


@app.route('/customer', methods=['POST'])
def customer():
    if request.method == 'POST':
        username = request.form['email_cu']
        password1 = request.form['password_cu']
        customer = []
        sql = text(
            "SELECT * FROM customer WHERE contact_info=:cname AND password=:pwd")
        cursor = g.conn.execute(sql, cname=username, pwd=password1)
        for result in cursor:
            row_as_dict = dict(result)
            customer.append(row_as_dict)
        cursor.close()

        if not customer:
            print('not found')
            return redirect('/')
        else:
            sql2 = text("SELECT address_name FROM customer_address JOIN customer ON customer_address.customer_id=customer.customer_id WHERE customer.contact_info=:cname AND customer.password=:cpwd")
            shipping = []
            cursor = g.conn.execute(sql2, cname=username, cpwd=password1)
            for result in cursor:
                row_as_dict = dict(result)
                shipping.append(row_as_dict)
            print(shipping)
            cursor.close()

            return render_template("checkout.html", customers=customer, shipping=shipping)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        print(request.form)

    return "Thanks for your support!"


@app.route('/signup', methods=['POST', 'GET'])
def cus_signup_jump():
    args = request.args
    print(args)

    return render_template("signup_customer.html")


@app.route('/signup_customer', methods=['POST', 'GET'])
def cus_signup():
    if request.method == 'POST':
        email = request.form['cus_email']
        name = request.form['cus_name']
        size = request.form['cus_size']
        password = request.form['cus_pw']
        password2 = request.form['cus_pw2']
        if password == password2:
            sql = text(
                "INSERT INTO customer(name,size,contact_info,password) VALUES \
                    (:textname,:textsize,:textemail,:textpassword)"
            )
            g.conn.execute(sql, textname=name, textsize=size,
                           textemail=email, textpassword=password)
            print('sucessfully inserted new customer')
            return redirect('/')
        else:
            return redirect('/login_customer')

    # return render_template("signup_customer.html")


@app.route('/login_employee', methods=['GET'])
def emp_switch():
    args = request.args
    print(args)

    return render_template("login_employee.html")


@app.route('/emp-login', methods=['POST'])  # fetch all products
def emp_login():
    id = request.form['emp_id']
    name = request.form['emp_name']
    age = request.form['emp_age']
    employee = []
    sql = text(
        "SELECT employee_id FROM employee WHERE employee_id=:eid AND name=:ename AND age=:eage")
    cursor = g.conn.execute(sql, eid=id, ename=name, eage=age)
    for result in cursor:
        row_as_dict = dict(result)
        employee.append(row_as_dict)
    cursor.close()

    if not employee:
        return redirect('login_employee')
    return render_template("employee.html")


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
    cursor.close()
    return redirect('/employee')


@app.route('/update', methods=['POST'])
def update():
    id = request.form['update_id']
    field = request.form['options']
    value = request.form['update_field']

    if field == 'product_name':
        sql = text(
            'UPDATE product SET product_name=:pvalue WHERE product_id=:pid')

    elif field == 'price':
        sql = text('UPDATE product SET price=:pvalue WHERE product_id=:pid')

    elif field == 'brand':
        sql = text('UPDATE product SET brand=:pvalue WHERE product_id=:pid')

    elif field == 'stock_num':
        sql = text('UPDATE product SET stock_num=:pvalue WHERE product_id=:pid')

    elif field == 'stock_id':
        sql = text('UPDATE product SET stock_id=:pvalue WHERE product_id=:pid')

    elif field == 'cloth_size':
        sql = text('UPDATE product SET cloth_size=:pvalue WHERE product_id=:pid')

    cursor = g.conn.execute(sql, pid=id, pvalue=value)
    cursor.close()
    return redirect('/employee')


@app.route('/readcustomer', methods=['POST'])
def readcustomer():
    id = request.form['customer_id']
    orders = []
    sql = text('SELECT name,contact_info,order_id FROM customer JOIN purchase ON customer.customer_id=purchase.customer_id WHERE customer.customer_id=:cid')
    cursor = g.conn.execute(sql, cid=id)

    for result in cursor:
        row_as_dict = dict(result)
        orders.append(row_as_dict)
    cursor.close()

    return render_template('employee.html', orders=orders)


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
