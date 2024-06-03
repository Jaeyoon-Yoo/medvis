from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load data
table_01_all = pd.read_csv('tables/Record_Table.csv')
table_02_ID_now = pd.read_csv('tables/Patients_ID_now.csv')
table_03_Cate_now = pd.read_csv('tables/Main_category_now.csv')
urine_input = pd.read_csv('tables/urine_input.csv')
urine_output = pd.read_csv('tables/urine_output.csv')

@app.route('/')
def hello_world():
    patient_ids = list(table_02_ID_now['subject_id'].astype(str).values)
    return render_template('main_page.html', patient_ids=patient_ids, selected_id="")

@app.route('/patient_page')
def patient_page():
    args = request.args
    ID = args.get('ID')
    patient_ids = list(table_02_ID_now['subject_id'].astype(str).values)
    return render_template('patient_page.html', ID=ID, patient_ids=patient_ids, selected_id=ID)

@app.route('/get_main_table')
def get_main_table():
    return jsonify({
        'IDs': list(table_02_ID_now['subject_id'].astype('str').values),
        'Categories': list(table_03_Cate_now['category'].astype('str').values)
    })

@app.route('/main_table_card')
def make_main_table_card():
    args = request.args
    ID = args.get('ID')
    Cate = args.get('Cate')
    outputs = get_filtered_values_card(ID, Cate)
    return jsonify({'value': outputs['val']})

def get_filtered_values_card(ID, Cate):
    val_selected = table_01_all[(table_01_all['subject_id'] == int(ID)) & (table_01_all['category'] == Cate)].sort_values('starttime', ascending=False)['starttime'].values
    if len(val_selected) == 0:
        return {'val': ['-', '-']}
    elif len(val_selected) == 1:
        return {'val': [str(val_selected[0]), '-']}
    else:
        return {'val': [str(val_selected[0]), str(val_selected[1])]}

@app.route('/get_categories')
def get_categories():
    args = request.args
    ID = args.get('ID', False)
    return jsonify({'Categories': list(get_data({'ID': ID})['category'].unique().astype(str))})

@app.route('/get_filtered_data')
def get_filtered_data():
    args = request.args
    ID = args.get('ID', False)
    Cate = args.get('Cate', False)
    output = get_data({'ID': ID, 'Cate': Cate})
    return jsonify({
        'Date': list(output['starttime'].astype(str)),
        'Value': list(output['value'].astype(str)),
        'Label': list(output['label'].astype(str)),
        'CategoryName': list(output['ordercategoryname'].astype(str)),
        'Idx': list(map(str, range(len(output))))
    })

def get_data(args):
    ID = args.get('ID', False)
    Cate = args.get('Cate', False)
    val_selected = table_01_all.copy()
    if ID:
        val_selected = val_selected[val_selected['subject_id'] == int(ID)]
    if Cate:
        val_selected = val_selected[val_selected['category'] == Cate]
    return val_selected

@app.route('/get_urine_data')
def get_urine_data():
    args = request.args
    ID = args.get('ID', False)
    if ID:
        output_data = urine_output[urine_output['subject_id'] == int(ID)]
        output_data = output_data[['charttime', 'value']]
        output_data = output_data.sort_values('charttime')
        
        return jsonify({
            'time': list(output_data['charttime'].astype(str)),
            'values': list(output_data['value'])
        })
    else:
        return jsonify({'time': [], 'values': []})


@app.route('/get_urine_input_data')
def get_urine_input_data():
    args = request.args
    ID = args.get('ID', False)
    if ID:
        input_data = urine_input[urine_input['subject_id'] == int(ID)]
        input_data = input_data[['starttime', 'endtime', 'amount']]
        return jsonify(input_data.to_dict(orient='records'))
    else:
        return jsonify([])

@app.route('/urine_page')
def urine_page():
    args = request.args
    ID = args.get('ID')
    patient_ids = list(table_02_ID_now['subject_id'].astype(str).values)
    return render_template('urine_page.html', ID=ID, patient_ids=patient_ids, selected_id=ID)

if __name__ == '__main__':
    app.run(debug=True)
