from flask import Flask, request, render_template,redirect,url_for
from datetime import datetime
import csv
import os
app = Flask(__name__)

# CSV_FILE = 'orders.csv'

# 填單頁面
@app.route('/', methods=['GET', 'POST'])
def index():
    success = request.args.get('success')
    return render_template('form.html',success=success)

@app.route('/submit', methods=['POST'])
def submit():
    product = request.form['product'].strip()
    quantity = request.form['quantity'].strip()
    url = request.form['url'].strip()
    note = request.form['note'].strip()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 現在時間（格式化）
    # ✅ 後端驗證
    if not product or not quantity or not url:
        return redirect(url_for('index', success=0))
    if not quantity.isdigit() or int(quantity) <= 0:
        return redirect(url_for('index', success=0))
    
    if not url.startswith("http://") and not url.startswith("https://"):
        return redirect(url_for('index', success=0))
    # ✅ 後端驗證結束
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

@app.route('/delete', methods=['POST'])
def delete_order():
    index_to_delete = int(request.form['index'])
    rows = []

    with open('orders.csv', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        rows = list(reader)

    if 0 <= index_to_delete < len(rows):
        rows.pop(index_to_delete)

    with open('orders.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return redirect(url_for('orders'))

if __name__ == '__main__':
    app.run(debug=True)