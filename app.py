from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load data
table_02_ID_now = pd.read_csv('tables/Patients_ID_now.csv')
table_discharge = pd.read_csv('tables/discharge.csv', dtype = str).set_index('subject_id').dropna()
urine_input = pd.read_csv('tables/urine_input.csv')
urine_output = pd.read_csv('tables/urine_output.csv')

@app.route('/')
def hello_world():
    patient_ids = list(table_02_ID_now['subject_id'].astype(str).values)
    return render_template('patient_page.html', patient_ids=patient_ids, selected_id="")

@app.route('/patient_page')
def patient_page():
    args = request.args
    ID = args.get('ID')
    patient_ids = list(table_02_ID_now['subject_id'].astype(str).values)
    return render_template('patient_page.html', ID=ID, patient_ids=patient_ids, selected_id=ID)

@app.route('/get_urine_data')
def get_urine_data():
    args = request.args
    ID = args.get('ID', False)
    if ID:
        input_data = urine_input[urine_input['subject_id'] == int(ID)]
        output_data = urine_output[urine_output['subject_id'] == int(ID)]
        
        input_data = input_data[['starttime', 'amount']].rename(columns={'starttime': 'time', 'amount': 'amount_input'})
        output_data = output_data[['charttime', 'value']].rename(columns={'charttime': 'time', 'value': 'amount_output'})
        
        data = pd.merge(input_data, output_data, on='time', how='outer').sort_values('time')
        data['time'] = pd.to_datetime(data['time'])
        data = data.fillna(0)
        
        return jsonify({
            'time': list(data['time'].astype(str)),
            'amount_input': list(data['amount_input']),
            'amount_output': list(data['amount_output'])
        })
    else:
        return jsonify({'time': [], 'amount_input': [], 'amount_output': []})

@app.route('/urine_page')
def urine_page():
    args = request.args
    ID = args.get('ID')
    patient_ids = list(table_02_ID_now['subject_id'].astype(str).values)
    return render_template('urine_page.html', ID=ID, patient_ids=patient_ids, selected_id=ID)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/get_discharge_data')
def get_discharge_data():
    args = request.args
    ID = args.get('ID', False)
    print(ID)
    if ID:
        data_ID = table_discharge.loc[ID]
               
        return jsonify({'date': [data_ID['charttime'][:10]],
                        'detail_1': [data_ID['text']],
                        'main_symptom': [i[i.find('.')+1:].strip() for i in data_ID['주호소'].split('\n')],
                        'main_disease': [i[i.find('.')+1:].strip() for i in data_ID['원인 질환'].split('\n')],
                        'other_disease': [i[i.find('.')+1:].strip() for i in data_ID['기저 질환'].split('\n')],
                        'treatment': [i[i.find('.')+1:].strip() for i in data_ID['주 처치 시술'].split('\n')],
                        'detail_history': [data_ID['detail history']]
                        })
    else:
        return jsonify({'date': [], 
                        'detail_1': [], 
                        'main_symptom': [], 
                        'main_disease': [], 
                        'other_disease': [], 
                        'treatment': [], 
                        'detail_history': []
                        })