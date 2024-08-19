from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import os
from zipfile import ZipFile
import sqlite3

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'your_secret_key'  # Add a secret key for security reasons

# Create a SQLite database and a table for texts
conn_text = sqlite3.connect('text_data.db')
cursor_text = conn_text.cursor()
cursor_text.execute('''
    CREATE TABLE IF NOT EXISTS texts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT
    )
''')
conn_text.commit()
conn_text.close()


@app.route('/')
def index():
    # Retrieve all texts from the database
    conn_text = sqlite3.connect('text_data.db')
    cursor_text = conn_text.cursor()
    cursor_text.execute('SELECT * FROM texts')
    texts = [{'id': text[0], 'content': text[1]} for text in cursor_text.fetchall()]
    conn_text.close()

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', texts=texts, filenames=files)


@app.route('/api/saveText', methods=['POST'])
def save_text():
    data = request.get_json()
    text_content = data.get('content')

    # Save text to the database
    conn_text = sqlite3.connect('text_data.db')
    cursor_text = conn_text.cursor()
    cursor_text.execute('INSERT INTO texts (content) VALUES (?)', (text_content,))
    conn_text.commit()
    conn_text.close()

    return jsonify({'message': 'Text saved successfully'})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/getText')
def get_text():
    # Retrieve all texts from the database
    conn_text = sqlite3.connect('text_data.db')
    cursor_text = conn_text.cursor()
    cursor_text.execute('SELECT * FROM texts')
    texts = [{'id': text[0], 'content': text[1]} for text in cursor_text.fetchall()]
    conn_text.close()

    return jsonify({'texts': texts})


@app.route('/api/updateText', methods=['POST'])
def update_text():
    data = request.get_json()
    text_id = data.get('id')
    new_content = data.get('content')

    # Update text in the database
    conn_text = sqlite3.connect('text_data.db')
    cursor_text = conn_text.cursor()
    cursor_text.execute('UPDATE texts SET content = ? WHERE id = ?', (new_content, text_id))
    conn_text.commit()
    conn_text.close()

    return jsonify({'message': 'Text updated successfully'})


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))

    return "Invalid file type"


@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('index'))


@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)


@app.route('/download_all')
def download_all_files():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if
             os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    zip_filename = 'all_files.zip'
    with ZipFile(zip_filename, 'w') as zip:
        for file in files:
            zip.write(os.path.join(app.config['UPLOAD_FOLDER'], file), file)
    return send_file(zip_filename, as_attachment=True)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import os
from zipfile import ZipFile
import sqlite3

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'your_secret_key'  # Add a secret key for security reasons

# Create a SQLite database and a table for texts
conn_text = sqlite3.connect('text_data.db')
cursor_text = conn_text.cursor()
cursor_text.execute('''
    CREATE TABLE IF NOT EXISTS texts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT
    )
''')
conn_text.commit()
conn_text.close()


@app.route('/')
def index():
    # Retrieve all texts from the database
    conn_text = sqlite3.connect('text_data.db')
    cursor_text = conn_text.cursor()
    cursor_text.execute('SELECT * FROM texts')
    texts = [{'id': text[0], 'content': text[1]} for text in cursor_text.fetchall()]
    conn_text.close()

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', texts=texts, filenames=files)


@app.route('/api/saveText', methods=['POST'])
def save_text():
    data = request.get_json()
    text_content = data.get('content')

    # Save text to the database
    conn_text = sqlite3.connect('text_data.db')
    cursor_text = conn_text.cursor()
    cursor_text.execute('INSERT INTO texts (content) VALUES (?)', (text_content,))
    conn_text.commit()
    conn_text.close()

    return jsonify({'message': 'Text saved successfully'})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/getText')
def get_text():
    # Retrieve all texts from the database
    conn_text = sqlite3.connect('text_data.db')
    cursor_text = conn_text.cursor()
    cursor_text.execute('SELECT * FROM texts')
    texts = [{'id': text[0], 'content': text[1]} for text in cursor_text.fetchall()]
    conn_text.close()

    return jsonify({'texts': texts})


@app.route('/api/updateText', methods=['POST'])
def update_text():
    data = request.get_json()
    text_id = data.get('id')
    new_content = data.get('content')

    # Update text in the database
    conn_text = sqlite3.connect('text_data.db')
    cursor_text = conn_text.cursor()
    cursor_text.execute('UPDATE texts SET content = ? WHERE id = ?', (new_content, text_id))
    conn_text.commit()
    conn_text.close()

    return jsonify({'message': 'Text updated successfully'})


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))

    return "Invalid file type"


@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('index'))


@app.route('/download/<filename>')
def download_file(filename):
    try:
        # Ensure the filename is secure
        filename = secure_filename(filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Make sure the path is absolute
        absolute_file_path = os.path.abspath(file_path)

        if os.path.exists(absolute_file_path):
            return send_file(absolute_file_path, as_attachment=True)
        else:
            return "File not found"
    except Exception as e:
        return str(e)


@app.route('/download_all')
def download_all_files():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if
             os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    zip_filename = 'all_files.zip'
    with ZipFile(zip_filename, 'w') as zip:
        for file in files:
            zip.write(os.path.join(app.config['UPLOAD_FOLDER'], file), file)
    return send_file(zip_filename, as_attachment=True)


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)
