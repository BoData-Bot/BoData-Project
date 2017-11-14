from flask import Flask
from flask import request
from flask import render_template
from flask_cors import CORS
import pandas as pd
import datetime
app = Flask(__name__)
CORS(app)

pathTo = '/Users/xuan/BoData-Project/dummyserver/'

@app.route('/statics/')
@app.route('/statics/<name>')
def serve_s(name=None):
    f = open(pathTo + "statics/" + name)
    t = f.read()
    f.close()
    return t


@app.route('/statics/js/')
@app.route('/statics/js/<name>')
def serve_js(name=None):
    f = open(pathTo + "statics/js/" + name)
    t = f.read()
    f.close()
    return t


@app.route('/statics/css/')
@app.route('/statics/css/<name>')
def serve_css(name=None):
    f = open(pathTo + "statics/css/" + name)
    t = f.read()
    f.close()
    return t


filepath = pathTo + 'boData_mockupUser.xlsx'
xl = pd.ExcelFile(filepath)
df1 = xl.parse('Data')
numrows = 730
products = ['ProdA', 'ProdB', 'ProdC', 'CompA', 'CompB', 'CompC']
mentionsdict = dict()
for i in range(numrows):
    cityname = df1.get_value(i, 'City')
    year = df1.get_value(i, 'Date').year
    month = df1.get_value(i, 'Date').month
    day = df1.get_value(i, 'Date').day
    for product in products:
        tmp = df1.get_value(i, product)
        mentionsdict[ (year, month, day, product, cityname) ] = tmp


sentimentdict = dict()
df2 = xl.parse('Data2')
numrows2 = 75
for i in range(numrows2):
    product = df2.get_value(i, 'Product')
    city = df2.get_value(i, 'City')
    s = df2.get_value(i, 'Sentence')
    pon = df2.get_value(i, 'Positive or Negative')
    c = df2.get_value(i, 'Confidence Score')
    if not (product, city) in sentimentdict:
        sentimentdict[(product, city)] = [ ]
    sentimentdict[(product, city)].append([s, pon, float(c)])


@app.route("/getsentimentfigure", methods=["POST"])
def getsentimentfigure():
    global sentimentdict
    products = request.form['products']
    if type(products) == str:
        products = eval(products)
    cities = products[1]
    products = products[0]
    result = [ ]
    for product in products:
        for city in cities:
            if (product, city) in sentimentdict:
                result += sentimentdict[(product, city)]
    return str(result)


@app.route("/getmentionsfigure", methods=["POST"])
def getmentionsfigure():
    global mentionsdict
    begindate = request.form['begin'].split("-")
    enddate = request.form['end'].split("-")
    currday = datetime.date(int(begindate[0]), int(begindate[1]), int(begindate[2]))
    endday = datetime.date(int(enddate[0]), int(enddate[1]), int(enddate[2]))
    oneday = datetime.timedelta(1)
    result = [ ]
    while currday <= endday:
        products = request.form['products']
        if type(products) == str:
            products = eval(products)
        cities = products[1]
        products = products[0]
        tmp = 0
        for city in cities:
            for product in products:
                if (currday.year, currday.month, currday.day, product, city) in mentionsdict:
                    tmp += mentionsdict[ (currday.year, currday.month, currday.day, product, city) ]
        result.append(tmp)
        currday += oneday
    return str(result)


@app.route("/")
def hello():
    return "Hello!"

