from flask import Flask, request
import pymysql
from flask import jsonify, json
# This function does takes the connection between the DataBase and our API
def startdb():
    # print("db connect")
    return pymysql.connect("localhost", "root", "******", "*********")

app = Flask(__name__)



@app.route('/energymeter', methods=['POST'])
def addhardness():
    db = startdb()
    cursor = db.cursor()
    try:
         _json = request.json
         _serviceData = _json['energy']
         if request.method == 'POST':
            meter = _serviceData.split(":")
            if meter[0] == '1':
                sql = "INSERT INTO powerReadings(power, temparature, humidity) VALUES(%s,%s,%s)"
                cursor.execute(sql, (meter[1], meter[2], meter[3]))
                db.commit()
                resp = jsonify({'status': 'success', 'code': 200, 'message': 'added successfully!'})
                resp.status_code = 200
                return resp
            elif meter[0] == "2":
                sql = "INSERT INTO 	magnetdetection(magnetalert) VALUES(%s)"
                cursor.execute(sql, (meter[1]))
                db.commit()
                resp = jsonify({'status': 'success', 'code': 200, 'message': 'added successfully!'})
                resp.status_code = 200
                return resp
            elif meter[0] == '3':
                sql = "INSERT INTO temphumidalert(temparature, humidity) VALUES(%s,%s)"
                cursor.execute(sql, (meter[1], meter[2]))
                db.commit()
                resp = jsonify({'status': 'success', 'code': 200, 'message': 'added successfully!'})
                resp.status_code = 200
                return resp
            elif meter[0] == '4':
                sql = "INSERT INTO powerconsuption(powerconsuption) VALUES(%s)"
                cursor.execute(sql, (meter[1]))
                db.commit()
                resp = jsonify({'status': 'success', 'code': 200, 'message': 'added successfully!'})
                resp.status_code = 200
                return resp
            else:
                return jsonify({'status': 'error', 'code': '400', 'message': 'incorrect data'})
         else:
             return not_found()
    except Exception as e:
         resp = jsonify({'status': 'error', 'code': '400', 'message': str(e)})
         return resp
    finally:
        cursor.close() 
        db.close()


def not_found():
    return jsonify({'status': 'error', 'code': '400', 'message': 'SQL error'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8200)
