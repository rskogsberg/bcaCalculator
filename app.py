import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
from compute import BcaCalculator, GoldenToad
from model import InputForm
#from werkzeug import secure_filename
import os

# Application object
app = Flask(__name__)

# Relative path of directory for uploaded files
UPLOAD_DIR = 'S:/Departments/Analytics/Chemical Analytics/Richard/tempUploadFolder'

app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
app.secret_key = 'MySecretKey'

if not os.path.isdir(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)

# Allowed file types for file upload
ALLOWED_EXTENSIONS = set(['txt'])

def allowed_file(filename):
    """Does filename have the right extension?"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Path to the web application
@app.route('/')
def upload_form():
	return render_template('index.html')

@app.route('/', methods=['GET','POST'])
def upload_file():
    form = InputForm(request.form)
    filename = None  # default
    if request.method == 'POST':
        # Save uploaded file on server if it exists and is valid
        if request.files:
            file = request.files[form.filename.name]
            if file and allowed_file(file.filename):
                # Make a valid version of filename for any file ystem
                #filename = secure_filename(file.filename)
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                       filename))  
            elif file and not allowed_file(file.filename):
                flash('Only txt files are accepted!')
                return redirect(request.url)
            elif file not in request.files:
                flash('Please include a file for upload!')
                return redirect(request.url)
        standardResults = None
        sampleResults = None
        if request.form.get('goldenToad') == 'on':
            runType = GoldenToad(filename)
            standardResults = runType.fillStandardsDataframe().to_html(index=False, classes='table')
            sampleResults = runType.fillSamplesDataframe().to_html(index=False, classes='table')
        elif request.form.get('notGoldenToad') == 'on':
            runType = BcaCalculator(filename)
            standardResults = runType.fillStandardsDataframe().to_html(index=False, classes='table')
            sampleResults = runType.fillSamplesDataframe().to_html(index=False, classes='table')
    return render_template('index.html', tables=[standardResults, sampleResults], form=form, standardResults=standardResults, sampleResults=sampleResults)

if __name__ == '__main__':
    app.run(debug=True)