import bootstrap
import os
from flask import Flask, request, jsonify
from auction import (
    Filesystem,
    Subscription,
    SubscriptionNormalizer,
    SubscriptionExists,
    SubscriptionMaximumReached
)

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
        try:
            search = {}

            if 'searchMinimumYear' in request.json and request.json['searchMinimumYear']:
                if len(request.json['searchMinimumYear']) > 100:
                    raise Exception("Search minimum year must be less than 100 characters.")

                search['year'] = {'minimum': request.json['searchMinimumYear']}

            if 'searchModel' in request.json and request.json['searchModel']:
                if len(request.json['searchModel']) > 100:
                    raise Exception("Search model must be less than 100 characters.")

                search['model'] = request.json['searchModel']

            subscription = bootstrap.auctions.subscribe(Subscription(
                request.json['email'],
                search
            ))
            return jsonify({
                'subscription': SubscriptionNormalizer.normalize(subscription)
            })
        except Exception as exception:
            return jsonify({
                'error': {
                    'type': exception.__class__.__name__,
                    'message': str(exception)
                }
            })
    else:
        normalized = []

        for subscription in bootstrap.auctions.subscriptions():
            normalized.append(SubscriptionNormalizer.normalize(subscription))

        return jsonify({
            'subscriptions': normalized
        })


if __name__ == "__main__":
    app.run()

