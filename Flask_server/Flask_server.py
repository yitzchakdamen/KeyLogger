from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from data_base import DataBase


app = Flask(__name__)

# תיקיית זמנית לקבצים
UPLOAD_FOLDER = 'temp_uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# יצירת תיקיית העלאה אם היא לא קיימת
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/upload', methods=['POST'])
def upload_file():
    # בדיקה האם הבקשה מכילה קובץ
    if 'file' not in request.files:
        return jsonify({'error': 'לא נמצא קובץ'}), 400

    file = request.files['file']

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
        data_base.read_file_and_import(file_path)

    # שליחת הנתונים לקלומר
    # response = send_to_kolmer(content)

    # מחיקת הקובץ הזמני
    os.remove(file_path)

    return jsonify("הקןבץ התקבל בהצלחה") #jsonify(response)


# פונקציה ששולחת את הנתונים לשרת קלומר
def send_to_kolmer(content):
    import requests  # ספרייה לשליחת בקשות לשרתים אחרים

    # כתובת השרת של קלומר
    kolmer_url = 'YOUR_KOLMER_API_ENDPOINT'

    # הגדרת כותרות לבקשה
    # כמו לכתוב כתובת על מעטפה
    headers = {'Content-Type': 'application/json'}

    # הכנת הנתונים לשליחה
    # כמו להכין מעטפה עם המכתב
    data = {
        'content': content,  # תוכן הקובץ שקיבלנו
        'source': 'txt_upload'  # מקור הנתונים
    }

    try:
        # שליחת הבקשה לקלומר
        response = requests.post(kolmer_url,
                                 json=data,
                                 headers=headers,
                                 timeout=30)  # נקבע זמן מועד לבקשה

        # בדיקה האם הבקשה הצליחה
        if response.status_code == 200:
            # הכל הצליח, מחזירים הודעת הצלחה
            return {'status': 'success', 'message': 'הנתונים נשלחו בהצלחה'}
        else:
            # הייתה שגיאה, מחזירים הודעת שגיאה
            return {'status': 'error',
                    'message': f'שגיאה בשליחה לקלומר: {response.text}'}

    except Exception as e:
        # אם יש שגיאה כללית (כמו בעיה בחיבור לאינטרנט)
        return {'status': 'error',
                'message': f'שגיאה בשליחה לקלומר: {str(e)}'}


# הפעלת השרת
if __name__ == '__main__':
    # הפעלת השרת במצב פיתוח
    app.run(debug=True)
