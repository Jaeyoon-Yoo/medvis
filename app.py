from flask import Flask, request
from flask import render_template

import pandas as pd
import numpy as np
app = Flask(__name__)

table_01_all = pd.read_csv('tables/Record_Table.csv')
table_02_ID_now = pd.read_csv('tables/Patients_ID_now.csv')
table_03_Cate_now = pd.read_csv('tables/Main_category_now.csv')


@app.route('/')
def hello_world():
    return render_template('main_page.html')

@app.route('/patient_page')
def patient_page():
    args = request.args
    
    ID = args['ID']
    return render_template('patient_page.html',ID=ID)
    

@app.route('/get_main_table')
def get_main_table():
    print(table_02_ID_now)
    print(table_03_Cate_now)
    return {'IDs': list(table_02_ID_now['subject_id'].astype('str').values), 
            'Categories': list(table_03_Cate_now['category'].astype('str').values)}

@app.route('/main_table_card')
def make_main_table_card():
    args = request.args
    ID = args['ID']
    Cate = args['Cate']
    outputs = get_filtered_values_card(ID,Cate)
    return {"value":outputs['val']}
    
def get_filtered_values_card(ID,Cate):
    val_selected = table_01_all[(table_01_all['subject_id'] == int(ID)) & (table_01_all['category'] == Cate)].sort_values('starttime', ascending=False)['starttime'].values
    if len(val_selected) == 0:
        return {'val': ['-','-']}
    elif len(val_selected) == 1:
        return {'val': [str(val_selected[0]), '-']}
    else:
        return {'val': [str(val_selected[0]), str(val_selected[1])]}
    
@app.route('/get_categories')
def get_categories():
    args = request.args
    if 'ID' in args.keys():
        ID = args['ID']
    else:
        ID = False
    return {'Categories': list(get_data({'ID': ID})['category'].unique().astype(str))}

@app.route('/get_filtered_data')
def get_filtered_data():
    args = request.args
    if 'ID' in args.keys():
        ID = args['ID']
    else:
        ID = False
    if 'Cate' in args.keys():
        Cate = args['Cate']
    else:
        Cate = False
    output = get_data({'ID': ID, 'Cate': Cate})
    return {'Date': list(output['starttime'].astype(str)),
            'Value': list(output['value'].astype(str)),
            'Label': list(output['label'].astype(str)),
            'CategoryName': list(output['ordercategoryname'].astype(str)),   
            'Idx': list(map(str,range(len(output))))}
        
        
def get_data(args):
    if 'ID' in args.keys():
        ID = args['ID']
    else:
        ID = False
    if 'Cate' in args.keys():
        Cate = args['Cate']
    else:
        Cate = False
    val_selected = table_01_all.copy()
    if ID:
        val_selected = val_selected[val_selected['subject_id'] == int(ID)]
    if Cate:
        val_selected = val_selected[val_selected['category'] == Cate]
    return val_selected