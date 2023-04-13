from flask import Flask, session, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
import copy
import config
import translate
from fileManage import Script

app = Flask(__name__)
app.secret_key = config.id_generator()
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'ScriptEN')
app.config['HANGUL_FOLDER'] = os.path.join(os.getcwd(), 'ScriptKR')

os.makedirs('ScriptEN', exist_ok=True)
os.makedirs('ScriptKR', exist_ok=True)


@app.route('/')
def home():
	return render_template('index.html')


@app.route('/charRule', methods=['POST'])
def charRegister():
	if request.method == 'POST':
		# 캐릭터 추가인 경우
		if request.form.get('submit') == 'new':
			newChar = request.form['newChar']
			charList = translate.appendChar(newChar, "")

		# 파일 업로드에서 넘어온 경우
		else:
			file = request.files['scriptFile']
			filePath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))

			# If file is not empty
			# if script.filename == '':
			
			# Save file in local
			file.save(filePath)
			file = Script(filePath)
			session['file'] = filePath
	
			# Initialize character dictionary
			charList = translate.parseJson2Char(file)

	return render_template('ruleAppend.html', charList = charList)


@app.route('/translation', methods=['POST'])
def editResult():
	oscript = Script(session['file'])
	idList = oscript.idList
	if request.method == 'POST':
		charDict = request.form

		for orig, trans in charDict.items():
			translate.appendChar(orig, trans)
	
	kscript = copy.deepcopy(oscript)
	translate.getTranslation(kscript)
	return render_template('transResult.html', **locals())


if __name__ == '__main__':
	app.run(host="0.0.0.0", port="8000", debug=True)