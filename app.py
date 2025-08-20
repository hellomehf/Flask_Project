import json

from flask import Flask, render_template , request

from fun_tele import sendMessage
from product import products
from flask_mail import Mail , Message
from tabulate import tabulate


app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'vidlovergt123@gmail.com'
app.config['MAIL_PASSWORD'] = 'hegy zyrn bbvu fphn'  # Use App Password from Google
app.config['MAIL_DEFAULT_SENDER'] = 'vidlovergt123@gmail.com'

mail = Mail(app)

@app.route('/')
def index():  # put application's code here
    return render_template('index.html')
@app.route('/catelog')
def catelog():
    product = products
    return  render_template('catolog.html', products=product)
@app.route('/cart')
def cart():
    product = products
    return render_template('cart.html' ,products=product)
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')
@app.post('/confirm')
def confirm():
    # get data form input type in html from form checkout.html
    form = request.form
    name = form.get('name')
    email = form.get('email')
    phone = form.get('phone')
    house = form.get('house')
    street = form.get('street')
    area = form.get('area')
    cart_item_str = form.get('cart-item')
    cart_item = json.loads(cart_item_str)
    item_row =[]
    total = sum(float(item['price']) * float(item['qty']) for item in cart_item)
    for item in cart_item:
        item_row.append(
            [
                f"{item['title'][0:15]}...",
                "$"+item["price"],
                item["qty"],
            ]
        )

    # table
    table = tabulate(
        tabular_data=item_row,
        headers=['Product Name', 'Price', 'Qty'],
    )
    # html from for telegram bot
    chat_id = '@notify_test_for_fun'
    html = f"<strong>CustomerName: {name}</strong>\n"
    html += f"<strong>Phone: {phone}</strong>\n"
    html += f"<strong>Email: {email}</strong>\n"
    html += f"<strong>Address: No.{house} , St.{street} , Area : {area}</strong>\n"
    html += f"<strong>-----------------------------</strong>\n"
    html += f"<pre>{table}</pre>\n"

    # call function for send message to tele
    sendMessage(
        chat_id=chat_id,
        message=html,
    )

    # send mail to customer
    msg = Message('Invoice From SU4.13 Shop', recipients=[email])
    msg.body = 'This is a plain text email sent from Flask.'
    message = render_template('invoice.html',
                              cart_item=cart_item,
                              customer_name=name,
                              email=email,
                              house=house,
                              area=area,
                              street=street,
                              total=total)

    msg.html = message
    mail.send(msg)

    return render_template('confirm_order.html')
@app.get('/product/<int:id>')
def product_details(id):
    product = next((p for p in products if p['id'] == id),None)
    return render_template('product_detail.html' , products=product)
@app.get('/shop')
def shop():
    return 'this is a shop'
if __name__ == '__main__':
    app.run()
