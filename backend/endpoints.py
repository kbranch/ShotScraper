import sql
from flask import Flask, render_template, request, redirect
# from flask_cors import CORS, cross_origin

app = Flask(__name__)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

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
    type = 'Personal Power'

    data = sql.getRankings(kingdom, type)

    return data

@app.route("/api/growth", methods=['GET'])
def getGrowth():
    kingdom = request.args.get('kingdom')
    type = 'Personal Power'

    data = sql.getGrowth(kingdom, type)

    return data

if __name__ == "__main__":
    app.run()
