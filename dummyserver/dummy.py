from flask import Flask
from flask import request
from flask import render_template
from flask_cors import CORS
import pandas as pd
import datetime
app = Flask(__name__)
CORS(app)

pathTo = '/Users/xuan/Desktop/BoData-Project/dummyserver/'

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


filepath = pathTo + 'boData_mockupUser (1).xlsx'
xl = pd.ExcelFile(filepath)
df1 = xl.parse('Data')
numrows = 730
products = ['Dr. Pepper', '7UP']
mentionsdict = dict()
for i in range(numrows):
    cityname = df1.get_value(i, 'City')
    year = df1.get_value(i, 'Date').year
    month = df1.get_value(i, 'Date').month
    day = df1.get_value(i, 'Date').day
    for product in products:
        tmp = df1.get_value(i, product)
        mentionsdict[ (year, month, day, product, cityname) ] = tmp
print("50%")


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
print("100%")


#@app.route("/getsentimentfigure", methods=["POST"])
def getsentimentfigure_():
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


filepath2 = pathTo + 'Data2.xlsx'
xl2 = pd.ExcelFile(filepath2)
st1 = xl2.parse('Sheet0')
mentionsdict2 = dict()
for i in range(21):
    tmp_keyword = st1.get_value(i, "Keyword")
    tmp_hour = st1.get_value(i, "Hour")
    if (tmp_hour, tmp_keyword) in mentionsdict2:
        mentionsdict2[ (tmp_hour, tmp_keyword) ] += 1
    else:
        mentionsdict2[ (tmp_hour, tmp_keyword) ] = 1
print(mentionsdict2)


sentimentdict2 = dict()
st2 = xl2.parse('Sheet1')
for i in range(21):
    product = st2.get_value(i, 'Key Word')
    #city = "New York"
    s = st2.get_value(i, 'Snippet')
    pon = st2.get_value(i, 'Polarity')
    c = st2.get_value(i, 'Polarity Confidence')
    if not product in sentimentdict2:
        sentimentdict2[product] = [ ]
    sentimentdict2[product].append([s, pon, float(c)])
print(sentimentdict2)


@app.route("/getsentimentfigure", methods=["POST"])
def getsentimentfigure():
    global sentimentdict2
    products = request.form['products']
    if type(products) == str:
        products = eval(products)
    cities = products[1]
    products = products[0]
    result = [ ]
    for product in products:
        if product in sentimentdict2:
            result += sentimentdict2[product]
    return str(result)


@app.route("/getmentionsfigure2", methods=["POST"])
def getmentionsfigure2():
    global mentionsdict2
    begintime = int(request.form['begin'])
    endtime = int(request.form['end'])
    currtime = begintime
    result = [ ]
    while currtime <= endtime:
        product = request.form['products']
        tmp = 0
        if (currtime, product) in mentionsdict2:
            tmp += mentionsdict2[ (currtime, product) ]
        result.append(tmp)
        currtime += 1
    return str(result)


@app.route("/")
def hello():
    return "Hello!"
