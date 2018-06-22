#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)


class Masternodes(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from masternodes") # This line performs query and returns json result
        return {'masternodes': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID
    
    def post(self):
        conn = db_connect.connect()
        print(request.json)
        ServiceID = request.json['ServiceID']
        Coin = request.json['Coin']
        IPaddress = request.json['IPaddress']
        Status = request.json['ReportsTo']
        query = conn.execute("insert into employees values(null,'{0}','{1}','{2}','{3}')".format(ServiceID,Coin,IPaddress,
                             Status))
        return {'status':'success'}
    def update(self):
        conn = db_connect.connect()
        print(request.json)# shitty code
        MNID = request.json['MNID']
        Change = request.json['Change']# Coin, IPaddress, Status..
        ChangeTo = request.json['ChangeTo'] # what to change it to
        query = conn.execute("update masternodes set json.loads{0} = 'json.loads{1}' WHERE ID {0}".format(MNID,Change,ChangeTo))
        return {'status':'success'}    

    
class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

    
class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(Masternodes, '/masternodes') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3


if __name__ == '__main__':
     app.run()
