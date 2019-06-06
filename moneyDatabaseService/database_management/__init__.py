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
            # fixing datetime issue
            dataList = []
            for i in data:
                i = list(i)
                for index,j in enumerate(i):
                    if isinstance(j, datetime.date):
                        i[index] = str(j)
                dataList.append(i)
            tables[t[1]] = dataList
        return tables, 200

class BuyingStock(Resource):
    badInput = {"Bad Input! Follow the example..." : {
                    "date" : "2019-05-28",
                    "stock" : "ITUB4",
                    "quantity" : 100,
                    "value" : 34.08,
                    "totalValue" : 3408.00,
                    "totalValuePaid" : 3409.20
                }}
    
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
            return self.badInput, 400

        args['date'] = args['date'].replace('/', '-')

        values = [args['date'], args['stock'], args['quantity'], args['value'], args['totalValue'], args['totalValuePaid']]
        for v in values:
            if not v:
                return self.badInput, 400

        db = get_db()
        cursor = db.cursor()

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
        try:
            args = parser.parse_args()      
        except:
            return {"Bad Input! Follow the example..." : {
                    "date" : "2019-05-28",
                    "stock" : "ITUB4",
                    "quantity" : 100,
                    "value" : 34.08,
                    "totalValue" : 3408.00,
                    "totalValuePaid" : 3409.20,
                    "rowId" : 4
                }}, 400
        if args['date']:
            args['date'] = args['date'].replace('/', '-')
        rowId = args['rowId']
        if not rowId:
            return 'Please provide a rowId number to update the values', 400
        # Deleting arguments which were not changed
        args = {key:value for key,value in args.items() if args[key]}

        db = get_db()
        cursor = db.cursor()

        values = []
        sqlUPDATE = "update buyingStock set "
        for key in args:
            sqlUPDATE += key + " = ? , "
            values.append(args[key])
        sqlUPDATE = sqlUPDATE[:-2] + " where rowId = ? ;"
        values.append(rowId)
        cursor.execute(sqlUPDATE, values)
        db.commit()

        # we also need to correctly recalculate the currentStock table's values (quantity, meanValue and totalValue) as well
        cursor.execute("select stock from buyingStock where rowId = ? ;", [rowId])
        stockCode = cursor.fetchall()[0][0]

        cursor.execute("select * from buyingStock where stock = '" + stockCode + "';")
        allBuying = cursor.fetchall()

        quantity = 0
        totalValue = 0
        for operation in allBuying:
            quantity += operation[2]
            totalValue += operation[5]
            meanValue = totalValue / quantity
    
        sqlCmd = "update currentStock set quantity = ?, meanValue = ?, totalValue = ? where stock = ?;"
        currentStockInfo = [quantity, meanValue, totalValue, stockCode]
        cursor.execute(sqlCmd, currentStockInfo)
        db.commit()

        return args, 200

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("delete from buyingStock;")
        db.commit()

        return "Success!", 200

class SellingStock(Resource):
    badInput = {"Bad Input! Follow the example..." : {
                    "date" : "2019-05-28",
                    "stock" : "ITUB4",
                    "quantity" : 100,
                    "value" : 34.08,
                    "totalValue" : 3408.00,
                    "totalValueReceived" : 3409.20
                }}

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
            return self.badInput, 400

        args['date'] = args['date'].replace('/', '-')

        values = [args['date'], args['stock'], args['quantity'], args['value'], args['totalValue'], args['totalValueReceived']]
        for v in values:
            if not v:
                return self.badInput, 400

        db = get_db()
        cursor = db.cursor()

        # seems that date with "slash format" (209/05/28) is not well received by SQL, so I am converting it by force here
        args['date'] = args['date'].replace('/', '-')

        cursor.execute("select quantity,meanValue,totalValue from currentStock where stock = '" + args['stock'] + "';")
        currentStockInfo = cursor.fetchall()
            # currentQuantity = currentStockInfo[0]
            # currentMeanValue = currentStockInfo[1]
            # currentTotalValue = currentStockInfo[2]

        # If the stock is currently available on currentStock table
        if currentStockInfo:
            currentStockInfo = list(currentStockInfo[0])
            # mean Value unchanged
            currentStockInfo[0] -= args['quantity']
            currentStockInfo[2] -= args['quantity']*currentStockInfo[1]
            currentStockInfo.append(args['stock'])

            sqlCmd = "update currentStock set quantity = ?, meanValue = ?, totalValue = ? where stock = ?;"
            cursor.execute(sqlCmd, currentStockInfo)
            db.commit()
        # If the stock is not currently available on currentStock table (new purchase)
        else:
            return "Stock not available on currentStock table! Not Found!", 404


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
        try:
            args = parser.parse_args()      
        except:
            return {"Bad Input! Follow the example..." : {
                    "date" : "2019-05-28",
                    "stock" : "ITUB4",
                    "quantity" : 100,
                    "value" : 34.08,
                    "totalValue" : 3408.00,
                    "totalValueReceived" : 3409.20,
                    "rowId" : 4
                }}, 400

        if args['date']:
            args['date'] = args['date'].replace('/', '-')
        rowId = args['rowId']
        if not rowId:
            return 'Please provide a rowId number to update the values', 400
        # Deleting arguments which were not changed
        args = {key:value for key,value in args.items() if args[key]}

        db = get_db()
        cursor = db.cursor()

        values = []
        sqlUPDATE = "update sellingStock set "
        for key in args:
            sqlUPDATE += key + " = ? , "
            values.append(args[key])
        sqlUPDATE = sqlUPDATE[:-2] + " where rowId = ? ;"
        values.append(rowId)
        cursor.execute(sqlUPDATE, values)
        db.commit()

        # we also need to correctly recalculate the currentStock table's values (quantity, meanValue and totalValue) as well
        cursor.execute("select stock from sellingStock where rowId = ? ;", [rowId])
        stockCode = cursor.fetchall()[0][0]

        cursor.execute("select * from sellingStock where stock = '" + stockCode + "';")
        allSelling = cursor.fetchall()

        cursor.execute("select * from buyingStock where stock = '" + stockCode + "';")
        allBuying = cursor.fetchall()

        # for selling operation, only quantity matters when updating currentStock table
        # first get from buyingStock the total quantity available there
        quantity = 0
        for operation in allBuying:
            quantity += operation[2]
        # then subtract the quantity available after selingStock table was updated
        for operation in allSelling:
            quantity -= operation[2]
    
        # get current meanValue available on currentStock table
        cursor.execute("select meanValue from currentStock where stock = '" + stockCode + "';")
        meanValue = cursor.fetchall()[0][0]

        # totalValue is then the meanValue with the new value of quantity
        totalValue = meanValue * quantity

        sqlCmd = "update currentStock set quantity = ?, meanValue = ?, totalValue = ? where stock = ?;"
        currentStockInfo = [quantity, meanValue, totalValue, stockCode]
        cursor.execute(sqlCmd, currentStockInfo)
        db.commit()

        return args, 200

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("delete from sellingStock;")
        db.commit()

        return "Success!", 200

class CurrentStock(Resource):
    def get(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select * from currentStock;")
        data = cursor.fetchall()
        
        return data, 200

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("delete from currentStock;")
        db.commit()

        return "Success!", 200

class getBuyingStockPerCode(Resource):
    def get(self, stockCode):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select * from buyingStock where stock = '" + stockCode + "';")
        data = cursor.fetchall()
        
        return data, 200

class getSellingStockPerCode(Resource):
    def get(self, stockCode):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select * from sellingStock where stock = '" + stockCode + "';")
        data = cursor.fetchall()
        
        return data, 200

class getCurrentStockPerCode(Resource):
    def get(self, stockCode):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select * from currentStock where stock = '" + stockCode + "';")
        data = cursor.fetchall()
        
        return data, 200

api.add_resource(Home, '/')
api.add_resource(BuyingStock, '/buy')
api.add_resource(SellingStock, '/sell')
api.add_resource(CurrentStock, '/current')
api.add_resource(getBuyingStockPerCode, '/buy/<string:stockCode>')
api.add_resource(getSellingStockPerCode, '/sell/<string:stockCode>')
api.add_resource(getCurrentStockPerCode, '/current/<string:stockCode>')
