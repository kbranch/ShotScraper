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
# @cross_origin()
def root():
    return {'status': 'OK'}

@app.route("/api/rankings", methods=['GET'])
# @cross_origin()
def getRankings():
    kingdom = request.args.get('kingdom')
    type = 'Personal Power'

    rankings = sql.getRankings(kingdom, type)

    return {'rankings': rankings}

if __name__ == "__main__":
    app.run()
