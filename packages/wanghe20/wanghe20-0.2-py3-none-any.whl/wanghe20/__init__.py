from flask import Flask,render_template,request, \
    make_response, redirect, url_for,session, flash
from werkzeug.utils import secure_filename    
from flask_admin import Admin
import os,sys

app = Flask(__name__)
app.secret_key = 'wanghe20'
app.config['UPLOAD_FOLDER'] = 'upload/'


from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import UpdateDeviceVersionClass, session

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='wanghe20', template_mode='bootstrap3')
admin.add_view(ModelView(UpdateDeviceVersionClass, session))



from flask.views import View

class Uploadmy(View):
    def dispatch_request(self):
        return render_template('upload.html')
app.add_url_rule('/upload2',  view_func=Uploadmy.as_view('show_upload'))


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader',methods=['GET','POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        print(request.files)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

        return 'file uploaded successfully'

    else:

        return render_template('upload.html')


@app.route("/flash")
def handle_flash():
    flash('用户名/密码错误！',category='error')
    return render_template("login.html")

@app.route("/errpage")
def handle_error():
    return redirect("/",code='303')



@app.route('/setsession')
def set_session():
    session['username'] = 'admin'
    session['age'] = '20'
    return "设置session"


@app.route("/getsession")
def get_session():
    return "设置的session是：" + session['username'] + "age:" + session['age']



@app.route('/')
def hello_world():
    resp = make_response("wanghe20")
    resp.set_cookie("name", "luzg", max_age=3600)
    return resp


@app.route("/get")
def get_cookie():
    cookie_1 = request.cookies.get("name")  # 获取名字为Itcast_1对应cookie的值
    return cookie_1

@app.route("/delete")
def delete_cookie():
    resp = make_response("del success")
    resp.delete_cookie("luzg")

    return resp


@app.route('/hello2')
def hello2():
    name = request.args['name']
    return "hello," + name
 

@app.route('/hello3')
def hello3():
    return "I am hello 3"

@app.route('/hello4')
def hello4():

    a = 10
    b = 20
    s = "wanghe20"
    my_list = [1, 5, 4, 3, 2]
    my_dict = {
        'name': 'durant',
        'age': 28
    }    
    return render_template("hello.html",
                            a=a,
                            b=b,
                            s=s,
                            my_list=my_list,
                            my_dict=my_dict
    )

@app.route('/login',methods = ['POST', 'GET','HEAD', 'PUT', "DELETE", "OPTIONS"])
def login():
    if request.method == 'POST':
        print(1)
        user = request.form['nm']
        return "you name is " + user
    elif request.method == 'GET':
        return render_template("login.html") 
    elif request.method == 'HEAD':
        return "HEAD"
    elif request.method == 'PUT':
        return "PUT"
    elif request.method == 'DELETE':
        return "DELETE"
    elif request.method == 'OPTIONS':
        return "options"

def run_server():
    import sys
    print(sys.argv)

    app.debug = sys.argv[2]
    app.run(host=sys.argv[1]) 

if __name__ == '__main__':
    import sys
    print(sys.argv)
    # run_server(sys.argv[3], sys.argv[4])