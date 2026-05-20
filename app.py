from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# -----------------------------
# In-memory Trip Storage
# -----------------------------

current_trip = {
    "name": "",
    "members": [],
    "expenses": []
}

# -----------------------------
# Helper Functions
# -----------------------------

def calc_summary(trip):

    total = sum(e['amount'] for e in trip['expenses'])

    count = len(trip['members'])

    fair_share = total / count if count > 0 else 0

    member_totals = {m: 0 for m in trip['members']}

    for expense in trip['expenses']:
        member_totals[expense['payer']] += expense['amount']

    balances = []

    for member in trip['members']:

        paid = member_totals[member]

        balance = paid - fair_share

        balances.append({
            "name": member,
            "paid": paid,
            "balance": round(balance, 2)
        })

    return {
        "total": round(total, 2),
        "fairShare": round(fair_share, 2),
        "count": count,
        "balances": balances
    }


def compute_settlement(trip):

    summary = calc_summary(trip)

    creditors = []
    debtors = []

    for balance in summary['balances']:

        if balance['balance'] > 0:
            creditors.append({
                "name": balance['name'],
                "amount": balance['balance']
            })

        elif balance['balance'] < 0:
            debtors.append({
                "name": balance['name'],
                "amount": abs(balance['balance'])
            })

    transactions = []

    i = 0
    j = 0

    while i < len(creditors) and j < len(debtors):

        creditor = creditors[i]
        debtor = debtors[j]

        amount = min(creditor['amount'], debtor['amount'])

        transactions.append({
            "from": debtor['name'],
            "to": creditor['name'],
            "amount": round(amount, 2)
        })

        creditor['amount'] -= amount
        debtor['amount'] -= amount

        if creditor['amount'] < 0.01:
            i += 1

        if debtor['amount'] < 0.01:
            j += 1

    return transactions


# -----------------------------
# Routes
# -----------------------------

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/trip', methods=['GET'])
def get_trip():
    return jsonify(current_trip)


@app.route('/api/create_trip', methods=['POST'])
def create_trip():

    data = request.get_json()

    name = data.get('name')
    members = data.get('members')

    if not name or len(members) < 2:
        return jsonify({
            "ok": False,
            "error": "Invalid trip data"
        }), 400

    current_trip['name'] = name
    current_trip['members'] = members
    current_trip['expenses'] = []

    return jsonify({
        "ok": True
    })


@app.route('/api/add_expense', methods=['POST'])
def add_expense():

    data = request.get_json()

    payer = data.get('payer')
    amount = float(data.get('amount'))
    description = data.get('description')

    expense = {
        "id": int(datetime.utcnow().timestamp() * 1000),
        "payer": payer,
        "amount": amount,
        "description": description,
        "date": datetime.now().strftime('%Y-%m-%d')
    }

    current_trip['expenses'].append(expense)

    return jsonify({
        "ok": True
    })


@app.route('/api/calc', methods=['GET'])
def calculations():

    summary = calc_summary(current_trip)

    return jsonify({
        "name": current_trip['name'],
        "total": summary['total'],
        "fairShare": summary['fairShare'],
        "count": summary['count'],
        "balances": summary['balances']
    })


@app.route('/api/settlement', methods=['GET'])
def settlement():

    transactions = compute_settlement(current_trip)

    return jsonify({
        "name": current_trip['name'],
        "transactions": transactions
    })


@app.route('/api/reset', methods=['POST'])
def reset_trip():

    current_trip['name'] = ""
    current_trip['members'] = []
    current_trip['expenses'] = []

    return jsonify({
        "ok": True
    })


# -----------------------------
# Run Application
# -----------------------------

if __name__ == '__main__':
    app.run(debug=True)