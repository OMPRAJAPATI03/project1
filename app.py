from flask import Flask, render_template,request,url_for,session,redirect
import pymysql
from werkzeug.utils import secure_filename
from flask_session import Session
import os



app = Flask(__name__)
conn = pymysql.connect(host = 'localhost',user = 'root',password = '',db = 'db_jwellarys')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.session_cookie_name = 'my_custom_cookie_name'
Session(app)
import pymysql


UPLOAD_FOLDER='static/upload/'
@app.route('/dashboard')
def dashboard():
    # if 'admin_id' not in session:
    #     return redirect('adminlogin1')
    # cursor = conn.cursor()
    # query = "SELECT COUNT(category_id) FROM categorys"
    # cursor.execute(query)
    # account = cursor.fetchone()[0]
    # print(account)
    # query1="SELECT COUNT(user_id) FROM users"
    # cursor.execute(query1)
    # ac = cursor.fetchone()[0]
    # print(ac)
    # query2="SELECT COUNT(product_id) FROM products"
    # cursor.execute(query2)
    # acc = cursor.fetchone()[0]
    # print(acc)
    
    # query3="SELECT COUNT(order_id) FROM orders"
    # cursor.execute(query3)
    # acco = cursor.fetchone()[0]
    # print(acco)
    # cursor.close()
    # ,area=account,area1=ac,area2=acc,area3=acco
    return render_template("admin/dashboard.html")



@app.route('/admin')
def adminlogin():
    return render_template("admin/adminlogin.html")


@app.route('/Addcatagory')
def Addcatagory():
    return render_template("admin/Addcatagory.html")



@app.route('/Viewcatagory')
def Viewcatagory():
    cursor = conn.cursor()
    query = "SELECT * FROM categorys"
    cursor.execute(query)
    account = cursor.fetchall()
    print(account)
    cursor.close()
    return render_template("admin/Viewcatagory.html",area=account)

@app.route('/catagory_insert',methods=["POST"])
def catagory_insert():
    cursor = conn.cursor()

    category_name = request.form['category_name']
    description = request.form['description']

    query = "INSERT INTO categorys(category_name,description)VALUES(%s,%s)"

    val=(category_name,description)
    cursor.execute(query,val)
    conn.commit()
    cursor.close()

    return redirect(url_for('Addcatagory'))

@app.route('/addproduct')
def addproduct():
    cursor = conn.cursor()
    query = "SELECT * FROM categorys"
    cursor.execute(query)
    account= cursor.fetchall()
    cursor.close()
    return render_template("admin/addproduct.html",area=account)

@app.route('/product_insert',methods=['post'])
def product_insert():
    cursor = conn.cursor()


    category_id = request.form['category_id']
    product_name = request.form['product_name']
    description = request.form['description']
    weight = request.form['weight']
    price  = request.form['price']
    image   = request.files['image']
    filename=secure_filename(image.filename)
    image.save(os.path.join(UPLOAD_FOLDER,filename))
    path=os.path.join(UPLOAD_FOLDER,filename)
    status = request.form['status']
    
    

    query = "INSERT INTO products(category_id,product_name,description,weight,price,image,status)VALUES(%s,%s,%s,%s,%s,%s,%s)"

    val=(category_id,product_name,description,weight,price,path,status)
    cursor.execute(query,val)
    conn.commit()
    cursor.close()

    return redirect(url_for('addproduct'))

@app.route('/viewproduct')
def viewproduct():
    cursor = conn.cursor()
    query = "SELECT * FROM products"
    cursor.execute(query)
    account = cursor.fetchall()
    print(account)
    cursor.close()
    return render_template("admin/Viewproduct.html",area=account)

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    cursor = conn.cursor()
    try:
        query = "DELETE FROM products WHERE product_id=%s"
        val = (product_id)
        cursor.execute(query,val)
        conn.commit()
        #flash('product details deleted successfully!')
        return redirect(url_for('viewproduct'))
    finally:
        cursor.close()



@app.route('/admin/deletecategory/<int:category_id>')
def deletecategory(category_id):
    cursor = conn.cursor()
    try:
        query = "DELETE FROM categorys WHERE category_id=%s"
        val = (category_id)
        cursor.execute(query,val)
        conn.commit()
        #flash('product details deleted successfully!')
        return redirect(url_for('Viewcatagory'))
    finally:
        cursor.close()








@app.route('/admin/adminlogin1', methods=['POST'])
def adminlogin1():
    cursor = conn.cursor()
    
    admin_email = request.form['admin_email']
    admin_pass = request.form['admin_pass']
    query = "SELECT * FROM admin_logins WHERE  admin_email =%s AND password =%s"
    val = (admin_email,admin_pass)
    cursor.execute(query,val)
    account = cursor.fetchone()
    # cursor.close()

    if account:
        session['admin_id']=account[0]
        session['admin_email']=account[2]
        session['admin_name']=account[1]
        msg = 'login in successfully !'
        return redirect('/dashboard')
    else:
        msg='incorrect username/password !'
        return render_template('admin/adminlogin.html',msg=msg)
    
@app.route('/logout')
def logout():
    session.pop('admin_name',None)
    session.pop('admin_email',None)
    session.pop('admin_id',None)
    # session.pop('address',None)
    # session.pop('password',None)
    return redirect(url_for('adminlogin'))










@app.route('/')
def homepage():
    cursor = conn.cursor()
    query = "SELECT * FROM categorys"
    cursor.execute(query)
    account= cursor.fetchall()
    query1 = "SELECT * FROM products"
    cursor.execute(query1)
    acc= cursor.fetchall()
    cursor.close()
    return render_template("user/homepage.html",data=account,area=acc)

@app.route('/user')
def user_register():
    return render_template("user/user_register.html")

@app.route('/user_insert', methods=['POST'])
def user_insert():
    cursor = conn.cursor()
    
    user_name = request.form['user_name']
    user_email = request.form['user_email']
    mobile = request.form['mobile']
    address = request.form['address']
    password = request.form['password']

    query = "INSERT INTO users(user_name,user_email,mobile,address,password)VALUES(%s,%s,%s,%s,%s)"

    val=(user_name,user_email,mobile,address,password)
    cursor.execute(query,val)
    conn.commit()
    cursor.close()

    return redirect(url_for('user_register'))
    






@app.route('/login')
def userlogin():
    return render_template("user/user_login.html")


@app.route('/userlogin1', methods=['POST'])
def userlogin1():
    cursor = conn.cursor()
    user_email = request.form['user_email']
    password = request.form['password']
    query = "SELECT * FROm users WHERE  user_email =%s AND password =%s"
    val = (user_email,password)
    cursor.execute(query,val)
    account = cursor.fetchone()
    # cursor.close()

    if account:
        session['user_id']=account[0]
        session['user_email']=account[2]
        session['user_name']=account[1]
        msg = 'login in successfully !'
        # return render_template('user/homepage.html',msg=msg)
        return redirect(url_for('homepage'))
    else:
        msg='incorrect username/password !'
        # return render_template('user/user_login.html',msg=msg)
        return redirect(url_for('userlogin'))
    

@app.route('/userlogout')
def userlogout():
    session.pop('user_name',None)
    session.pop('user_email',None)
    session.pop('user_id',None)
    # session.pop('address',None)
    # session.pop('password',None)
    return redirect(url_for('userlogin'))





@app.route('/userviewproduct')
def userviewproduct1():
    cursor = conn.cursor()
    query = "SELECT * FROM products"
    cursor.execute(query)
    account = cursor.fetchall()
    cursor.close()
    return render_template("user/userviewproduct.html")


@app.route('/userviewproduct/<int:category_id>')
def userviewproduct(category_id):
    cursor = conn.cursor()
    query = "SELECT * FROM products WHERE category_id = %s"
    cursor.execute(query, (category_id,))
    account = cursor.fetchall()

    val=(category_id,)
    cursor.execute(query,val)
    account = cursor.fetchall()

    query1 = "SELECT * FROM categorys"
    # val=(category_id,)
    cursor.execute(query1)
    ac=cursor.fetchall()
    cursor.close()
    return render_template("user/userViewproduct.html",area=account,data=ac)

    

@app.route('/productdetails/<int:product_id>')
def productdetails(product_id):
    cursor = conn.cursor()
    query = "SELECT * FROM products where product_id=%s"
    val=(product_id,)
    cursor.execute(query,val)
    account = cursor.fetchall()
    cursor.close()
    return render_template("user/productdetails.html",area=account)



@app.route('/addcart/<int:product_id>')
def addcart(product_id):
    cursor = conn.cursor()
    qty = 1
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/userlogin')

    query = "INSERT INTO carts (user_id, product_id, qty) VALUES (%s, %s, %s)"
    cursor.execute(query, (user_id, product_id, qty))
    conn.commit()
    cursor.close()
    return redirect('/cart')


@app.route('/cart')
def viewcart():
    user_id = session.get('user_id')

    if user_id is None:
        return redirect('/userlogin')

    cursor = conn.cursor()
    query = """
        SELECT a.cart_id, a.user_id, a.product_id, a.qty,
               b.product_id, b.product_name, b.price, b.image
        FROM carts AS a 
        JOIN products AS b ON a.product_id = b.product_id
        WHERE a.user_id = %s
    """
    cursor.execute(query, (user_id,))
    cart_items = cursor.fetchall()
    cursor.close()

    # qty index = 3
    # price index = 6
    subtotal = sum(int(item[3]) * float(item[6]) for item in cart_items)

    return render_template('user/viewcart.html', cart=cart_items, subtotal=subtotal)


@app.route('/deletecart/<int:cart_id>')
def delete_cart(cart_id):
    cursor = conn.cursor()
    query = "DELETE FROM carts WHERE cart_id = %s"
    cursor.execute(query, (cart_id,))
    conn.commit()
    cursor.close()
    return redirect('/cart')
                           
@app.route('/update_qty/<int:cart_id>/<string:action>')
def update_qty(cart_id, action):
    cursor = conn.cursor()

    # First get current qty
    cursor.execute("SELECT qty FROM carts WHERE cart_id = %s", (cart_id,))
    data = cursor.fetchone()

    if not data:
        cursor.close()
        return redirect('/cart')

    qty = int(data[0])

    # Increase OR decrease
    if action == "plus":
        qty += 1
    elif action == "minus" and qty > 1:
        qty -= 1

    # Update in DB
    cursor.execute("UPDATE carts SET qty = %s WHERE cart_id = %s", (qty, cart_id))
    conn.commit()
    cursor.close()

    return redirect('/cart')




  
    
@app.route('/checkout', methods=['POST'])
def checkout():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/userlogin')

    cursor = conn.cursor()
    name = request.form['name']
    contact = request.form['contact']
    email = request.form['email']
    country = request.form['country']
    state = request.form['state']
    zipcode = request.form['zipcode']
    address = request.form['address']
    payment_type = request.form['payment_type']
    print(payment_type)
    amount = request.form['amount']
    upinumber = request.form['upinumber']
    bankname = request.form['bankname']
    accountnumber = request.form['accountnumber']


    # Cart ma je che e badhu fetch
    cursor.execute("SELECT product_id, qty FROM carts WHERE user_id=%s", (user_id,))
    cart_items = cursor.fetchall()

    if not cart_items:
        cursor.close()
        return redirect('/cart')
    
    cursor.execute("SELECT UUID()")
    order_number = cursor.fetchone()[0]


    # Orders table ma insert
    for product_id, qty in cart_items:
       cursor.execute("""
    INSERT INTO `orders` 
    (order_number, user_id, product_id, qty, order_status, order_date)
    VALUES (UUID(), %s, %s, %s, 'Pending', NOW())
    """, (user_id, product_id, qty))
    #order_id = cursor.lastrowid

    

    cursor = conn.cursor()

  
    cursor.execute("""
        INSERT INTO order_detail 
        (order_number, name, contact_no, email, country, state, zipcode, address,pyment_type,total_amount,upi_id,bank_name,account_number)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (order_number, name, contact, email, country, state, zipcode, address,payment_type,amount,upinumber,bankname,accountnumber))

    # Clear cart
    cursor.execute("DELETE FROM carts WHERE user_id=%s", (user_id,))

    # Cart saaf
    cursor.execute("DELETE FROM carts WHERE user_id=%s", (user_id,))
    conn.commit()
    cursor.close()
    

    return redirect('/')


@app.route('/vieworder')
def vieworder():
    cursor = conn.cursor()
    query = "select a.*,b.* from orders as a join users as b where a.user_id = b.user_id and a.user_id  GROUP BY order_number"
    
    cursor.execute(query)
    account = cursor.fetchall()
    cursor.close()
    return render_template("admin/vieworder.html", area=account)

@app.route('/order_success')
def order_success():
    if 'user_id' not in session:
        return redirect('/userlogin')

    user_id = session['user_id']     
    cursor = conn.cursor()    
    query = """
        SELECT 
    o.order_id,
    o.order_number,
    o.product_id,
    o.qty,
    o.order_status,
    o.order_date,
    u.user_name AS user_name,
    u.user_email
	FROM orders o
	JOIN users u 
    ON o.user_id = u.user_id
    WHERE o.user_id = %s
    ORDER BY o.order_id DESC;

    """

    cursor.execute(query,(user_id,))
    account = cursor.fetchall()

    cursor.close()
    

    return render_template('user/order_success.html', area=account)



if __name__=="__main__":
    app.run(debug=True)