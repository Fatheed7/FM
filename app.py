from flask import (
    Flask, request, render_template,
    redirect, make_response, session, url_for,
    flash, jsonify
    )
from function_names import function_names
import os
import pandas as pd

if os.path.exists("env.py"):
    import env


from calculate_functions import *

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

data_list = []


@app.route('/')
def index():
    selected_options = session.get('selected_options', [])
    return render_template(
        'index.html',
        function_names=function_names,
        selected_options=selected_options)


@app.route('/get_data')
def get_data():
    return jsonify(data_list)


@app.route('/clear_data')
def clear_data():
    data_list.clear()
    return jsonify({'message': 'Data list cleared successfully'})


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            flash('No file part.', 'error')
            return redirect(url_for('index'))

        file = request.files['file']

        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))

        if file:
            try:
                form_data = request.form.to_dict()

                selected_options = []
                data_calc_values = []

                for key, value in form_data.items():
                    data_calc_values.append(key)
                    selected_options.append(value)

                if not data_calc_values:
                    flash('At least one checkbox must be selected.', 'error')
                    return redirect(url_for('index'))

                # List containing selected functions to be run
                calculation_functions = [
                    calculate_speed_workrate_score
                ]

                # Iterate over selected function names
                # and dynamically add them to the list
                for option in selected_options:
                    try:
                        function_name = option
                        # Fetch the function by name and add it to the list
                        calculation_functions.append(
                            getattr(__import__(
                                'calculate_functions'), function_name))
                    except AttributeError:
                        flash(f'Function not found: {function_name}', 'error')
                        return redirect(url_for('index'))

                # Read the uploaded HTML file using Pandas
                # This assumes the HTML file contains tables
                squad_rawdata_list = pd.read_html(
                    file, header=0, encoding='utf-8')
                squad_rawdata = squad_rawdata_list[0]

                # Run the selected functions on the data
                for calculation_function in calculation_functions:
                    squad_rawdata = calculation_function(squad_rawdata)
                
                # Determine earning column
                if 'Wage' in squad_rawdata.columns:
                    earnings_column = 'Wage'
                elif 'Salary' in squad_rawdata.columns:
                    earnings_column = 'Salary'
                else:
                    earnings_column = None

                # Add 'Earnings' to your DataFrame
                if earnings_column:
                    squad_rawdata['Earnings'] = squad_rawdata[earnings_column]

                # Builds Squad Dataframe using only columns
                # that will be exported to HTML
                squad = squad_rawdata[[
                    'Inf', 'Name', 'Age', 'Club', 'Transfer Value',
                    'Nat', 'Position', 'Personality', 'Media Handling',
                    'Left Foot', 'Right Foot', 'Spd', 'Jum', 'Str', 'Work',
                    'Height'] + data_calc_values]
                
                if earnings_column:
                    squad.append('Earnings')

                global data_list
                data_list = squad.fillna('').to_dict(orient='records')

                session['selected_options'] = selected_options

                return redirect(url_for('index'))

            except ValueError as ve:
                return render_template("error.html", error=ve)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/<path:invalid_route>')
def invalid_route(invalid_route):
    # Route back to index page on invalid route
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
