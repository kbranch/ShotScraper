import sql
from flask import Flask, request

app = Flask(__name__)

@app.after_request
def afterRequest(response):
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route("/")
def root():
    return {'status': 'OK'}

@app.route("/api/rankings", methods=['GET'])
def getRankings():
    kingdom = request.args.get('kingdom')
    startDate = request.args.get('startDate') or '2025-07-01'
    endDate = request.args.get('endDate') or '3000-01-01'
    type = 'Personal Power'

    data = sql.getRankings(kingdom, type, startDate, endDate)

    return data

@app.route("/api/growth", methods=['GET'])
def getGrowth():
    kingdom = request.args.get('kingdom')
    startDate = request.args.get('startDate') or '2025-07-01'
    endDate = request.args.get('endDate') or '3000-01-01'
    type = 'Personal Power'

    data = sql.getGrowth(kingdom, type, startDate, endDate)

    return data

@app.route("/api/allianceGrowth", methods=['GET'])
def getAllianceGrowth():
    kingdom = request.args.get('kingdom')
    startDate = request.args.get('startDate') or '2025-07-01'
    endDate = request.args.get('endDate') or '3000-01-01'
    type = 'Personal Power'

    data = sql.getAllianceGrowth(kingdom, type, startDate, endDate)

    return data

if __name__ == "__main__":
    app.run()
