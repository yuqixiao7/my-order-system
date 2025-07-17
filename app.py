from flask import Flask, request, render_template,redirect,url_for
from datetime import datetime
import csv
import os
app = Flask(__name__)

# CSV_FILE = 'orders.csv'

# 填單頁面
@app.route('/')
def index():
    success = request.args.get('success')
    return render_template('form.html',success=success)

@app.route('/submit', methods=['POST'])
def submit():
    product = request.form['product']
    quantity = request.form['quantity']
    url = request.form['url']
    note = request.form['note']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 現在時間（格式化）
    with open('orders.csv', mode='a', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp,product, quantity, url, note])

    return redirect(url_for('index', success=1))

@app.route('/orders')
def orders():
    data = []
    with open('orders.csv', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return render_template('orders.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)