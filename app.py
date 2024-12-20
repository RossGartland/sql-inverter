from flask import Flask, request, render_template
import os
from insert_to_delete_processor import delete_processor
from delete_to_insert_processor import insert_processor


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_sql():
    # Get SQL from the text box
    sql_script = request.form['sql_input']
    conversion_type = request.form.get('conversion_type')  # Get the selected conversion type

    if not sql_script.strip():
        return "No SQL input provided", 400

    # Process the SQL content based on the selected conversion type
    if conversion_type == "delete_to_insert":
        output_script = insert_processor(sql_script)
    elif conversion_type == "insert_to_delete":
        output_script = delete_processor(sql_script)
    else:
        return "Invalid conversion type selected", 400

    # Return the processed script to the web page
    return render_template('index.html', sql_input=sql_script, sql_output=output_script, conversion_type=conversion_type)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)