from flask import Flask, flash, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
import config
import translate

app = Flask(__name__)
app.config['SECRET_KEY'] = config.FLASK_KEY
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'ScriptEN')

os.makedirs('ScriptEN', exist_ok=True)


@app.route('/')
def home():
	return render_template('index.html')


@app.route('/charRule', methods=['POST'])
def charRegister():
	if request.method == 'POST':
		script = request.files['scriptFile']

		# If file is not empty
		# if script.filename == '':
		
		# Save file in local
		fname = secure_filename(script.filename)
		script.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
	
	# result<라는 딕셔너리를 받아서 넘겨주어야 함!!
	result = translate.parseJson2Char(os.path.join(app.config['UPLOAD_FOLDER'], fname))

	#ttt = translate.getTranslation(script)
	return render_template('ruleAppend.html', **locals())


if __name__ == '__main__':
	app.run(host="0.0.0.0", port="8000", debug=True)