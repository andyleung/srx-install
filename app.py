#!/usr/bin/python

from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from jnpr.junos import Device 
from jnpr.junos.utils.sw import SW 
import os

UPLOAD_FOLDER = '/Users/andy/programs/flask/swinstall/images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','tgz','docx','xlsx'])

app.secret_key = "juniper"

@app.route('/')
@app.route('/add_device', methods=['GET','POST'])
def add_device():
  if request.method == 'POST':
    versions = []
    kk = request.form
    gg = frozenset(kk.items())
    read_frozen = dict(gg)
    print 'read_frozen: ', read_frozen
    list_len=len(read_frozen)/3
    hostname = read_frozen['hostname']
    username = read_frozen['username']
    password = read_frozen['password']
    mytuple = (hostname, username, password)
    global update_list
    update_list = []
    update_list.append(mytuple)
    print 'update_list: ', update_list
    #devices = connect_hosts(hostname,username,password)
    print 'hostname: ', hostname, username, password
    if list_len > 2:
         for i in range(1, list_len):
             hostname = read_frozen['hostname'+str(i)]
             username = read_frozen['username'+str(i)]
             password = read_frozen['password'+str(i)]
             mytuple = (hostname, username, password)
             update_list.append(mytuple)
    versions = connect_hosts(update_list)
    print 'update_list: ', update_list
    print "versions: ", versions
    return render_template('list_device.html', length=len(update_list), update_list=update_list, versions=versions)
  else:
    return render_template('add_device.html')

def connect_hosts(update_list):
      num_of_hosts = len(update_list)
      sw_version = []
      print "Num of hosts: ", num_of_hosts
      for i in range(num_of_hosts):
              hostname = update_list[i][0] 
              usr = update_list[i][1]
              psswd = update_list[i][2]
              print "Host name: ", hostname, usr, psswd
              dev = Device(hostname,user=usr,password=psswd)
              dev.open()
              sw_version.insert(i, dev.facts['version'])
              dev.close()
      return sw_version

@app.route('/upgrade_os', methods=['POST'])
def upgrade_os():
      upgrade_host = request.form.getlist('upgrade_srx')
      reboot_list = request.form.getlist('optradio')
      file = request.files['file']
      filename = secure_filename(file.filename)
      print "Upgrade hosts are: ", upgrade_host
      print "Reboot options are: ", reboot_list
      print "Upgrade image: ", filename
      print "update_list", update_list
      for i in upgrade_host:
           for j in update_list:
               if i in j:
                    hostname = j[0]
                    usr = j[1]
                    psswd = j[2]
                    dev = Device(hostname, user=usr, password=psswd)
                    dev.open()
                    dev.bind(sw=SW)
                    upgrade_file = "images/"+filename
                    flash(dev.sw.install(package = upgrade_file, progress = my_progress))
      return render_template('/add_device.html')

def my_progress(dev, msg):
      print "{}:{}".format(dev.hostname, msg)

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        # Get the name of the uploaded file
        file = request.files['file']
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
            #
            # return redirect(url_for('uploaded_file', filename=filename))
            return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
	app.run(
           host='0.0.0.0',
           port=5000,
           debug=True)
