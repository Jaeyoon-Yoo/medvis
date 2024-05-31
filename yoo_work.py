from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)
table_discharge = pd.read_csv('tables/discharge.csv').set_index('subject_id') 

@app.route('/get_discharge_data')
def get_discharge_data():
    args = request.args
    ID = args.get('ID', False)
    if ID:
        data_ID = table_discharge.loc[ID]
        
        input_data = input_data[['starttime', 'amount']].rename(columns={'starttime': 'time', 'amount': 'amount_input'})
        output_data = output_data[['charttime', 'value']].rename(columns={'charttime': 'time', 'value': 'amount_output'})
        
        data = pd.merge(input_data, output_data, on='time', how='outer').sort_values('time')
        data['time'] = pd.to_datetime(data['time'])
        data = data.fillna(0)
        
        return jsonify({'date': data_ID['charttime'][:10],
                        'detail_1': data_ID['text'],
                        'main_symptom': [i[i.find('.')+1:].strip() for i in data_ID['주호소'].split('\n')],
                        'main_disease': [i[i.find('.')+1:].strip() for i in data_ID['원인 질환'].split('\n')],
                        'other_disease': [i[i.find('.')+1:].strip() for i in data_ID['기저 질환'].split('\n')],
                        'treatment': [i[i.find('.')+1:].strip() for i in data_ID['주 처치 시술'].split('\n')],
                        'detail_history': data_ID['detail history']
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
