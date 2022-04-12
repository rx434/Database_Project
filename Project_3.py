# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 14:42:29 2020

@author: xinfe
"""

from flask import Flask, render_template, request, session, url_for, redirect, Markup
import pymysql.cursors
import json

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='project',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def before_login():
	return render_template('before_login.html')

@app.route('/searchflight', methods=['GET', 'POST'])
def search_flight():
    source_city = request.form['source_city']
    destination_city = request.form['destination_city']
    date = request.form['date']

    cursor = conn.cursor()
    query = 'SELECT * FROM flight_information WHERE departure_city = %s AND arrival_city = %s AND date(departure_time) = %s AND status = %s'
    cursor.execute(query, (source_city, destination_city, date, 'upcoming'))
    flights = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template('before_login.html', flights = flights)

@app.route('/searchstatus', methods=['GET', 'POST'])
def search_status():
    airline = request.form['airline']
    flight_num = request.form['flight_number']
    
    cursor = conn.cursor()
    query = 'SELECT airline_name, flight_num, status FROM flight WHERE airline_name = %s AND flight_num = %s'
    cursor.execute(query, (airline, flight_num))
    status = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template('before_login.html', status = status)

#This block is all about login
@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/customerlogin')
def customer_login():
    return render_template('customer_login.html')

@app.route('/cloginAuth', methods=['GET', 'POST'])
def cloginAuth():
    username = request.form['username']
    password = request.form['password']
    
    cursor = conn.cursor()
    query = 'SELECT * FROM customer WHERE email = %s AND password = md5(%s)'
    cursor.execute(query, (username, password))
    
    data = cursor.fetchone()
    conn.commit()
    cursor.close()
    
    if (data):
        session['username'] = username
        session['role'] = 'customer'
        session['booking_agent_id'] = 'null'
        return redirect(url_for('home'))
    
    else:
        error = 'Invalid username and password'
        return render_template('customer_login.html', error = error)

@app.route('/agentlogin')
def agent_login():
    return render_template('agent_login.html')

@app.route('/aloginAuth', methods=['GET', 'POST'])
def aloginAuth():
    username = request.form['username']
    password = request.form['password']
    agent_id = request.form['agent_id']
    
    cursor = conn.cursor()
    query = 'SELECT * FROM booking_agent WHERE email = %s AND password = md5(%s) AND booking_agent_id = %s'
    cursor.execute(query, (username, password, agent_id))
    
    data = cursor.fetchone()
    conn.commit()
    cursor.close()
    
    if (data):
        session['username'] = username
        session['role'] = 'booking_agent'
        session['booking_agent_id'] = agent_id
        return redirect(url_for('home'))
    
    else:
        error = 'Invalid username and password'
        return render_template('agent_login.html', error = error)

@app.route('/stafflogin')
def staff_login():
    return render_template('staff_login.html')

@app.route('/sloginAuth', methods=['GET', 'POST'])
def sloginAuth():
    username = request.form['username']
    password = request.form['password']
    
    cursor = conn.cursor()
    query = 'SELECT * FROM airline_staff WHERE username = %s AND password = md5(%s)'
    cursor.execute(query, (username, password))
    
    data = cursor.fetchone()
    conn.commit()
    cursor.close()
    
    if (data):
        session['username'] = username
        session['role'] = 'airline_staff'
        session['booking_agent_id'] = 'null'
        session['agent_airline'] = data['airline_name']
        return redirect(url_for('home'))
    
    else:
        error = 'Invalid username and password'
        return render_template('staff_login.html', error = error)

#This biock is all about register
@app.route('/register')
def register():
	return render_template('register.html')
    
    
@app.route('/customerregister')
def customer_register():
    return render_template('customer_register.html') 

@app.route('/cregisterAuth', methods=['GET', 'POST'])
def cregisterAuth():
    email = request.form['email']
    name = request.form['name']
    phone_number = request.form['phone_number']
    date_of_birth = request.form['date_of_birth']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    building_number = request.form['building_number']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    passport_number = request.form['passport_number']
    passport_expiration = request.form['passport_expiration']
    passport_country = request.form['passport_country']
	
    cursor = conn.cursor()
    
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (email))
    
    data = cursor.fetchone()
    
    error = None
    if (data):
        error = "This user already exists"
        return render_template('customer_register.html', error = error)
    else:
        if (password != confirm_password):
            error = "Your confirm password doesn't fit to your password"
            conn.commit()
            cursor.close()
            return render_template('customer_register.html', error = error)
        else:
            ins = 'INSERT INTO customer VALUES(%s, %s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(ins, (email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth))
            conn.commit()
            cursor.close()
            return render_template('register_success.html')

@app.route('/agentregister')
def agent_register():
    return render_template('agent_register.html')

@app.route('/aregisterAuth', methods=['GET', 'POST'])
def aregisterAuth():
    email = request.form['email']
    booking_agent_id = request.form['booking_agent_id']
    password = request.form['password']
    confirm_password = confirm_password = request.form['confirm_password']
    
    cursor = conn.cursor()
    
    query = 'SELECT * FROM booking_agent WHERE email = %s'
    cursor.execute(query, (email))
    
    data = cursor.fetchone()
    
    error = None
    if (data):
        error = "This user already exists"
        return render_template('agent_register.html', error = error)
    else:
        if (password != confirm_password):
            error = "Your confirm password doesn't fit to your password"
            conn.commit()
            cursor.close()
            return render_template('agent_register.html', error = error)
        else:
            ins = 'INSERT INTO booking_agent VALUES(%s, md5(%s), %s)'
            cursor.execute(ins, (email, password, booking_agent_id))
            conn.commit()
            cursor.close()
            return render_template('register_success.html')

@app.route('/staffregister')
def staff_register():
    return render_template('staff_register.html')

@app.route('/sregisterAuth', methods=['GET', 'POST'])
def sregisterAuth():
    username = request.form['username']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    airline_name = request.form['airline_name']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    cursor = conn.cursor()
    
    query = 'SELECT * FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
    
    data = cursor.fetchone()
    
    error = None
    if (data):
        error = "This user already exists"
        return render_template('staff_register.html', error = error)
    else:
        if (password != confirm_password):
            error = "Your confirm password doesn't fit to your password"
            conn.commit()
            cursor.close()
            return render_template('staff_register.html', error = error)
        else:
            query = 'SELECT * FROM airline WHERE airline_name = %s'
            cursor.execute(query, (airline_name))
            data = cursor.fetchone()
            if not (data):
                ins = 'INSERT INTO airline VALUES(%s)'
                cursor.execute(ins, (airline_name))
            ins = 'INSERT INTO airline_staff VALUES(%s, md5(%s), %s, %s, %s, %s)'
            cursor.execute(ins, (username, password, first_name, last_name, date_of_birth, airline_name))
            conn.commit()
            cursor.close()
            return render_template('register_success.html')
        
#This block is all about home
@app.route('/home', methods=['GET', 'POST'])
def home():
    username = session['username']
    role = session['role']
    return render_template('home.html', username = username, role = role)

@app.route('/logout')
def logout():
    if session['role'] == 'airline_staff':
        session.pop('agent_airline')
    session.pop('username')
    session.pop('role')
    session.pop('booking_agent_id')
    return redirect('/')

#This block is all about customer's valid operation
@app.route('/home/customer/view', methods=['GET', 'POST'])
def customer_view():
    customer_email = session['username']
    
    cursor = conn.cursor()
    query = 'SELECT * FROM user_purchase_information WHERE customer_email = %s ORDER BY purchase_date'
    cursor.execute(query, (customer_email))
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template('customer_view.html', flights = data)

@app.route('/home/customer/searchstatus', methods=['GET', 'POST'])
def customer_search_status():
    airline = request.form['airline']
    flight_num = request.form['flight_number']
    
    cursor = conn.cursor()
    query = 'SELECT airline_name, flight_num, status FROM flight WHERE airline_name = %s AND flight_num = %s'
    cursor.execute(query, (airline, flight_num))
    status = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template('customer_view.html', status = status)

@app.route('/home/customer/searchflight', methods=['GET', 'POST'])
def customersearch():
    customer_email = session['username']
    
    from_date = request.form['from_date']
    to_date = request.form['to_date']
    departure_city = request.form['departure_city']
    arrival_city = request.form['arrival_city']
    
    cursor = conn.cursor()
    
    if (from_date, to_date, departure_city, arrival_city) == ('', '', '', ''): #0,0,0,0
        query = 'SELECT * FROM user_purchase_information WHERE customer_email = %s ORDER BY purchase_date'
        cursor.execute(query, (customer_email))
        data = cursor.fetchall()
    elif (from_date, to_date, departure_city) == ('', '', ''): #0,0,0,1
        query = 'SELECT * FROM user_purchase_information WHERE customer_email = %s AND arrival_city = %s ORDER BY purchase_date' 
        cursor.execute(query, (customer_email, arrival_city))
        data = cursor.fetchall()
    elif (from_date, to_date, arrival_city) == ('', '', ''): #0,0,1,0
        query = 'SELECT * FROM user_purchase_information WHERE customer_email = %s AND departure_city = %s ORDER BY purchase_date' 
        cursor.execute(query, (customer_email, departure_city))
        data = cursor.fetchall()
    elif (from_date, to_date) == ('', ''): #0,0,1,1
        query = 'SELECT * FROM user_purchase_information WHERE customer_email = %s AND departure_city = %s AND arrival_city = %s ORDER BY purchase_date' 
        cursor.execute(query, (customer_email, departure_city, arrival_city))
        data = cursor.fetchall()
    elif (from_date, departure_city, arrival_city) == ('', '', ''): #0,1,0,0
        query = 'SELECT * FROM user_purchase_information WHERE customer_email = %s AND purchase_date <= %s ORDER BY purchase_date' 
        cursor.execute(query, (customer_email, to_date))
        data = cursor.fetchall()
    elif (from_date, departure_city) == ('', ''): #0,1,0,1
        query = 'SELECT * FROM user_purchase_information WHERE customer_email = %s AND purchase_date <= %s AND arrival_city = %s ORDER BY purchase_date' 
        cursor.execute(query, (customer_email, to_date, arrival_city))
        data = cursor.fetchall()
    elif (from_date, arrival_city) == ('', ''): #0,1,1,0
        query = 'SELECT * FROM user_purchase_information WHERE customer_email = %s AND purchase_date <= %s AND departure_city = %s ORDER BY purchase_date' 
        cursor.execute(query, (customer_email, to_date, departure_city))
        data = cursor.fetchall()
    elif (from_date == ''): #0,1,1,1
        query = 'SELECT * FROM user_purchase_information WHERE customer_email = %s AND purchase_date <= %s AND departure_city = %s AND arrival_city = %s ORDER BY purchase_date'
        cursor.execute(query, (customer_email, to_date, departure_city, arrival_city))
        data = cursor.fetchall()
    elif (to_date, departure_city, arrival_city) == ('', '', ''): #1,0,0,0
        query = 'SELECT * FROM user_purchase_information WHERE customer_email = %s AND purchase_date >= %s ORDER BY purchase_date'
        cursor.execute(query, (customer_email, from_date))
        data = cursor.fetchall()
    elif (to_date, departure_city) == ('', ''): #1,0,0,1
        query = 'SELECT * FROM user_purchase_information WHERE customer_email = %s AND purchase_date >= %s AND arrival_city = %s ORDER BY purchase_date'
        cursor.execute(query, (customer_email, from_date, arrival_city))
        data = cursor.fetchall()
    elif (to_date, arrival_city) == ('', ''): #1,0,1,0
        query = 'SELECT * FROM user_purchase_information WHERE customer_email = %s AND purchase_date >= %s AND departure_city = %s ORDER BY purchase_date'
        cursor.execute(query, (customer_email, from_date, departure_city))
        data = cursor.fetchall()
    elif (to_date == ''): #1,0,1,1
        query = 'SELECT * FROM user_purchase_information WHERE customer_email = %s AND purchase_date >= %s AND departure_city = %s AND arrival_city = %s ORDER BY purchase_date'
        cursor.execute(query, (customer_email, from_date, departure_city, arrival_city))
        data = cursor.fetchall()
    elif (departure_city, arrival_city) == ('', ''): #1,1,0,0
        query = 'SELECT * FROM user_purchase_information WHERE customer_email = %s AND purchase_date >= %s AND purchase_date <= %s ORDER BY purchase_date'
        cursor.execute(query, (customer_email, from_date, to_date))
        data = cursor.fetchall()
    elif (departure_city == ''): #1,1,0,1
        query = 'SELECT * FROM user_purchase_information WHERE customer_email = %s AND purchase_date >= %s AND purchase_date <= %s AND arrival_city = %s ORDER BY purchase_date'
        cursor.execute(query, (customer_email, from_date, to_date, arrival_city))
        data = cursor.fetchall()
    elif (arrival_city == ''): #1,1,1,0
        query = 'SELECT * FROM user_purchase_information WHERE customer_email = %s AND purchase_date >= %s AND purchase_date <= %s AND departure_city = %s ORDER BY purchase_date'
        cursor.execute(query, (customer_email, from_date, to_date, departure_city))
        data = cursor.fetchall()
    else: #1,1,1,1
        query = 'SELECT * FROM user_purchase_information WHERE customer_email = %s AND purchase_date >= %s AND purchase_date <= %s AND departure_city = %s AND arrival_city = %s ORDER BY purchase_date'
        cursor.execute(query, (customer_email, from_date, to_date, departure_city, arrival_city))
        data = cursor.fetchall()

    conn.commit()
    cursor.close()
    return render_template('customer_view.html', flights = data)

@app.route('/home/customer/track', methods=['GET', 'POST'])
def customer_track():
    customer_email = session['username']
    
    cursor = conn.cursor()
    query = 'SELECT date_sub(current_date, interval 1 year) AS from_date, current_date AS to_date, SUM(price) AS money FROM user_purchase_information WHERE customer_email = %s AND purchase_date >= date_sub(current_date, interval 1 year) AND purchase_date <= current_date'
    cursor.execute(query, (customer_email))
    data1 = cursor.fetchone()
    
    query = "SELECT date_format(purchase_date, %s) AS month, SUM(price) AS monthly_cost FROM user_purchase_information u WHERE customer_email = %s AND purchase_date >= date_sub(current_date, interval 1 year) AND purchase_date <= current_date Group BY date_format(purchase_date, %s) ORDER BY month"
    cursor.execute(query, ('%Y-%m', customer_email, '%Y-%m'))
    data2 = cursor.fetchall()
    
    conn.commit()
    cursor.close()

    x_data = [line['month'] for line in data2]
    y_data = [float(line['monthly_cost']) for line in data2]


    return render_template('customer_track.html', x_data = Markup(json.dumps(x_data)), y_data = json.dumps(y_data), from_date = data1['from_date'], to_date = data1['to_date'], money = data1['money'])
   
@app.route('/home/customer/searchtrack', methods=['GET', 'POST'])
def customer_searchtrack():
    customer_email = session['username']
    error = None
    
    from_date = request.form['from_date']
    to_date = request.form['to_date']
    
    cursor = conn.cursor()
    query = 'SELECT %s AS from_date, %s AS to_date, SUM(price) AS money FROM user_purchase_information WHERE customer_email = %s AND purchase_date >= %s AND purchase_date <= %s'
    cursor.execute(query, (from_date, to_date, customer_email, from_date, to_date))
    data1 = cursor.fetchone()
    
    query = "SELECT date_format(purchase_date, %s) AS month, SUM(price) AS monthly_cost FROM user_purchase_information u WHERE customer_email = %s AND purchase_date >= %s AND purchase_date <= %s GROUP BY date_format(purchase_date, %s) ORDER BY month"
    cursor.execute(query, ('%Y-%m', customer_email, from_date, to_date, '%Y-%m'))
    data2 = cursor.fetchall()
    
    x_data = [line['month'] for line in data2]
    y_data = [float(line['monthly_cost']) for line in data2]
    
    if data1['from_date'] > data1['to_date']:
        error = 'invalid date'
        return render_template('customer_track.html', error = error)
    else:
        return render_template('customer_track.html', x_data = Markup(json.dumps(x_data)), y_data = json.dumps(y_data), from_date = data1['from_date'], to_date = data1['to_date'], money = data1['money'])
    
    
@app.route('/home/customer/searchandpurchase', methods=['GET', 'POST']) 
def searchandpurchase():
    return render_template('customer_purchase.html')

@app.route('/home/customer/searchtickets', methods=['GET', 'POST'])
def search_tickets():
    source_city = request.form['source_city']
    destination_city = request.form['destination_city']
    departure_time = request.form['date']
    
    cursor = conn.cursor()
    query = 'SELECT * FROM tickets_information WHERE status = %s AND departure_city = %s AND arrival_city = %s AND date(departure_time) = %s AND remainning_tickets > 0'
    cursor.execute(query, ('upcoming', source_city, destination_city, departure_time))
    data = cursor.fetchall()
    
    conn.commit()
    cursor.close()
    
    return render_template('customer_purchase.html', tickets = data)

@app.route('/customerpurchase', methods=['GET', 'POST'])
def customerpurchase():
    customer_email = session['username']
    airline_name = request.form['airline_name']
    flight_num = request.form['flight_num']
    
    cursor = conn.cursor()
    query = 'INSERT INTO ticket VALUES((SELECT MAX(ticket_id) + 1 FROM purchases), %s, %s)'
    cursor.execute(query, (airline_name, flight_num))
    conn.commit()
    cursor.close()
    
    cursor = conn.cursor()
    query = 'INSERT INTO purchases VALUES((SELECT MAX(ticket_id) FROM ticket), %s, null, current_date)'
    cursor.execute(query, (customer_email))
    conn.commit()
    cursor.close()
    
    return render_template('purchase_success.html')

#This block is all about booking_agents' valid operation
@app.route('/home/agent/view', methods=['GET', 'POST'])
def agent_view():
    booking_agent_id = session['booking_agent_id']
    
    cursor = conn.cursor()
    query = 'SELECT * FROM user_purchase_information WHERE booking_agent_id = %s ORDER BY purchase_date'
    cursor.execute(query, (booking_agent_id))
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template('agent_view.html', flights = data)

@app.route('/home/agent/searchstatus', methods=['GET', 'POST'])
def agent_search_status():
    airline = request.form['airline']
    flight_num = request.form['flight_number']
    
    cursor = conn.cursor()
    query = 'SELECT airline_name, flight_num, status FROM flight WHERE airline_name = %s AND flight_num = %s'
    cursor.execute(query, (airline, flight_num))
    status = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template('agent_view.html', status = status)

@app.route('/home/agent/searchflight', methods=['GET', 'POST'])
def agentsearch():
    booking_agent_id = session['booking_agent_id']
    
    from_date = request.form['from_date']
    to_date = request.form['to_date']
    departure_city = request.form['departure_city']
    arrival_city = request.form['arrival_city']
    
    cursor = conn.cursor()
    
    if (from_date, to_date, departure_city, arrival_city) == ('', '', '', ''): #0,0,0,0
        query = 'SELECT * FROM user_purchase_information WHERE booking_agent_id = %s ORDER BY purchase_date'
        cursor.execute(query, (booking_agent_id))
        data = cursor.fetchall()
    elif (from_date, to_date, departure_city) == ('', '', ''): #0,0,0,1
        query = 'SELECT * FROM user_purchase_information WHERE booking_agent_id = %s AND arrival_city = %s ORDER BY purchase_date' 
        cursor.execute(query, (booking_agent_id, arrival_city))
        data = cursor.fetchall()
    elif (from_date, to_date, arrival_city) == ('', '', ''): #0,0,1,0
        query = 'SELECT * FROM user_purchase_information WHERE booking_agent_id = %s AND departure_city = %s ORDER BY purchase_date' 
        cursor.execute(query, (booking_agent_id, departure_city))
        data = cursor.fetchall()
    elif (from_date, to_date) == ('', ''): #0,0,1,1
        query = 'SELECT * FROM user_purchase_information WHERE booking_agent_id = %s AND departure_city = %s AND arrival_city = %s ORDER BY purchase_date' 
        cursor.execute(query, (booking_agent_id, departure_city, arrival_city))
        data = cursor.fetchall()
    elif (from_date, departure_city, arrival_city) == ('', '', ''): #0,1,0,0
        query = 'SELECT * FROM user_purchase_information WHERE booking_agent_id = %s AND purchase_date <= %s ORDER BY purchase_date' 
        cursor.execute(query, (booking_agent_id, to_date))
        data = cursor.fetchall()
    elif (from_date, departure_city) == ('', ''): #0,1,0,1
        query = 'SELECT * FROM user_purchase_information WHERE booking_agent_id = %s AND purchase_date <= %s AND arrival_city = %s ORDER BY purchase_date' 
        cursor.execute(query, (booking_agent_id, to_date, arrival_city))
        data = cursor.fetchall()
    elif (from_date, arrival_city) == ('', ''): #0,1,1,0
        query = 'SELECT * FROM user_purchase_information WHERE booking_agent_id = %s AND purchase_date <= %s AND departure_city = %s ORDER BY purchase_date' 
        cursor.execute(query, (booking_agent_id, to_date, departure_city))
        data = cursor.fetchall()
    elif (from_date == ''): #0,1,1,1
        query = 'SELECT * FROM user_purchase_information WHERE booking_agent_id = %s AND purchase_date <= %s AND departure_city = %s AND arrival_city = %s ORDER BY purchase_date'
        cursor.execute(query, (booking_agent_id, to_date, departure_city, arrival_city))
        data = cursor.fetchall()
    elif (to_date, departure_city, arrival_city) == ('', '', ''): #1,0,0,0
        query = 'SELECT * FROM user_purchase_information WHERE booking_agent_id = %s AND purchase_date >= %s ORDER BY purchase_date'
        cursor.execute(query, (booking_agent_id, from_date))
        data = cursor.fetchall()
    elif (to_date, departure_city) == ('', ''): #1,0,0,1
        query = 'SELECT * FROM user_purchase_information WHERE booking_agent_id = %s AND purchase_date >= %s AND arrival_city = %s ORDER BY purchase_date'
        cursor.execute(query, (booking_agent_id, from_date, arrival_city))
        data = cursor.fetchall()
    elif (to_date, arrival_city) == ('', ''): #1,0,1,0
        query = 'SELECT * FROM user_purchase_information WHERE booking_agent_id = %s AND purchase_date >= %s AND departure_city = %s ORDER BY purchase_date'
        cursor.execute(query, (booking_agent_id, from_date, departure_city))
        data = cursor.fetchall()
    elif (to_date == ''): #1,0,1,1
        query = 'SELECT * FROM user_purchase_information WHERE booking_agent_id = %s AND purchase_date >= %s AND departure_city = %s AND arrival_city = %s ORDER BY purchase_date'
        cursor.execute(query, (booking_agent_id, from_date, departure_city, arrival_city))
        data = cursor.fetchall()
    elif (departure_city, arrival_city) == ('', ''): #1,1,0,0
        query = 'SELECT * FROM user_purchase_information WHERE booking_agent_id = %s AND purchase_date >= %s AND purchase_date <= %s ORDER BY purchase_date'
        cursor.execute(query, (booking_agent_id, from_date, to_date))
        data = cursor.fetchall()
    elif (departure_city == ''): #1,1,0,1
        query = 'SELECT * FROM user_purchase_information WHERE booking_agent_id = %s AND purchase_date >= %s AND purchase_date <= %s AND arrival_city = %s ORDER BY purchase_date'
        cursor.execute(query, (booking_agent_id, from_date, to_date, arrival_city))
        data = cursor.fetchall()
    elif (arrival_city == ''): #1,1,1,0
        query = 'SELECT * FROM user_purchase_information WHERE booking_agent_id = %s AND purchase_date >= %s AND purchase_date <= %s AND departure_city = %s ORDER BY purchase_date'
        cursor.execute(query, (booking_agent_id, from_date, to_date, departure_city))
        data = cursor.fetchall()
    else: #1,1,1,1
        query = 'SELECT * FROM user_purchase_information WHERE booking_agent_id = %s AND purchase_date >= %s AND purchase_date <= %s AND departure_city = %s AND arrival_city = %s ORDER BY purchase_date'
        cursor.execute(query, (booking_agent_id, from_date, to_date, departure_city, arrival_city))
        data = cursor.fetchall()

    conn.commit()
    cursor.close()
    return render_template('agent_view.html', flights = data)
 
@app.route('/home/agent/commission', methods=['GET', 'POST'])
def agentcommission():
    booking_agent_id = session['booking_agent_id']
    
    cursor = conn.cursor()
    query = 'SELECT date_sub(current_date, interval 30 DAY) AS from_date, current_date AS to_date, SUM(price * 0.1) AS total_amount_commission, AVG(price * 0.1) AS average_commission, COUNT(price) AS number_of_tickets FROM user_purchase_information WHERE booking_agent_id = %s AND purchase_date >= date_sub(current_date, interval 30 DAY) AND purchase_date <= current_date'
    cursor.execute(query, (booking_agent_id))
    data = cursor.fetchone()
    
    conn.commit()
    cursor.close()
    return render_template('agent_commission.html', from_date = data['from_date'], to_date = data['to_date'], total_amount_commission = data['total_amount_commission'], average_commission = data['average_commission'], number_of_tickets = data['number_of_tickets'])

@app.route('/home/agent/searchcommission', methods=['GET', 'POST'])
def searchcommission():
    booking_agent_id = session['booking_agent_id']
    from_date = request.form['from_date']
    to_date = request.form['to_date']
    error = None
    
    cursor = conn.cursor()
    query = 'SELECT %s AS from_date, %s AS to_date, SUM(price * 0.1) AS total_amount_commission, AVG(price * 0.1) AS average_commission, COUNT(price) AS number_of_tickets FROM user_purchase_information WHERE booking_agent_id = %s AND purchase_date >= %s AND purchase_date <= %s'
    cursor.execute(query, (from_date, to_date, booking_agent_id, from_date, to_date))
    data = cursor.fetchone()
    
    conn.commit()
    cursor.close()
    
    if data['from_date'] > data['to_date']:
        error = 'invalid date'
        return render_template('agent_commission.html', error = error)
    else:
        return render_template('agent_commission.html', from_date = data['from_date'], to_date = data['to_date'], total_amount_commission = data['total_amount_commission'], average_commission = data['average_commission'], number_of_tickets = data['number_of_tickets'])
    
    
    
@app.route('/home/agent/topcustomer', methods=['GET', 'POST'])
def top_customer():
    booking_agent_id = session['booking_agent_id']
    
    cursor = conn.cursor()
    query = 'SELECT customer_email, COUNT(price) AS number_of_tickets FROM user_purchase_information WHERE booking_agent_id = %s AND purchase_date >= date_sub(current_date, interval 6 MONTH) AND purchase_date <= current_date GROUP BY customer_email ORDER BY number_of_tickets DESC'
    cursor.execute(query, (booking_agent_id))
    data1 = cursor.fetchall()
    data1 = data1[:5]
    x_data1 = [line['customer_email'] for line in data1]
    y_data1 = [int(line['number_of_tickets']) for line in data1]
    
    query = 'SELECT date_sub(current_date, interval 6 MONTH) AS from_date1, current_date AS to_date1'
    cursor.execute(query)
    date1 = cursor.fetchone()
    
    query = 'SELECT customer_email, SUM(price * 0.1) AS amount_of_commission FROM user_purchase_information WHERE booking_agent_id = %s AND purchase_date >= date_sub(current_date, interval 1 YEAR) AND purchase_date <= current_date GROUP BY customer_email ORDER BY amount_of_commission DESC'
    cursor.execute(query, (booking_agent_id))
    data2 = cursor.fetchall()
    data2 = data2[:5]
    x_data2 = [line['customer_email'] for line in data2]
    y_data2 = [float(line['amount_of_commission']) for line in data2]
    
    query = 'SELECT date_sub(current_date, interval 1 YEAR) AS from_date2, current_date AS to_date2'
    cursor.execute(query)
    date2 = cursor.fetchone()

    conn.commit()
    cursor.close()
    
    return render_template('agent_topcustomers.html', x_data1 = Markup(json.dumps(x_data1)), y_data1 = json.dumps(y_data1), x_data2 = Markup(json.dumps(x_data2)), y_data2 = json.dumps(y_data2), from_date1 = date1['from_date1'], to_date1 = date1['to_date1'], from_date2 = date2['from_date2'], to_date2 = date2['to_date2'], data1 = data1, data2 = data2)
    
@app.route('/home/agent/searchandpurchase', methods=['GET', 'POST'])
def a_searchandpurchase():
    return render_template('agent_purchase.html')

@app.route('/home/agent/searchtickets', methods=['GET', 'POST'])
def a_searchtickets():
    source_city = request.form['source_city']
    destination_city = request.form['destination_city']
    departure_time = request.form['date']
    
    cursor = conn.cursor()
    query = 'SELECT * FROM tickets_information WHERE status = %s AND departure_city = %s AND arrival_city = %s AND date(departure_time) = %s AND remainning_tickets > 0'
    cursor.execute(query, ('upcoming', source_city, destination_city, departure_time))
    data = cursor.fetchall()
    
    conn.commit()
    cursor.close()
    
    return render_template('agent_purchase.html', tickets = data)

@app.route('/agentpurchase', methods=['GET', 'POST'])
def agent_purchase():
    booking_agent_id = session['booking_agent_id']
    customer_email = request.form['customer_email']
    airline_name = request.form['airline_name']
    flight_num = request.form['flight_num']
    
    cursor = conn.cursor()
    query = 'INSERT INTO ticket VALUES((SELECT MAX(ticket_id) + 1 FROM purchases), %s, %s)'
    cursor.execute(query, (airline_name, flight_num))
    conn.commit()
    cursor.close()
    
    cursor = conn.cursor()
    query = 'INSERT INTO purchases VALUES((SELECT MAX(ticket_id) FROM ticket), %s, %s, current_date)'
    cursor.execute(query, (customer_email, booking_agent_id))
    conn.commit()
    cursor.close()
    
    return render_template('purchase_success.html')
    
#This whole block is all about the functions of airline staff
@app.route('/home/staff/view', methods=['GET', 'POST'])
def staff_view():
    airline_name = session['agent_airline']
    
    cursor = conn.cursor()
    query = 'SELECT * FROM flight_information WHERE airline_name = %s AND date(departure_time) >= current_date AND date(departure_time) <= date_add(current_date, interval 30 day) AND status = %s'
    cursor.execute(query, (airline_name, 'upcoming'))
    data = cursor.fetchall()
    
    conn.commit()
    cursor.close()
    
    return render_template('staff_view.html', data = data, airline_name = airline_name)

@app.route('/home/staff/search', methods=['GET', 'POST'])
def staff_search():
    airline_name = session['agent_airline']
    return render_template('staff_search.html', airline_name = airline_name)

@app.route('/home/staff/searchandsee', methods=['GET', 'POST'])
def staff_search_flight():
    airline_name = session['agent_airline']
    
    departure_city = request.form['source_city']
    arrival_city = request.form['destination_city']
    from_date = request.form['from_date']
    to_date = request.form['to_date']
    
    cursor = conn.cursor()
    query = 'SELECT * FROM flight_information WHERE airline_name = %s AND departure_city = %s AND arrival_city = %s AND date(departure_time) >= %s AND date(departure_time) <= %s'
    cursor.execute(query, (airline_name, departure_city, arrival_city, from_date, to_date))
    data = cursor.fetchall()
    
    conn.commit()
    cursor.close()
    
    return render_template('staff_search.html', airline_name = airline_name, data = data)

@app.route('/home/staff/search/seecustomers', methods=['GET', 'POST'])
def see_all_customers():
    airline_name = request.form['airline_name']
    flight_num = request.form['flight_num']
    
    cursor = conn.cursor()
    query = 'SELECT airline_name, flight_num, customer_email, COUNT(*) AS number_of_tickets FROM user_purchase_information WHERE airline_name = %s AND flight_num = %s GROUP BY airline_name, flight_num, customer_email'
    cursor.execute(query, (airline_name, flight_num))
    data = cursor.fetchall()
    
    conn.commit()
    cursor.close()
    
    return render_template('staff_see_customers.html', data = data)

@app.route('/home/staff/searchstatus', methods=['GET', 'POST'])
def staff_search_status():
    airline_name = session['agent_airline']
    flight_num = request.form['flight_number']
    
    cursor = conn.cursor()
    query = 'SELECT airline_name, flight_num, status FROM flight WHERE airline_name = %s AND flight_num = %s'
    cursor.execute(query, (airline_name, flight_num))
    status = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template('staff_search.html', airline_name = airline_name, status = status)
    
@app.route('/home/staff/update', methods=['GET', 'POST'])
def home_update():
    return render_template('update_home.html')

@app.route('/home/staff/update/flights', methods=['GET', 'POST'])
def create_flights_interface():
    airline_name = session['agent_airline']
    
    cursor = conn.cursor()
    query = 'SELECT * FROM flight_information WHERE airline_name = %s AND date(departure_time) >= current_date AND date(departure_time) <= date_add(current_date, interval 30 day) AND status = %s'
    cursor.execute(query, (airline_name, 'upcoming'))
    data = cursor.fetchall()
    
    conn.commit()
    cursor.close()
    
    return render_template('staff_create_flights.html', data = data, airline_name = airline_name)


app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)