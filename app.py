from flask import Flask, session, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename
import os
import copy
import config
import scriptDict
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


@app.route('/ruleAppend', methods=['POST'])
def charRegister():
	if request.method == 'POST':
		# 단어 추가인 경우
		if request.form.get('submit') == 'new':
			newWord = request.form['newWord']
			scriptDict.appendWord(newWord, "")

		# 파일 업로드에서 넘어온 경우
		else:
			file = request.files['scriptFile']
			fname = secure_filename(file.filename)
			session['fname'] = fname
			filePath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))

			# If file is not empty
			# if script.filename == '':
			
			# Save file in local
			file.save(filePath)
			file = Script(filePath)
	
			# Initialize character dictionary
			scriptDict.parseJson2Char(file)

		charList = scriptDict.characters()

	return render_template('charAppend.html', charList = charList)


@app.route('/charAppend', methods=['POST'])
def charRegister():
	if request.method == 'POST':
		# 캐릭터 추가인 경우
		if request.form.get('submit') == 'new':
			newChar = request.form['newChar']
			scriptDict.appendChar(newChar, "")

		# 파일 업로드에서 넘어온 경우
		else:
			file = request.files['scriptFile']
			fname = secure_filename(file.filename)
			session['fname'] = fname
			filePath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))

			# If file is not empty
			# if script.filename == '':
			
			# Save file in local
			file.save(filePath)
			file = Script(filePath)
	
			# Initialize character dictionary
			scriptDict.parseJson2Char(file)

		charList = scriptDict.characters()

	return render_template('charAppend.html', charList = charList)


@app.route('/translation', methods=['POST'])
def editResult():
	if request.method == 'POST':
		file = os.path.join(app.config['UPLOAD_FOLDER'], session['fname'])
		oscript = Script(file)
		idList = oscript.idList

		# 파일 내보내기 버튼을 누른 경우
		if request.form.get('submit') == 'export':
			scriptFile = os.path.join(app.config['HANGUL_FOLDER'], session['fname'])
			return send_file(scriptFile, as_attachment=True)

		# save 버튼을 누른 경우
		elif request.form.get('submit') == 'save':
			pass
		
		# 캐릭터 등록에서 넘어온 경우
		else:
			charDict = request.form

			# # 사용자가 입력한 캐릭터들을 캐릭터 용어집에 등록
			# for orig, trans in charDict.items():
			# 	translate.appendChar(orig, trans)

			# for char in charList:
			# 	scriptDict.appendChar(char, charDict[char])
			# 	scriptDict.setTone(char, charDict[char+'_features'])

			for char in scriptDict.characters():
				name = char.original
				scriptDict.updateChar(name, charDict[name], "", charDict[name+'_features'])

			# 번역한 정보는 원본 oscript를 수정하지 않고 kscript에 따로 기록
			kscript = copy.deepcopy(oscript)

			# Translate script
			translate.getTranslation(kscript)

			# Export translated script to local
			outpath = os.path.join(app.config['HANGUL_FOLDER'], session['fname'])
			kscript.export(outpath)

	return render_template('transResult.html', **locals())


if __name__ == '__main__':
	app.run(host="0.0.0.0", port="8000", debug=True)