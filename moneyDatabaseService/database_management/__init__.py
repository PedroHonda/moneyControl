import os
import sqlite3
import datetime
from flask import Flask, request, g
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

moneyDB = os.path.realpath(__file__).split('database_management')[0]+'databases/money.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            moneyDB,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

class Home(Resource):
    def get(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select * from sqlite_master where type = 'table';")

        tables = {}
        for t in cursor.fetchall():
            cursor.execute("select * from " + t[1] + ";")
            data = cursor.fetchall()
            tables[t[1]] = data
        
        return tables, 200

class BuyingStock(Resource):
    def get(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select rowId,* from buyingStock")
        data = cursor.fetchall()
        dataList = []

        # fixing datetime issue
        for i in data:
            i = list(i)
            for index,j in enumerate(i):
                if isinstance(j, datetime.date):
                    i[index] = str(j)
            dataList.append(i)

        return dataList, 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('date', type=str, help='Date must be a String')
        parser.add_argument('stock', type=str, help='Stock name must be a String')
        parser.add_argument('quantity', type=int, help='Quantity must be a Float')
        parser.add_argument('value', type=float, help='Value litre must be a Float')
        parser.add_argument('totalValue', type=float, help='Total Value must be a Float')
        parser.add_argument('totalValuePaid', type=float, help='Total Value Paid must be a Float')
        try:
            args = parser.parse_args()      
        except:
            return {"Bad Input! Follow the example..." : {
                    "date" : "2019-05-28",
                    "stock" : "ITUB4",
                    "quantity" : 100,
                    "value" : 34.08,
                    "totalValue" : 3408.00,
                    "totalValuePaid" : 3409.20
                }}, 400

        db = get_db()
        cursor = db.cursor()

        values = [args['date'], args['stock'], args['quantity'], args['value'], args['totalValue'], args['totalValuePaid']]

        sqlCmd = "insert into buyingStock(date, stock, quantity, value, totalValue, totalValuePaid) values (?,?,?,?,?,?)"
        cursor.execute(sqlCmd, values)
        db.commit()

        cursor.execute("select quantity,meanValue,totalValue from currentStock where stock = '" + args['stock'] + "';")
        currentStockInfo = cursor.fetchall()
            # currentQuantity = currentStockInfo[0]
            # currentMeanValue = currentStockInfo[1]
            # currentTotalValue = currentStockInfo[2]

        # If the stock is currently available on currentStock table
        if currentStockInfo:
            currentStockInfo = list(currentStockInfo[0])
            currentStockInfo[1] = (currentStockInfo[2] + args['totalValuePaid']) / (currentStockInfo[0] + args['quantity'])
            currentStockInfo[0] += args['quantity']
            currentStockInfo[2] += args['totalValuePaid']
            currentStockInfo.append(args['stock'])

            # keep meanValue with only 3 decimal points
            sqlCmd = "update currentStock set quantity = ?, meanValue = ?, totalValue = ? where stock = ?;"
            cursor.execute(sqlCmd, currentStockInfo)
            db.commit()
        # If the stock is not currently available on currentStock table (new purchase)
        else:
            sqlCmd = "insert into currentStock(stock, quantity, meanValue, totalValue) values (?,?,?,?)"
            currentStockInfo = [args['stock'], args['quantity'], args['totalValuePaid'] / args['quantity'], args['totalValuePaid']]
            cursor.execute(sqlCmd, currentStockInfo)
            db.commit()

        return args, 200

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('date', type=str, help='Date must be a String')
        parser.add_argument('stock', type=str, help='Stock name must be a String')
        parser.add_argument('quantity', type=int, help='Quantity must be a Float')
        parser.add_argument('value', type=float, help='Value litre must be a Float')
        parser.add_argument('totalValue', type=float, help='Total Value must be a Float')
        parser.add_argument('totalValuePaid', type=float, help='Total Value Paid must be a Float')
        parser.add_argument('rowId', type=int, help='RowId Received must be a Int')
        args = parser.parse_args()

        return args, 200

class SellingStock(Resource):
    def get(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select rowId,* from sellingStock")
        data = cursor.fetchall()
        dataList = []

        # fixing datetime issue
        for i in data:
            i = list(i)
            for index,j in enumerate(i):
                if isinstance(j, datetime.date):
                    i[index] = str(j)
            dataList.append(i)

        return dataList, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('date', type=str, help='Date must be a String')
        parser.add_argument('stock', type=str, help='Stock name must be a String')
        parser.add_argument('quantity', type=int, help='Quantity must be a Float')
        parser.add_argument('value', type=float, help='Value litre must be a Float')
        parser.add_argument('totalValue', type=float, help='Total Value must be a Float')
        parser.add_argument('totalValueReceived', type=float, help='Total Value Received must be a Float')
        try:
            args = parser.parse_args()      
        except:
            return {"Bad Input! Follow the example..." : {
                    "date" : "2019-05-28",
                    "stock" : "ITUB4",
                    "quantity" : 100,
                    "value" : 34.08,
                    "totalValue" : 3408.00,
                    "totalValueReceived" : 3409.20
                }}, 400

        db = get_db()
        cursor = db.cursor()

        values = [args['date'], args['stock'], args['quantity'], args['value'], args['totalValue'], args['totalValueReceived']]

        sqlCmd = "insert into sellingStock(date, stock, quantity, value, totalValue, totalValueReceived) values (?,?,?,?,?,?)"
        cursor.execute(sqlCmd, values)
        db.commit()
        return args, 200

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('date', type=str, help='Date must be a String')
        parser.add_argument('stock', type=str, help='Stock name must be a String')
        parser.add_argument('quantity', type=int, help='Quantity must be a Float')
        parser.add_argument('value', type=float, help='Value litre must be a Float')
        parser.add_argument('totalValue', type=float, help='Total Value must be a Float')
        parser.add_argument('totalValueReceived', type=float, help='Total Value Received must be a Float')
        parser.add_argument('rowId', type=int, help='RowId Received must be a Int')
        args = parser.parse_args()

        return args, 200

class CurrentStock(Resource):
    def get(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select * from currentStock;")
        data = cursor.fetchall()
        
        return data, 200

api.add_resource(Home, '/')
api.add_resource(BuyingStock, '/buy')
api.add_resource(SellingStock, '/sell')
api.add_resource(CurrentStock, '/current')