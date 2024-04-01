from flask import Flask, request, jsonify, render_template_string, url_for
import os
import sqlite3
import concurrent.futures
import json


app = Flask(__name__)


#### DATABASE PROCESSING#####

# Function to process all db files in a folder
def get_dbs(folder_path):
    db_list = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".db"):
            file_path = os.path.join(folder_path, file_name)
            db_list.append(file_path)
    return db_list

# Function to create a database connection
def get_db_connection(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

# Function to execute a query on a database
def execute_query_on_db(db_name, query):
    sql_query = "SELECT * FROM data WHERE email LIKE ?"
    
    results = {}
    try:
        conn = get_db_connection(db_name)
        cursor = conn.execute(sql_query, ('%' + query + '%',))
        #cursor = conn.execute(sql_query, query)
        #cursor = conn.execute(query)
        results[db_name] = [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        results[db_name] = {'error': str(e)}
    finally:
        conn.close()
    return results


#### HTML PROCESSING ####

def generate_html_results(data):
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="ISO 8859-15">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Breached</title>
        <style>
            body {{
                margin: 0;
                margin-top: 10px;
                padding: 0;
                padding-top: 10;
                margin-bot: 10px;
                padding-bop: 10;
                font-family: Arial, sans-serif;
                background: #007bff;
                height: 100vh;
                display: flex;
                justify-content: center;
            }}
            
            table {{
                border: 10;
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-collapse: collapse;
                width: 100%;
                margin: 20 auto;
                margin-top: 30px;
                padding-top: 20%;
            }}
            
            th, td {{
                padding: 10px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            
            th {{
                background-color: #007bff;
                color: white;
            }}
        </style>
    </head>
    <body>
    <div class="logo">
        <table>
            <thead></thead>
            <tbody>
            </tbody>
        </table>
    </div>

    <div class="tables">
    <table>
    '''
    for key, value in data.items():
        for v in value:
            html += '''
            <table>
            <tbody>
            '''
            for i,j in v.items():
                if i != "id":
                    html += f'<tr><td>{i}</td><td>{j}</td></tr>'
            html += '''
            </tbody>
            </table>
            '''
    html += '''
    </div>
    </body>
    </html>
    '''
    return html

# Route to display the query form
@app.route('/')
def query_form():
    return render_template_string('''
                                  
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="ISO 8859-15">
<meta name="viewport" content="width=device-width, initial-scale=2.0">
<title>Breached</title>
<style>
    body {
        margin: 0;
        padding: 0;
        font-family: Arial, sans-serif;
        background: linear-gradient(to bottom right, #007bff, #1a8cff);
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .form-container {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    
    .form-container input[type="text"] {
        width: 100%;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        box-sizing: border-box;
    }
    
    .form-container input[type="submit"] {
        width: 100%;
        padding: 10px;
        border: none;
        border-radius: 5px;
        background-color: #007bff;
        color: #fff;
        cursor: pointer;
    }
    
    .form-container input[type="submit"]:hover {
        background-color: #0056b3;
    }
</style>
</head>
                                  
<body>
    <div class="form-container">
        <form action="/query" method="get">
            <input type="text" id="query" name="q" placeholder="Enter an email" required>
            <input type="submit" value="Submit">
        </form>
    </div>
</body>
</html>

    ''')

# Load Browser Favorite Icon
@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='image/favicon.ico')

# Route to execute SELECT queries on multiple databases concurrently
@app.route('/query', methods=['GET'])
def execute_query():
    db_names = get_dbs(".")
    query = request.args.get('q', None)
    
    if query is None:
        return jsonify({'error': 'Query must be provided.'}), 400
    print (query)
    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_db = {executor.submit(execute_query_on_db, db_name, query): db_name for db_name in db_names}
        for future in concurrent.futures.as_completed(future_to_db):
            db_name = future_to_db[future]
            try:
                result = future.result()
                results.update(result)
            except Exception as e:
                results[db_name] = {'error': str(e)}

    return generate_html_results(results)

if __name__ == '__main__':
    app.run(debug=True)
