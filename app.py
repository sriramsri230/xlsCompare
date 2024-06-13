from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['xls', 'xlsx']


def compare_excel_files(file1, file2):
    try:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
    except Exception as e:
        return [], str(e)

    matches = df1[df1.apply(tuple, 1).isin(df2.apply(tuple, 1))]

    return matches.to_dict(orient='records'), None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    if 'file1' not in request.files or 'file2' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))

    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == '' or file2.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
        flash('Invalid file type. Only .xls and .xlsx files are allowed.')
        return redirect(url_for('index'))

    matches, error = compare_excel_files(file1, file2)

    if error:
        flash(f'Error processing files: {error}')
        return redirect(url_for('index'))

    return render_template('result.html', matches=matches)


if __name__ == '__main__':
    app.run(debug=True,port=4999)
