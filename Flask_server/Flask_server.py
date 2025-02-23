from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from data_base import DataBase
from KeyboardParser import KeyboardParser


app = Flask(__name__)

# תיקיית זמנית לקבצים
UPLOAD_FOLDER = 'temp_uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# יצירת תיקיית העלאה אם היא לא קיימת
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # בדיקה האם הבקשה מכילה קובץ
    if 'file' not in request.files:
        return jsonify({'error': 'לא נמצא קובץ'}), 400

    file = request.files['file']
    machine_name = request.form.get("computer_name_device_id")

    if file.filename == '': # בדיקה האם הקובץ ריק
        return jsonify({'error': 'שם הקובץ ריק'}), 400
    elif not file.filename.endswith('.txt'): # בדיקה שזה קובץ TXT
        return jsonify({'error': 'רק קבצי TXT מותרים'}), 400

    # שמירת הקובץ בצורה בטוחה
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # קריאת תוכן הקובץ
    with DataBase() as data_base:
        data_base.read_file_and_import(file_path, machine_name)

    # מחיקת הקובץ הזמני
    os.remove(file_path)

    return jsonify("הקןבץ התקבל בהצלחה") #jsonify(response)


@app.route('/get_data', methods=['GET'])
def get_data():

    machine_name = request.args.get("computer_name_device_id")
    year = request.args.get("year")
    month = request.args.get("month")

    print(f'Received: machine_name={machine_name}, year={year}, month={month}')

    with DataBase() as data_base:
        text_input = data_base.retrieval_from_database(machine_name=machine_name,year=year,month=month)

    # data = KeyboardParser().parse_text_input(text_input)

    return jsonify(text_input)


# הפעלת השרת
if __name__ == '__main__':
    # הפעלת השרת במצב פיתוח
    app.run(debug=True)
# from flask import Flask, request, jsonify
# import os
# from werkzeug.utils import secure_filename
# from data_base import DataBase
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from flask_cors import CORS
#
# app = Flask(__name__)
# CORS(app)  # לאפשר בקשות מה-Front-End
#
# # הגדרת סודיות ל-JWT
# app.config['JWT_SECRET_KEY'] = 'my_secret_key'
# jwt = JWTManager(app)
#
# UPLOAD_FOLDER = 'temp_uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
#
# # סימולציה של מסד נתונים למשתמשים (צריך להחליף למסד אמיתי)
# USERS = {
#     "admin": "1234",  # סיסמה לדוגמה
#     "user": "password"
# }
#
# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')
#
#     if username in USERS and USERS[username] == password:
#         token = create_access_token(identity=username)
#         return jsonify({'token': token})
#
#     return jsonify({'error': 'שם משתמש או סיסמה לא נכונים'}), 401
#
#
# @app.route('/data', methods=['GET'])
# @jwt_required()
# def get_data():
#     current_user = get_jwt_identity()
#
#     with DataBase() as db:
#         data = db.get_user_data(current_user)  # פונקציה שמחזירה נתונים מהמסד
#
#     return jsonify(data)
#
#
# @app.route('/upload', methods=['POST'])
# @jwt_required()
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'לא נמצא קובץ'}), 400
#
#     file = request.files['file']
#     machine_name = request.form.get("computer_name_device_id")
#
#     if file.filename == '':
#         return jsonify({'error': 'שם הקובץ ריק'}), 400
#     elif not file.filename.endswith('.txt'):
#         return jsonify({'error': 'רק קבצי TXT מותרים'}), 400
#
#     filename = secure_filename(file.filename)
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     file.save(file_path)
#
#     with DataBase() as data_base:
#         data_base.read_file_and_import(file_path, machine_name)
#
#     os.remove(file_path)
#
#     return jsonify("הקןבץ התקבל בהצלחה")
#
# if __name__ == '__main__':
#     app.run(debug=True)
#
