from flask import Flask, flash, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
import config
import translate

app = Flask(__name__)
app.config['SECRET_KEY'] = config.flask_key
app.config['UPLOAD_FOLDER'] = '*/uploads'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/translated', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        # Check if the post request has a file
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        script = request.files["scriptFile"]
        
        # If file not uploaded
        if script.filename == '':
            flash("No file selected")
            return redirect(request.url)
        
        # Save file in local
        fname = secure_filename(script.filename)
        script.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))


        ttt = translate.getTranslation(script)
        return render_template('transResult.html', **locals())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8000", debug=True)