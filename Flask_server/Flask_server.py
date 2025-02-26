from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from data_base import DataBase
from KeyboardParser import KeyboardParser
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # מאפשר לכל המקורות לגשת ל-API

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
    day = request.args.get("day")
    hour = request.args.get("hour")
    minute = request.args.get("minute")

    print(f'Received: {machine_name}, {year}, {month}, {day}, {hour}, {minute}')

    with DataBase() as data_base:
        data = data_base.retrieval_from_database(year=year, month=month, day=day, hour=hour, minute=minute, machine_name=machine_name)

    events = [{"machine_name":event[3],"date":event[2], "data":KeyboardParser(event[1]).format_as_text()} for event in data]
    return jsonify(events)

@app.route('/get_info', methods=['GET'])
def get_info():
    with DataBase() as data_base:
        data = data_base.get_machine_tracking_info()
    return jsonify(data)

@app.route('/delete_data', methods=['GET'])
def delete_data():
    """
    :return :
    """
    machine_name = request.args.get("computer_name_device_id")
    year = request.args.get("year")
    month = request.args.get("month")
    day = request.args.get("day")
    hour = request.args.get("hour")
    minute = request.args.get("minute")

    print(f'Received: {machine_name}, {year}, {month}, {day}, {hour}, {minute}')

    with DataBase() as data_base:
        data = data_base.delete_events_by_date(year=year, month=month, day=day, hour=hour, minute=minute, machine_name=machine_name)

    return jsonify(f"נמחקו {data} אירועים ")


# הפעלת השרת
if __name__ == '__main__':
    # הפעלת השרת במצב פיתוח
    app.run(debug=True)