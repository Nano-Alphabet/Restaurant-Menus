import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Restaurant and Menuitems").sheet1
sh = client.open("Restaurant and Menuitems").get_worksheet(1)

@app.route("/")
def HelloWorld():
    hi = sheet.get_all_records()
    return render_template('home.html', items=hi)


@app.route("/Home", methods=['GET', 'POST'])
def home():
    hi = sheet.get_all_records()
    if request.method == 'POST':
        Name = request.form.get('name')
        Address = request.form.get('address')
        Number = request.form.get('phone_no')
        Ar = [int(x.get("id")) for x in hi]
        try:
            I = max(Ar)+1
        except:
            I=1
        row = [I, Name, Address, Number]
        sheet.append_row(row)
    hi = sheet.get_all_records()
    return render_template('home.html', items=hi)


@app.route("/Del", methods=['GET', 'POST'])
def del_res():
    by = sh.get_all_records()
    if (request.method == 'POST'):
        name = request.form.get('name')
        cell = sheet.find(name)
        Id=sheet.cell(cell.row,0).value
        for i in range(len(by)):
            if j.get("restaurant_id") == Id:
                sh.delete_row(i)
        sheet.delete_row(cell.row)
    hi = sheet.get_all_records()
    return render_template("home.html", items=hi)
@app.route("/restaurants/<int:restaurant_id>/", methods=['GET', 'POST'])
def AddItems(restaurant_id):
    item = sh.get_all_records()
    if request.method=='POST':
        Name=request.form.get('name')
        Price=request.form.get('price')
        Ar = [int(x.get("id")) for x in item]
        try:
            I = max(Ar)+1
        except:
            I=1
        row = [I, Name, Price, restaurant_id]
        sh.append_row(row)
    item = sh.get_all_records()
    Ar=[]
    for i in item:
        if i.get("restaurant_id")==restaurant_id:
            Ar.append(i)
    return render_template('MenuItem.html', items=Ar, id=restaurant_id)
@app.route("/del_item<int:restaurant_id>/", methods=['GET', 'POST'])
def del_item(restaurant_id):
    if (request.method == 'POST'):
        name = request.form.get('name')
        cell = sh.find(name)
        sh.delete_row(cell.row)
    item = sh.get_all_records()
    Ar = []
    for i in item:
        if i.get("restaurant_id") == restaurant_id:
            Ar.append(i)
    return render_template('MenuItem.html', items=Ar, id=restaurant_id)
