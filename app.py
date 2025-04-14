# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from models.account_types import SavingAccount, checkingAccount
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
accounts = {}

@app.route('/')
def index():
    return render_template('index.html', accounts=accounts)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        account_type = request.form.get('account_type')
        account_number = request.form.get('account_number')
        initial_balance = float(request.form.get('initial_balance', 0))

        if account_number in accounts:
            flash('Account number already exists!', 'error')
        elif account_type == 'saving':
            accounts[account_number] = SavingAccount(account_number, initial_balance)
            flash('Saving account created successfully!', 'success')
        elif account_type == 'checking':
            accounts[account_number] = checkingAccount(account_number, initial_balance)
            flash('checking account created!', 'success')
        else:
            flash('Invalid account type', 'error')

        return redirect(url_for('index'))

    return render_template('create_account.html')

@app.route('/deposit/<account_number>', methods=['GET', 'POST'])
def deposit(account_number):
    account = accounts.get(account_number)
    if not account:
        flash('Account not found', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        note = request.form.get('note', '')
        success, message = account.deposit(amount, note)
        flash(message, 'success' if success else 'error')
        return redirect(url_for('account_detail', account_number=account_number))

    return render_template('deposit.html', account=account)

@app.route('/withdraw/<account_number>', methods=['GET', 'POST'])
def withdraw(account_number):
    account = accounts.get(account_number)
    if not account:
        flash('Account not found', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        success, message = account.withdraw(amount)
        flash(message, 'success' if success else 'error')
        return redirect(url_for('account_detail', account_number=account_number))

    return render_template('withdraw.html', account=account)

@app.route('/account/<account_number>')
def account_detail(account_number):
    account = accounts.get(account_number)
    if not account:
        flash('Account not found', 'error')
        return redirect(url_for('index'))

    transactions = account.transactions[-10:]
    chart_data = {
        'dates': [t['date'] for t in transactions],
        'deposits': [t['amount'] if t['type'] == 'deposit' else 0 for t in transactions],
        'withdrawals': [t['amount'] if t['type'] == 'withdrawal' else 0 for t in transactions]
    }

    return render_template('account_detail.html', account=account, transactions=transactions, chart_data=json.dumps(chart_data))

if __name__ == '__main__':
    app.run(debug=True)
