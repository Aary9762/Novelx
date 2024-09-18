from flask import Flask, request, redirect, url_for, render_template
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db_config = {
    'user': 'root',
    'password': 'dmpab409@',
    'host': 'localhost',
    'database': 'novel_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM novels")
    novels = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', novels=novels)

@app.route('/novel/<int:novel_id>')
def view_novel(novel_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM novels WHERE id = %s", (novel_id,))
    novel = cursor.fetchone()
    cursor.execute("SELECT * FROM chapters WHERE novel_id = %s", (novel_id,))
    chapters = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_novel.html', novel=novel, chapters=chapters)

@app.route('/create_novel', methods=['GET', 'POST'])
def create_novel():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO novels (title, description) VALUES (%s, %s)", (title, description))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create_novel.html')

@app.route('/add_chapter/<int:novel_id>', methods=['GET', 'POST'])
def add_chapter(novel_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chapters (novel_id, title, content) VALUES (%s, %s, %s)", (novel_id, title, content))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('view_novel', novel_id=novel_id))
    return render_template('add_chapter.html', novel_id=novel_id)

@app.route('/delete_novel/<int:novel_id>', methods=['POST'])
def delete_novel(novel_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chapters WHERE novel_id = %s", (novel_id,))
    cursor.execute("DELETE FROM novels WHERE id = %s", (novel_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM novels WHERE title LIKE %s", ('%' + query + '%',))
    novels = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', novels=novels)

if __name__ == '__main__':
    app.run(debug=True)
