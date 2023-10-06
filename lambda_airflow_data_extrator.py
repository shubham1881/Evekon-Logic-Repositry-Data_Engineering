import boto3
import http.client
import base64
import pandas as pd
from datetime import datetime
from io import StringIO
import ast


mwaa_env_name = 'env_name'
#mwaa_cli_command = 'dags list-runs --dag kdh_source_to_curated_ebs_pipeline --start-date 2023-09-04'
mwaa_cli_command=f'dags list-runs --dag dag_name'
client = boto3.client('mwaa')

def lambda_handler(event, context):

    mwaa_cli_token = client.create_cli_token(
            Name=mwaa_env_name)

    print(f" token is {mwaa_cli_token}")

    conn = http.client.HTTPSConnection(mwaa_cli_token['WebServerHostname'])
    print(f"here is the connection info {conn}")
    payload = mwaa_cli_command
    headers = {
    'Authorization': 'Bearer ' + mwaa_cli_token['CliToken'],
    'Content-Type': 'text/plain'
    }

    try :
        conn.request("POST", "/aws_mwaa/cli", payload, headers)
    except Exception as e:
        print(f"An error occurred : {e}")

    res = conn.getresponse()
    data = res.read()
    dict_str = data.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)

    #print(f"dict {base64.b64decode(mydata['stdout'])}")

    st=base64.b64decode(mydata['stdout'])
    #data_s = mydata['stdout']
    s=str(st,'utf-8')

    data = StringIO(s)

    df=pd.read_csv(data, sep='|')
    #df=df[0]
    #print(f"here is df zero {df[0]}")

    s3 = boto3.resource('s3')
    bucket_name = 'gilead-kdh-dev-us-west-2-raw'
    prefix=f"Testing_dag_status/status.csv"
    csv_buffer=StringIO()
    df.to_csv(csv_buffer,index=True)
    s3.Object(bucket_name,prefix).put(Body=csv_buffer.getvalue())
    print("uploaded successful")



    print(f"final df is {df}")
    return base64.b64decode(mydata['stdout'])