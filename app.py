from flask import Flask, flash, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
import config
import translate

app = Flask(__name__)
app.config['SECRET_KEY'] = config.flask_key
app.config['UPLOAD_FOLDER'] = '*/Scripts/orig'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/charRule', methods=['GET', 'POST'])
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
        print("File saved successfully")

        # result<라는 딕셔너리를 받아서 넘겨주어야 함!!
        print(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        result = translate.parseJson2Char(os.path.join(app.config['UPLOAD_FOLDER'], fname))

        #ttt = translate.getTranslation(script)
        return render_template('ruleAppend.html', **locals())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8000", debug=True)