# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 16:26:46 2023

@author: danie
"""

# Import modules
from dash import Dash, html, dcc, Input, Output, dash_table
from dash.dependencies import State
import pandas as pd
import pysftp
import io
import base64
import psycopg2
import dash_auth
from datetime import datetime

# App
app = Dash(__name__)

# # Keep this out of source code repository - save in a file or a database
# VALID_USERNAME_PASSWORD_PAIRS = { 'Admin': 'corporateactions' }

# # Credentials
# auth = dash_auth.BasicAuth(
#                             app,
#                             VALID_USERNAME_PASSWORD_PAIRS
#                             )

# App
dict_ca = {"Dividends":["Corporate Action Status",
                        "If modification id",
                        "Corporate Action Date",
                        "Scope Affected",
                        "Identification",
                        "Corporate Action Effective Date",
                        "Corporate Action Receipt Date",
                        "Document",
                        "Dividend Announcement Date",
                        "Dividend Record Date",
                        "Dividend Ex Date",
                        "Dividend Payment Date",
                        "Dividend Gross",
                        "Dividend Net",
                        "How is the Dividend payed?"],
            "Investment Manager":["Corporate Action Status",
                                  "If modification id",
                                  "Corporate Action Date",
                                  "Scope Affected",
                                  "Identification",
                                  "Corporate Action Effective Date",
                                  "Document",
                                  "Portfolio Manager Name",
                                  "Portfolio Manager Role Starting Date"],
            "Management Company":["Corporate Action Status",
                                  "If modification id",
                                  "Corporate Action Date",
                                  "Scope Affected",
                                  "Identification",
                                  "Corporate Action Effective Date",
                                  "Document",
                                  "ManCo",
                                  "Domicile Of ManCo",
                                  "Email address of the ManCo"],
            "Split and Reverse Split":["Corporate Action Status",
                                       "If modification id",
                                       "Corporate Action Date",
                                       "Scope Affected",
                                       "Identification",
                                       "Corporate Action Effective Date",
                                       "Document",
                                       "Split Ratio",
                                       "Reverse Split"],
            "Advisor":["Corporate Action Status",
                       "If modification id",
                       "Corporate Action Date",
                       "Scope Affected",
                       "Identification",
                       "Corporate Action Effective Date",
                       "Document",
                       "Fund Advisor Name",
                       "Sub Investment Advisor Name"],
            "Admin Custodian Transfer Agent":["Corporate Action Status",
                                              "If modification id",
                                              "Corporate Action Date",
                                              "Scope Affected",
                                              "Identification",
                                              "Corporate Action Effective Date",
                                              "Document",
                                              "Fund Administrator Name",
                                              "Custodian Bank Name",
                                              "Depositary Bank Name",
                                              "Depositary Bank LEI",
                                              "Transfer Agent Name",
                                              "LEI of Custodian"],
            "Auditor":["Corporate Action Status",
                       "If modification id",
                       "Corporate Action Date",
                       "Scope Affected",
                       "Identification",
                       "Corporate Action Effective Date",
                       "Document",
                       "Auditor Name"],
            "SICAV Static and Sub Fund Statics":["Corporate Action Status",
                                                 "If modification id",
                                                 "Corporate Action Date",
                                                 "Scope Affected",
                                                 "Identification",
                                                 "Corporate Action Effective Date",
                                                 "Document",
                                                 "Umbrella",
                                                 "Domicile of Umbrella",
                                                 "Legal Fund Name Including Umbrella",
                                                 "Legal Fund Name Only",
                                                 "Fund Launch Date",
                                                 "Full Share Class Name",
                                                 "Abbreviated Share Class Name"],
            "NAV Publications Incidents":["Corporate Action Status",
                                          "If modification id",
                                          "Corporate Action Date",
                                          "Scope Affected",
                                          "Identification",
                                          "Corporate Action Effective Date",
                                          "Document"],
            "Investment Status":["Corporate Action Status",
                                 "If modification id",
                                 "Corporate Action Date",
                                 "Scope Affected",
                                 "Identification",
                                 "Corporate Action Effective Date",
                                 "Document",
                                 "Share Class Lifecycle",
                                 "Dormant Start Date",
                                 "Dormant End Date",
                                 "Liquidation Start Date",
                                 "Termination Date",
                                 "Investment Status"],
            "Min Investment Amount or Min Holdings":["Corporate Action Status",
                                                     "If modification id",
                                                     "Corporate Action Date",
                                                     "Scope Affected",
                                                     "Identification",
                                                     "Corporate Action Effective Date",
                                                     "Document",
                                                     "Min Initial Subscription in Shares",
                                                     "Min Initial Subscription in Amount",
                                                     "Currency of Min Subscription",
                                                     "Min Subsequent Subscription in Shares",
                                                     "Min Subsequent Subscription in Amount",
                                                     "Min Redepmtion Category",
                                                     "Min Initial Redepmtion in Shares",
                                                     "Min Initial Redepmtion in Amount",
                                                     "Currency of Minimum Redemption",
                                                     "Standard Min Remaing Amount",
                                                     "Currency of Min Remaining Amount"],
            "Fees":["Corporate Action Status",
                    "If modification id",
                    "Corporate Action Date",
                    "Scope Affected",
                    "Identification",
                    "Corporate Action Effective Date",
                    "Document",
                    "Performance Fee Applied",
                    "Custodian Fee Applied",
                    "Depositary Fee Applied",
                    "Applied Subscription Fee In Favour of Fund",
                    "Applied Subscription Fee In Favour of Distributor",
                    "Applied Redepmtion Fee in Favour of Distributor",
                    "Applied Redepmtion Fee in Favour of Fund",
                    "Management Fee Applied",
                    "All in Fee Applied",
                    "Distribution Fee",
                    "Ongoing Charges",
                    "Servicing Fees"],
            "Subscription Redemption Notice Periods":["Corporate Action Status",
                                                      "If modification id",
                                                      "Corporate Action Date",
                                                      "Scope Affected",
                                                      "Identification",
                                                      "Corporate Action Effective Date",
                                                      "Document",
                                                      "Redemption Notice Period"],
            "Settlement Data":["Corporate Action Status",
                               "If modification id",
                               "Corporate Action Date",
                               "Scope Affected",
                               "Identification",
                               "Corporate Action Effective Date",
                               "Document",
                               "Fund Valuation Point",
                               "Valuation Frequency",
                               "Max Number of Possible Decimals Shares",
                               "Max Number of Possible Decimals Amounts",
                               "Max Number of Possible Decimals NAV",
                               "Cut off time for Subscription",
                               "Cut off time",
                               "Calendar or business days for transactions",
                               "Settlement Period for Subscription",
                               "Settlement Period for Redemption",
                               "Non Dealing Days"],
            "General Meeting":["Corporate Action Status",
                               "If modification id",
                               "Corporate Action Date",
                               "Scope Affected",
                               "Identification",
                               "Corporate Action Effective Date",
                               "Document",
                               "General Meeting Ponts",
                               "General Meeting Date"],
            "Mergers":["Corporate Action Status",
                       "If modification id",
                       "Corporate Action Date",
                       "Scope Affected",
                       "Identification",
                       "Corporate Action Effective Date",
                       "Document",
                       "Sub Fund Merge Absorved",
                       "Sub Fund Merge Absorbing",
                       "Company Merge Absorved",
                       "Company Name Absorbing",
                       "Merger Tax Exempt",
                       "ISIN Merger Fund Absorbing",
                       "ISIN Merged Fund Absorved",
                       "Last Trade Date Absorbing Fund",
                       "Last Trade Date Absorbed Fund"],
            "Guarantor":["Corporate Action Status",
                         "If modification id",
                         "Corporate Action Date",
                         "Scope Affected",
                         "Identification",
                         "Corporate Action Effective Date",
                         "Document",
                         "Fund Guarantor",
                         "Guarantor Rating Review"],
            "Investment Policy":["Corporate Action Status",
                                 "If modification id",
                                 "Corporate Action Date",
                                 "Scope Affected",
                                 "Identification",
                                 "Corporate Action Effective Date",
                                 "Document",
                                 "Investment Objective",
                                 "Max Leverage in Fund",
                                 "Is Fund Targeting Environmental or Social Objectives (EOS]",
                                 "Swap Counterparty Name",
                                 "Benchmark",
                                 "Investment Policy"],
            "Other Corporate Actions":["Corporate Action Status",
                                       "If modification id",
                                       "Corporate Action Date",
                                       "Scope Affected",
                                       "Identification",
                                       "Corporate Action Effective Date",
                                       "Document",
                                       "Other Corporate Actions"],
            "Taxation and Register":["Corporate Action Status",
                                     "If modification id",
                                     "Corporate Action Date",
                                     "Scope Affected",
                                     "Identification",
                                     "Corporate Action Effective Date",
                                     "Document",
                                     "Is Eligible for tax deferred Fund switch in Spain",
                                     "Number of Shareholders",
                                     "PEA Plan dEpargne in actions",
                                     "Other Tax Figures",
                                     "NAV disclosed channel"]}

dict_ca_types= {"Corporate Action Status":"text",
                "If modification id":"numeric",
                "Corporate Action Date":"datetime",
                "Scope Affected":"text",
                "Identification":"text",
                "Corporate Action Effective Date":"datetime",
                "Corporate Action Receipt Date":"datetime",
                "Document":"text",
                "Dividend Announcement Date":"datetime",
                "Dividend Record Date":"datetime",
                "Dividend Ex Date":"datetime",
                "Dividend Payment Date":"datetime",
                "Dividend Gross":"numeric",
                "Dividend Net":"numeric",
                "How is the Dividend payed?":"text",
                "Portfolio Manager Name":"text",
                "Portfolio Manager Role Starting Date":"datetime",
                "ManCo":"text",
                "Domicile Of ManCo":"text",
                "Email address of the ManCo":"text",
                "Split Ratio":"numeric",
                "Reverse Split":"numeric",
                "Fund Advisor Name":"text",
                "Sub Investment Advisor Name":"text",
                "Fund Administrator Name":"text",
                "Custodian Bank Name":"text",
                "Depositary Bank Name":"text",
                "Depositary Bank LEI":"text",
                "Transfer Agent Name":"text",
                "LEI of Custodian":"text",
                "Auditor Name":"text",
                "Umbrella":"text",
                "Domicile of Umbrella":"text",
                "Legal Fund Name Including Umbrella":"text",
                "Legal Fund Name Only":"text",
                "Fund Launch Date":"datetime",
                "Full Share Class Name":"text",
                "Abbreviated Share Class Name":"text",
                "Share Class Lifecycle":"text",
                "Dormant Start Date":"datetime",
                "Dormant End Date":"datetime",
                "Liquidation Start Date":"datetime",
                "Termination Date":"datetime",
                "Investment Status":"text",
                "Min Initial Subscription in Shares":"numeric",
                "Min Initial Subscription in Amount":"numeric",
                "Currency of Min Subscription":"text",
                "Min Subsequent Subscription in Shares":"numeric",
                "Min Subsequent Subscription in Amount":"numeric",
                "Min Redepmtion Category":"text",
                "Min Initial Redepmtion in Shares":"numeric",
                "Min Initial Redepmtion in Amount":"numeric",
                "Currency of Minimum Redemption":"text",
                "Standard Min Remaing Amount":"numeric"}

dict_div_rename = {"Corporate Action Status":"ficad00000",
                   "If modification id":"fica000007",
                   "Corporate Action Date":"ficad00001",
                   "Scope Affected":"fica000001",
                   "Identification":"fica000002",
                   "Corporate Action Effective Date":"ficad00003",
                   "Corporate Action Receipt Date":"fiad00004",
                   "Document":"fica000005",
                   "Dividend Announcement Date":"ofdy005005",
                   "Dividend Record Date":"ofdy005007",
                   "Dividend Ex Date":"ofdy005010",
                   "Dividend Payment Date":"ofdy005015",
                   "Dividend Gross":"ofdy005020",
                   "Dividend Net":"ofdy005022",
                   "How is the Dividend payed?":"fica003021"}

df = pd.DataFrame(index=range(5),columns=dict_ca['Dividends'])

app.layout = html.Div([
                    html.Div([
                        html.Div([
                                    html.H5("INSERT NEW CORPORATE ACTIONS")
                                    ])
                            ]),
                    html.Div([
                        dcc.Dropdown(id = 'type_corp_act',
                                     multi = False,
                                     value = 'Dividends',
                                     options = list(dict_ca.keys())
                                     )
                            ]),
                    html.Div([
                            dash_table.DataTable(
                                id='tbl',
                                data=df.to_dict('records'),
                                columns = [{"name": i, "id": i, "presentation": "dropdown", "type": dict_ca_types[i]} if i in ['Scope Affected','Corporate Action Status'] else {"name": i, "id": i, "type": dict_ca_types[i]} for i in df.columns],
                                editable=True,
                                dropdown={
                                    'Scope Affected': {
                                        'options': [ {'label': i, 'value': i} for i in ["1","2","3"] ]
                                        },
                                    'Corporate Action Status': {
                                        'options': [ {'label': i, 'value': i} for i in ["N"] ]
                                        }
                                    },
                                row_deletable=True
                                ),
                            html.Div(id='tbl-container')
                            ]),
                    html.Div(
                            [
                                html.Button('Add Row', id='editing-rows-button', n_clicks=0),
                                ]
                            ),
                    html.Div(
                            [
                                html.Button('Insert Data', id='tbl-button-insertinto', n_clicks=0),
                                html.Div(id = 'tbl-text-status')
                                ]
                            ),
                    html.Div(
                            [
                                dcc.Upload(
                                            id = 'upload_doc',
                                            children = html.Div([
                                                                 'Drag and Drop or ',
                                                                 html.A('Select Files')
                                                                ]),
                                            style = {
                                                    'width': '20%',
                                                    'height': '60px',
                                                    'lineHeight': '60px',
                                                    'borderWidth': '1px',
                                                    'borderStyle': 'dashed',
                                                    'borderRadius': '5px',
                                                    'textAlign': 'center',
                                                    'margin': '10px'
                                                    }
                                            )
                                ]
                            ),
                    html.Div(id='output-data-upload'),
                    html.Div([
                                dcc.Textarea(
                                             id = 'textarea-state-example',
                                             value = 'Name of the document to save in SFTP',
                                             style = {'width': '30%', 'height': 20},
                                             ),
                                html.Button(
                                            'Submit',
                                            id = 'textarea-state-example-button',
                                            n_clicks = 0
                                            ),
                                html.Div(
                                         id = 'textarea-state-example-output'
                                         )
                            ]),
                    html.Div([
                        html.Div([
                                    html.H5("UPDATE CORPORATE ACTIONS")
                                    ])
                            ]),
                    html.Div([
                        dcc.Dropdown(id = 'type_corp_act_2',
                                     multi = False,
                                     value = 'Dividends',
                                     options = list(dict_ca.keys())
                                     )
                            ]),
                    html.Div([
                            dash_table.DataTable(
                                id='tbl2',
                                data=df.to_dict('records'),
                                columns = [{"name": i, "id": i, "presentation": "dropdown", "type": dict_ca_types[i]} if i in ['Scope Affected','Corporate Action Status'] else {"name": i, "id": i, "type": dict_ca_types[i]} for i in df.columns],
                                editable=True,
                                dropdown={
                                    'Scope Affected': {
                                        'options': [ {'label': i, 'value': i} for i in ["1","2","3"] ]
                                        },
                                    'Corporate Action Status': {
                                        'options': [ {'label': i, 'value': i} for i in ["M"] ]
                                        }
                                    },
                                row_deletable=True
                                ),
                            html.Div(id='tbl-container2')
                            ]),
                    html.Div(
                            [
                                html.Button('Add Row', id='editing-rows-button2', n_clicks=0),
                                ]
                            ),
                    html.Div(
                            [
                                html.Button('Get data by id', id='tbl-button-selectupd', n_clicks=0)
                                ]
                            ),
                    html.Div(
                            [
                                html.Button('Update Data', id='tbl-button-exec_update', n_clicks=0),
                                html.Div(id = 'tbl-text-status2')
                                ]
                            )
                    ])


# Parse contents
def parse_contents_files(contents, filename):

    if contents is not None:

        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        try:
            
            if 'csv' in filename[-3:].lower():
                # CSV file
                io_obj = io.StringIO(decoded.decode('utf-8'))
                
            elif 'xlsx' in filename[-4:].lower():
                # Excel file
                io_obj = io.BytesIO(decoded)

            elif 'pdf' in filename[-3:].lower():
                # pdf file
                io_obj = io.BytesIO(decoded)

            elif 'png' in filename[-3:].lower():
                # pdf file
                io_obj = io.BytesIO(decoded)

            elif 'docx' in filename[-4:].lower():
                # pdf file
                io_obj = io.BytesIO(decoded)
                
        except:
            
            io_obj = io.StringIO("Error")
    
        return io_obj


# Function to 
def upload_files_to_sftp(file,filename_initial,filename_mod):

    # Connection Credentials.
    host="13.36.102.82"
    port=22
    username="fundiftp9A5"
    password="Y2xwPSWv6v"
    
    # Connection to sftp server
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    conn = pysftp.Connection(host = host,
                             username = username,
                             password = password,
                             cnopts = cnopts,
                             port = port)
    
    io_obj = parse_contents_files(file, filename_initial)    
    
    file_extension = filename_initial.split(".")[-1]
    
    try:
        conn.putfo(io_obj, "corporate-action/" + filename_mod + "." + file_extension)
        status_upload = "Done"
        
    except:
        status_upload = "Error"        
    
    return status_upload

# Definition of the file content
def parse_contents(filename):

    return html.Div([
                    html.H5(filename)
                    ])

# Definition of the file content
def status_pdf(filename):
    return html.Div([
                    html.H5(filename)
                    ])


@app.callback(Output('output-data-upload', 'children'),
              Input('upload_doc', 'contents'),
              Input('upload_doc', 'filename'))
def update_output(filecontent, filename):
    if filecontent is not None:
        children = [parse_contents(filename)]
        return children

@app.callback(
    Output('tbl', 'data'),
    Input('editing-rows-button', 'n_clicks'),
    State('tbl', 'data'),
    State('tbl', 'columns'))
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows

@app.callback(Output('tbl', 'columns'),
              Input('type_corp_act', 'value'))
def actualize_db(type_layout):
    return [{"name": i, "id": i, "presentation":"dropdown"} if i in ['Scope Affected',"Corporate Action Status"] else {"name": i, "id": i} for i in dict_ca[type_layout]]

@app.callback(
    Output('textarea-state-example-output', 'children'),
    Input('textarea-state-example-button', 'n_clicks'),
    Input('upload_doc', 'contents'),
    Input('upload_doc', 'filename'),
    State('textarea-state-example', 'value')
)
def update_output_2(n_clicks, filecontent, filename, value):
    if n_clicks > 0:
        return html.Div([
                        upload_files_to_sftp(filecontent, filename, value)
                        ])

    
@app.callback(
    Output('tbl-text-status', 'children'),
    Input('tbl-button-insertinto', 'n_clicks'),
    Input('type_corp_act', 'value'),
    [Input('tbl', 'data'),
      Input('tbl', 'columns')])
def insert_into_ca(n_clicks, type_of_ca, data, cols):

    if n_clicks > 0:

        if type_of_ca == 'Dividends':
            
            # Create the data frame
            df = pd.DataFrame(data, columns=[ c['name'] for c in cols])
            df = df.drop(['Corporate Action Status','If modification id'],axis=1)
            df.columns = [dict_div_rename[i] for i in df.columns]
            df['ficad00000'] = 'N'

            # Type of corporate actions
            df['fica000004'] = "1"

            # Timestamp
            datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.000")
            df['fica000008'] = datetime_now
            
            # Divide the data frame between:
            # Insert-into
            df_new = df.drop('fica000007',axis=1)
            
            # Conditional
            if len(df_new) > 0:
            
                # Insert-into
                list_insert_into = [(i[0].strip(),
                                      i[1].strip(),
                                      int(i[2].strip()),
                                      i[3].strip(),
                                      i[4].strip(),
                                      i[5].strip(),
                                      i[6].strip(),
                                      i[7].strip(),
                                      i[8].strip(),
                                      i[9].strip(),
                                      i[10].strip(),
                                      float(i[11].replace(",",".").strip()),
                                      float(i[12].replace(",",".").strip()),
                                      i[13].strip(),
                                      int(i[14].strip()),
                                      i[15].strip()) for i in df_new.to_numpy()]
    
                # New Backend (POSTGRES)
                newbackend_ca_db = psycopg2.connect(host = "db-dev-cluster.cdv9yi5xuzxq.eu-west-3.rds.amazonaws.com",
                                                    database = "corporate actions",
                                                    user = "postgres",
                                                    password = "934m$b&QnCrk")
                cursor = newbackend_ca_db.cursor() 
                cursor.executemany(' INSERT INTO dividends ' + "(" + ",".join(df_new.columns) + ")" +\
                                    ' VALUES ' + "(" + ",".join(["%s" for i in df_new.columns]) + ")",
                                    list_insert_into)
                newbackend_ca_db.commit()
                cursor.close()
        
    
    return html.Div([
                    html.H5("Done")
                    ])

@app.callback(
    Output('tbl2', 'data'),
    Input('tbl-button-selectupd', 'n_clicks'),
    Input('type_corp_act_2', 'value'),
    [State('tbl2', 'data'),
     Input('tbl2', 'columns')])
def select_ca(n_clicks, type_of_ca, data, cols):

    if n_clicks > 0:

        if type_of_ca == "Dividends":
            
            # Create the data frame
            df = pd.DataFrame(data, columns=[ c['name'] for c in cols])
            df.columns = [dict_div_rename[i] for i in df.columns]
            select_ids = df['fica000007'][df['fica000007'] != ""].dropna()
            select_ids = tuple(select_ids)
            
            # New Backend (POSTGRES)
            newbackend_ca_db = psycopg2.connect(host = "db-dev-cluster.cdv9yi5xuzxq.eu-west-3.rds.amazonaws.com",
                                                database = "corporate actions",
                                                user = "postgres",
                                                password = "934m$b&QnCrk")
            
            # Get information
            dict_temp = dict(zip(list(dict_div_rename.values()),list(dict_div_rename.keys())))
            df_get_info = pd.read_sql_query(f'SELECT * FROM dividends WHERE fica000007 in {select_ids}', newbackend_ca_db)[list(dict_temp.keys())]
            df_get_info.columns = [dict_temp[i] for i in df_get_info.columns]
        
    else:

        # Create the data frame
        df = pd.DataFrame(data, columns=[ c['name'] for c in cols])
        df = df.drop('If modification id',axis=1)
        df.columns = [dict_div_rename[i] for i in df.columns]
        df_get_info = df.copy()

    return df_get_info.to_dict('records')

@app.callback(
    Output('tbl-text-status2', 'children'),
    Input('tbl-button-exec_update', 'n_clicks'),
    Input('type_corp_act_2', 'value'),
    [State('tbl2', 'data'),
      Input('tbl2', 'columns')])
def update_ca(n_clicks, type_of_ca, data, cols):

    if n_clicks > 0:

        if type_of_ca == 'Dividends':
            
            # Create the data frame
            df = pd.DataFrame(data, columns=[ c['name'] for c in cols])
            df = df.drop(['Corporate Action Status'],axis=1)
            df.columns = [dict_div_rename[i] for i in df.columns]
            df['ficad00000'] = "M"

            # Type of corporate actions
            df['fica000004'] = "1"

            # Timestamp
            datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.000")
            df['fica000008'] = datetime_now
            
            # Divide the data frame between:
            # Update
            df_modified = df.copy()            
            df_modified = df_modified.astype(str)
            
            # Conditional
            if len(df_modified) > 0:
            
                # Update
                list_update = [(i[1].strip(),
                                int(i[2].strip()),
                                i[3].strip(),
                                i[4].strip(),
                                i[5].strip(),
                                i[6].strip(),
                                i[7].strip(),
                                i[8].strip(),
                                i[9].strip(),
                                i[10].strip(),
                                float(i[11].replace(",",".").strip()),
                                float(i[12].replace(",",".").strip()),
                                i[13].strip(),
                                i[14].strip(),
                                int(i[15].strip()),
                                i[16].strip(),
                                int(i[0].strip())) for i in df_modified.to_numpy()]
                
                # # New Backend (POSTGRES)
                newbackend_ca_db = psycopg2.connect(host = "db-dev-cluster.cdv9yi5xuzxq.eu-west-3.rds.amazonaws.com",
                                                    database = "corporate actions",
                                                    user = "postgres",
                                                    password = "934m$b&QnCrk")
                cursor = newbackend_ca_db.cursor() 
                cursor.executemany(f'UPDATE dividends'
                                    ' SET ' +  " = %s,".join(df_modified.columns[1:]) + " = %s" +\
                                    ' WHERE fica000007 = %s',
                                    list_update)
                newbackend_ca_db.commit()
                cursor.close()

            text_to_show = "Done"

    else:
        
        text_to_show = ""
    
    return html.Div([
                    html.H5(text_to_show)
                    ])



if __name__ == '__main__':
    app.run_server(debug=True)