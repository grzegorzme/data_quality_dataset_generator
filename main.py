import numpy as np
import datetime
import json
import random
from flask import Flask, jsonify, render_template


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/data')
def generate_dataset(n=100):
    # id
    id_ = list(range(n))
    invalid_ids = np.random.choice(list(range(n)), size=3, replace=False)
    id_[invalid_ids[0]] = id_[invalid_ids[1]]
    id_[invalid_ids[2]] = None

    # date
    startdate = datetime.date(2000, 1, 1)
    nbdays = (datetime.date.today() - startdate).days
    date_ = [(startdate + datetime.timedelta(days=np.random.randint(0, nbdays))).strftime('%Y-%m-%d') for _ in range(n)]

    invalid_ids = np.random.choice(list(range(n)), size=random.randint(2, 5), replace=False)
    date_[invalid_ids[0]] = '9999-01-01'
    for ii in invalid_ids[1:]:
        date_[ii] = (startdate + datetime.timedelta(days=np.random.randint(0, nbdays))).strftime('%d-%B-%y')

    # view count
    view_count_ = []
    view_count_split_ = []
    for i in range(n):
        view_count_list = list(int(x) for x in np.random.randint(1, 100, 5))
        view_count_by_category_json = {'category_{}'.format(c): k for c, k in enumerate(view_count_list)}
        view_count_.append(sum(view_count_list))
        view_count_split_.append(json.dumps(view_count_by_category_json))

    invalid_ids = np.random.choice(list(range(n)), size=random.randint(4, 7), replace=False)

    view_count_split_[invalid_ids[0]] = view_count_split_[invalid_ids[0]][:-1]
    view_count_split_[invalid_ids[1]] = view_count_split_[invalid_ids[1]].replace('\"', '\'')
    view_count_[invalid_ids[2]] *= -1
    for ii in invalid_ids[3:]:
        view_count_[ii] += random.randint(1, 10)

    return jsonify([{
        'id': a,
        'date': b,
        'view_count': c,
        'view_count_by_category': d
    } for a, b, c, d in zip(id_, date_, view_count_, view_count_split_)])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
