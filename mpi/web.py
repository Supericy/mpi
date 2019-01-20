import bootstrap
import os
from auction import Filesystem, Subscription, SubscriptionNormalizer
from flask import Flask, request, jsonify

app = Flask(__name__)


def template(template):
    storage = os.path.dirname(os.path.realpath(__file__))
    return Filesystem.get(f'{storage}/templates/{template}')


@app.route('/')
def index():
    return template('index.vue')


@app.route('/api/v1/subscriptions', methods=['GET', 'POST'])
def api_v1_subscriptions():
    if request.method == 'POST':
        search = {}

        if 'searchMinimumYear' in request.json and request.json['searchMinimumYear']:
            search['year'] = {'minimum': request.json['searchMinimumYear']}

        if 'searchModel' in request.json and request.json['searchModel']:
            search['model'] = request.json['searchModel']

        subscription = bootstrap.auctions.subscribe(Subscription(
            request.json['email'],
            search
        ))
        return jsonify({
            'subscription': SubscriptionNormalizer.normalize(subscription)
        })
    else:
        normalized = []

        for subscription in bootstrap.auctions.subscriptions():
            normalized.append(SubscriptionNormalizer.normalize(subscription))

        return jsonify({
            'subscriptions': normalized
        })
