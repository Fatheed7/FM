import json
from flask import (
    Flask, request, render_template,
    redirect, make_response, session, url_for,
    flash, jsonify
    )
import os
import pandas as pd
from collections import OrderedDict

if os.path.exists("env.py"):
    import env


from calculate_functions import *

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

data_list = []

@app.route('/')
def index():
    function_names = {
        'calculate_advanced_forward_attack':  ('Advanced Forward - Attack', 'afa'),
        'calculate_advanced_playmaker_attack':  ('Advanced Playmaker - Attack', 'apa'),
        'calculate_advanced_playmaker_support':  ('Advanced Playmaker - Support', 'aps'),
        'calculate_anchor_defend':  ('Anchor - Defend', 'ad'),
        'calculate_attacking_midfielder_attack':  ('Attacking Midfielder - Attack', 'ama'),
        'calculate_attacking_midfielder_support':  ('Attacking Midfielder - Support', 'ams'),
        'calculate_ball_playing_defender_cover':  ('Ball Playing Defender - Cover', 'bpdc'),
        'calculate_ball_playing_defender_defend':  ('Ball Playing Defender - Defend', 'bpdd'),
        'calculate_ball_playing_defender_stopper':  ('Ball Playing Defender - Stopper', 'bpds'),
        'calculate_ball_winning_midfielder_defend':  ('Ball Winning Midfielder - Defend', 'bwmd'),
        'calculate_ball_winning_midfielder_support':  ('Ball Winning Midfielder - Support', 'bwms'),
        'calculate_box_to_box_midfielder_support':  ('Box to Box Midfielder - Support', 'b2bs'),
        'calculate_carrilero_support':  ('Carrilero - Support', 'cars'),
        'calculate_central_defender_cover':  ('Central Defender - Cover', 'cdc'),
        'calculate_central_defender_defend':  ('Central Defender - Defend', 'cdd'),
        'calculate_central_defender_stopper':  ('Central Defender - Stopper', 'cds'),
        'calculate_central_midfielder_attack':  ('Central Midfielder - Attack', 'cma'),
        'calculate_central_midfielder_defend':  ('Central Midfielder - Defend', 'cmd'),
        'calculate_central_midfielder_support':  ('Central  Midfielder - Support', 'cms'),
        'calculate_complete_forward_attack':  ('Complete Forward - Attack', 'cfa'),
        'calculate_complete_forward_support':  ('Complete Forward - Support', 'cfs'),
        'calculate_complete_wing_back_attack':  ('Complete Wingback - Attack', 'cwba'),
        'calculate_complete_wing_back_support':  ('Complete Wingback - Support', 'cwbs'),
        'calculate_deep_lying_forward_attack':  ('Deep Lying Forward - Attack', 'dlfa'),
        'calculate_deep_lying_forward_support':  ('Deep Lying Forward - Support', 'dlfs'),
        'calculate_deep_lying_playmaker_defend':  ('Deep Lying Playmaker - Defend', 'dlpd'),
        'calculate_deep_lying_playmaker_support':  ('Deep Lying Playmaker - Support', 'dlps'),
        'calculate_defensive_midfielder_defend':  ('Defensive Midfielder - Defend', 'dmd'),
        'calculate_defensive_midfielder_support':  ('Defensive Midfielder - Support', 'dms'),
        'calculate_defensive_winger_defend':  ('Defensive Winger - Defend', 'dwd'),
        'calculate_defensive_winger_support':  ('Defense Winger - Support', 'dws'),
        'calculate_false_nine_support':  ('False Nine - Support', 'f9s'),
        'calculate_full_back_attack':  ('Fullback - Attack', 'fba'),
        'calculate_full_back_defend':  ('Fullback - Defend', 'fbd'),
        'calculate_full_back_support':  ('Fullback - Support', 'fbs'),
        'calculate_goalkeeper_defend':  ('GK - Defend', 'gkd'),
        'calculate_half_back_defend':  ('Half Back - Defend', 'hbd'),
        'calculate_inverted_full_back_defend':  ('Inverted Fullback - Defend', 'ifbd'),
        'calculate_inverted_winger_attack':  ('Inverted Winger - Attack', 'iwa'),
        'calculate_inverted_winger_support':  ('Inverted Winger - Support', 'iws'),
        'calculate_inverted_wing_back_attack':  ('Inverted Wingback - Attack', 'iwba'),
        'calculate_inverted_wing_back_defend':  ('Inverted Wingback - Defend', 'iwbd'),
        'calculate_inverted_wing_back_support':  ('Inverted Wingback - Support', 'iwbs'),
        'calculate_libero_defend':  ('Libero - Defend', 'ld'),
        'calculate_libero_support':  ('Libero - Support', 'ls'),
        'calculate_mezzala_attack':  ('Mezzala - Attack', 'meza'),
        'calculate_mezzala_support':  ('Mezzala - Support', 'mezs'),
        'calculate_nononsense_centre_back_cover':  ('No-Nonsense Centreback - Cover', 'ncbc'),
        'calculate_nononsense_centre_back_defend':  ('No-Nonsense Centreback - Defend', 'ncbd'),
        'calculate_nononsense_centre_back_stopper':  ('No-Nonsense Centreback - Stopper', 'ncbs'),
        'calculate_nononsense_full_back_defend':  ('No-Nonsense Fullback - Defend', 'nfbd'),
        'calculate_poacher_attack':  ('Poacher - Attack', 'pa'),
        'calculate_pressing_forward_attack':  ('Pressing Forward- Attack', 'pfa'),
        'calculate_pressing_forward_defend':  ('Pressing Forward - Defend', 'pfd'),
        'calculate_pressing_forward_support':  ('Pressing Forward - Support', 'pfs'),
        'calculate_raumdeuter_attack':  ('Raumdeuter - Attack', 'raua'),
        'calculate_regista_support':  ('Regista - Support', 'regs'),
        'calculate_roaming_playmaker_support':  ('Roaming Playmaker - Support', 'rps'),
        'calculate_segundo_volante_attack':  ('Segundo Volante - Attack', 'sva'),
        'calculate_segundo_volante_support':  ('Segundo Volante - Support', 'svs'),
        'calculate_shadow_striker_attack':  ('Shadow Striker - Attack', 'ssa'),
        'calculate_sweeper_keeper_attack':  ('Sweeper Keeper - Attack', 'ska'),
        'calculate_sweeper_keeper_defend':  ('Sweeper Keeper - Defend', 'skd'),
        'calculate_sweeper_keeper_support':  ('Sweeper Keeper - Support', 'sks'),
        'calculate_target_forward_attack':  ('Target Forward - Attack', 'tfa'),
        'calculate_target_forward_support':  ('Target Forward - Support', 'tfs'),
        'calculate_trequartista_attack':  ('Trequartista - Attack', 'trea'),
        'calculate_wide_centre_back_attack':  ('Wide Centreback - Attack', 'wcba'),
        'calculate_wide_centre_back_defend':  ('Wide Centreback - Defend', 'wcbd'),
        'calculate_wide_centre_back_support':  ('Wide Centreback - Support', 'wcbs'),
        'calculate_wide_midfielder_attack':  ('Wide Midfielder - Attack', 'wma'),
        'calculate_wide_midfielder_defend':  ('Wide Midfielder - Defend', 'wmd'),
        'calculate_wide_midfielder_support':  ('Wide Midfielder - Support', 'wms'),
        'calculate_wide_playmaker_attack':  ('Wide Playmaker - Attack', 'wpa'),
        'calculate_wide_playmaker_support':  ('Wide Playmaker - Support', 'wps'),
        'calculate_wide_target_forward_attack':  ('Wide Target Forward - Attack', 'wtfa'),
        'calculate_wide_target_forward_support':  ('Wide Target Forward - Support', 'wtfs'),
        'calculate_winger_attack':  ('Winger - Attack', 'wa'),
        'calculate_winger_support':  ('Winger - Support', 'ws'),
        'calculate_wing_back_attack':  ('Wingback - Attack', 'wba'),
        'calculate_wing_back_defend':  ('Wingback - Defend', 'wbd'),
        'calculate_wing_back_support':  ('Wingback - Support', 'wbs'),
    }
    selected_options = session.get('selected_options', [])
    return render_template('index.html',function_names=function_names, selected_options=selected_options)

@app.route('/get_data')
def get_data():
    json_data = json.dumps(data_list)

    response = make_response(json_data)
    response.headers['Content-Type'] = 'application/json'
    return response

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
                    calculate_speed_workrate_score  # Always include this function
                ]

                # Iterate over selected function names and dynamically add them to the list
                for option in selected_options:
                    try:
                        function_name = option
                        # Fetch the function by name and add it to the list
                        calculation_functions.append(getattr(__import__('calculate_functions'), function_name))
                    except AttributeError:
                        flash(f'Function not found: {function_name}', 'error')
                        return redirect(url_for('index'))

                # Read the uploaded HTML file using Pandas
                # This assumes the HTML file contains tables
                squad_rawdata_list = pd.read_html(file, header=0, encoding='utf-8')
                squad_rawdata = squad_rawdata_list[0]

                # Run the selected functions on the data
                for calculation_function in calculation_functions:
                    squad_rawdata = calculation_function(squad_rawdata)

                # Builds Squad Dataframe using only columns
                # that will be exported to HTML
                squad = squad_rawdata[[
                    'Inf', 'Name', 'Age', 'Club', 'Transfer Value', 'Wage',
                    'Nat', 'Position', 'Personality', 'Media Handling',
                    'Left Foot', 'Right Foot', 'Spd', 'Jum', 'Str', 'Work',
                    'Height'] + data_calc_values]

                ordered_data = (squad.fillna('')
                .to_dict(orient='records', into=OrderedDict))

                global data_list
                data_list = ordered_data
                
                print(data_list)

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


def generate_html(dataframe: pd.DataFrame):
    # Get the table HTML from the dataframe
    table_html = dataframe.to_html(table_id="table", index=False, na_rep='')

    # Construct the HTML with jQuery Data tables
    html = f"""
    <html>
    <header>
        <meta charset="utf-8">
        <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
        <title>Processed FM Data</title>
    </header>
    <body>
        <button id="downloadButton">Download HTML</button>
        {table_html}
        <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js"
            integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI="
            crossorigin="anonymous"></script>
        <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
        <script>
            $(document).ready(function () {{
                $('#table').DataTable({{
                    paging: false,
                    order: [[12, 'desc']],
                    // scrollY: 400,
                }});

                // Add click event listener to the download button
                document.getElementById('downloadButton').addEventListener('click', function () {{
                    // Create a Blob containing the HTML content
                    var blob = new Blob(['<!DOCTYPE html><html>' +
                    document.documentElement.outerHTML + '</html>'], {{ type: 'text/html' }});
                    // Create a temporary URL for the Blob
                    var url = URL.createObjectURL(blob);
                    // Create a download link and trigger a click event to download the file
                    var a = document.createElement('a');
                    a.href = url;
                    a.download = 'processed_data.html';
                    document.body.appendChild(a);
                    a.click();
                    // Clean up the temporary URL and remove the download link
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                }});
            }});
        </script>
    </body>
    </html>
    """
    # Return the HTML as bytes
    return html.encode('utf-8')



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
