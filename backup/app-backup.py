#!/usr/bin/python

from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
from jnpr.junos import Device 
from jnpr.junos.utils.sw import SW 
import os


UPLOAD_FOLDER = '/Users/andy/programs/flask/swinstall/images'
ALLOWED_EXTENSIONS = set(['txt','tgz','ova','jpg','docx','xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# app.secret_key = "juniper"
# connection_string = "mongodb://localhost"
# connection = pymongo.MongoClient(connection_string)
# database = connection.srx
# collection_name = 'software'

upgrade_list =[]


# @app.route('/')
# def home():
# 	return render_template('add_device.html')

# @app.route('/')
# @app.route('/add_device', methods=['GET','POST'])
# def add_device():
#   if request.method == 'POST':
#     versions = []
#     update_list = []
#     kk = request.form
#     gg = frozenset(kk.items())
#     read_frozen = dict(gg)
#     print 'read_frozen: ', read_frozen
#     list_len=len(read_frozen)/3
#     hostname = read_frozen['hostname']
#     username = read_frozen['username']
#     password = read_frozen['password']
#     mytuple = (hostname, username, password)
#     update_list.append(mytuple)
#     print 'update_list: ', update_list
#     #devices = connect_hosts(hostname,username,password)
#     print 'hostname: ', hostname, username, password
#     if list_len > 2:
#          for i in range(1, list_len):
#              hostname = read_frozen['hostname'+str(i)]
#              username = read_frozen['username'+str(i)]
#              password = read_frozen['password'+str(i)]
#              mytuple = (hostname, username, password)
#              update_list.append(mytuple)
#     versions = connect_hosts(update_list)
#     print 'update_list: ', update_list
#     print "versions: ", versions
#     return render_template('list_device.html', length=len(update_list), update_list=update_list, versions=versions)
#   else:
#     return render_template('add_device.html')

# def connect_hosts(update_list):
#       num_of_hosts = len(update_list)
#       sw_version = []
#       print "Num of hosts: ", num_of_hosts
#       for i in range(num_of_hosts):
#               hostname = update_list[i][0] 
#               usr = update_list[i][1]
#               psswd = update_list[i][2]
#               print "Host name: ", hostname, usr, psswd
#               dev = Device(hostname,user=usr,password=psswd)
#               dev.open()
#               sw_version.insert(i, dev.facts['version'])
#               dev.close()
#       return sw_version

# @app.route('/upgrade_os', methods=['POST'])
# def upgrade_os():
#        upgrade_host = request.form.getlist('upgrade_srx')
#        reboot_list = request.form.getlist('optradio')
#        print "Upgrade hosts are: ", upgrade_host
#        print "Reboot options are: ", reboot_list 
#        return render_template('/add_device.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
	app.run(
           host='0.0.0.0',
           port=5000,
           debug=True)
