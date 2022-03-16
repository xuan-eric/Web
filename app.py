from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

DEBUG = True

app = Flask(__name__)

app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dream1024'
app.config['MYSQL_DB'] = 'pythonlogin'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def login01():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            msg = '用戶名或密碼錯誤！'
    return render_template('login.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'sex' in request.form and 'phone' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        sex = request.form['sex']
        phone = request.form['phone']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = '帳戶已存在!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = '無效的郵件地址！'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = '用戶名只能包含字符和數字！'
        elif not re.match(r'[A-Za-z0-9]+', phone):
            msg = '用戶名只能包含字符和數字！'
        elif not re.match(r'[A-Za-z0-9]+', sex):
            msg = '用戶名只能包含字符和數字！'
        elif not username or not password or not email or not sex or not phone:
            msg = '請填寫表格！'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute(
                'INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s)', (username, password, email, sex, phone))
            mysql.connection.commit()
            msg = '您已經成功註冊了！'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = '請填寫表格！'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/aboutus')
def aboutus():
    return render_template('about-us.html')


@app.route('/pubfac')
def pubfac():
    return render_template('public facilities.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/opinion')
def opinion():
    return render_template('opinion.html')


@app.route('/singlepost')
def singlepost():
    return render_template('single-post.html')


@app.route('/repair')
def repair():
    return render_template('repair.html')


@app.route('/account')
def account():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s',
                       (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('account.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/communication')
def communication():
    return render_template('resident communication.html')


# 下方測試


@app.route('/dbtest')
def dbtest():
    sql_cmd = """
        select *
        from user
        """

    query_data = db.engine.execute(sql_cmd)
    print(query_data)
    return 'ok'


@app.route('/xuan')
def xuan():
    return render_template('xuan.html')


@app.route('/font')
def fontawesome():
    return render_template('mytest/fontawesome.html')


@app.route('/index')
def mytestindex():
    return render_template('mytest/index.html')


@app.route('/static')
def myteststatic_test():
    return render_template('mytest/static_test.html')


# @app.route('/login')
# def mytestlogin():
#     return render_template('mytest/login.html')


@app.route('/user/<username>')
def mytestuser(username):
    return render_template('mytest/user.html', name=username)


@app.route('/if')
def mytestif_test():
    rad1 = random.randint(1, 3)
    return render_template('mytest/if_test.html', number=rad1)


@app.route('/for')
def mytestfor_test():
    show = [{'name': '林漢瑄', 'birth': '0228'},
            {'name': 'Eric Lin', 'birth': '0000'}]
    return render_template('mytest/for_test.html', **locals())


def mytestdo_index_class(index):
    if index % 3 == 0:
        return 'line'
    else:
        return ''


app.add_template_filter(mytestdo_index_class, 'index_class')


@app.route('/base_index')
def mytestbase_index():
    return render_template('mytest/base_index.html')


@app.route('/product')
def mytestproduct():
    return render_template('mytest/product.html')


@app.route('/testindex')
def testindex():
    return render_template('mytest/testindex.html')


if __name__ == '__main__':
    app.run(debug=True)
