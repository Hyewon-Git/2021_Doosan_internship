from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import boto3
from werkzeug.wrappers import response
import api 
from response import *
# from config import *

app = Flask(__name__)
CORS(app)
# 계정이름 리스트에 넣어서
credentials = ["di-prd","div-prd"]
session_dic={}

for i in credentials:
    session_dic[i] = boto3.Session(profile_name=i,region_name="ap-northeast-2")

def ec2():
    print("describe ec2")
    try:
        hw_ec2 = boto3.client(
            service_name='ec2',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_EC2_REGION
        )
        hw_ec2_response = hw_ec2.describe_instances()
        print(hw_ec2)
    except Exception as e:
        print(e)
        exit("FAIL")
    else:
        return hw_ec2_response

@app.route('/')
def h_check():
    print("start")
    return jsonify("check : True")
    

@app.route('/test')
def test():
    print("test")
    return jsonify(data)

try:
    account = request.args['account']
except Exception as e:
    account = "All"
print("account: ", account)
origin_elb = api.elb_class(session_dic,account)
origin_elb.lookup()

@app.route('/elb', methods=['GET','POST'])
def elb_list():
    elb = origin_elb
    # try:
    #     account = request.args['account']
    # except Exception as e:
    #     account = "All"
    # elb = api.elb_class(session_dic,account)
    # all elb list
    if request.method == 'GET':
        return jsonify(elb.result)
    # refresh elb
    if request.method == 'POST': 
        refresh_elb = api.elb_class(session_dic,account)
        # elb_name_list = request.form['elb_names']
        elb = refresh_elb
        return jsonify(elb.lookup())
        
if __name__ == '__main__' :
    

    app.run(host='0.0.0.0', port='5000', debug=True)