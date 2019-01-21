import bootstrap
import os
from flask import Flask, request, jsonify, url_for
from config import config
from auction import (
    Filesystem,
    Subscription,
    SubscriptionNormalizer
)


app = Flask(__name__)

#TODO: make this work behind reverse proxy
# app.config['SERVER_NAME'] = config['web']['base_uri']


def template(template):
    storage = os.path.dirname(os.path.realpath(__file__))
    return Filesystem.get(f'{storage}/templates/{template}')


@app.route('/')
def index():
    return template('index.vue')


@app.route('/api/v1/subscriptions/<subscriptionId>', methods=['DELETE'])
def api_v1_subscription_delete(subscriptionId):
    try:
        bootstrap.auctions.unsubscribe(subscriptionId)
        return jsonify({})
    except Exception as exception:
        return jsonify_exception(exception)


@app.route('/api/v1/subscriptions', methods=['GET'])
def api_v1_subscriptions_get():
    normalized = []

    for subscription in bootstrap.auctions.subscriptions():
        normalized.append(subscription_normalize_with_links(subscription))

    return jsonify({
        'subscriptions': normalized,
        '_links': {
            "self": {
                "href": url_for('api_v1_subscriptions_get')
            }
        }
    })


@app.route('/api/v1/subscriptions', methods=['POST'])
def api_v1_subscriptions_post():
    try:
        search = {}

        if 'searchMinimumYear' in request.json and request.json['searchMinimumYear']:
            if len(request.json['searchMinimumYear']) > 100:
                raise Exception("Search minimum year must be less than 100 characters.")

            search['year'] = {'minimum': request.json['searchMinimumYear']}

        if 'searchModel' in request.json and request.json['searchModel']:
            if len(request.json['searchModel']) > 100:
                raise Exception("Search model must be less than 100 characters.")

            search['model'] = request.json['searchModel'].lower()

        subscription = bootstrap.auctions.subscribe(Subscription(
            request.json['email'],
            search
        ))
        # TODO: Location header
        return jsonify({
            'subscription': subscription_normalize_with_links(subscription)
        }), 201
    except Exception as exception:
        return jsonify_exception(exception)


def subscription_normalize_with_links(subscription):
    normalized = SubscriptionNormalizer.normalize(subscription)
    normalized['_links'] = {
        "self": {
            "href": url_for(
                'api_v1_subscription_delete',
                subscriptionId=subscription.subscriptionId
            )
        }
    }

    return normalized


def jsonify_exception(exception):
    return jsonify({
        'error': {
            'type': exception.__class__.__name__,
            'message': str(exception)
        }
    })


if __name__ == "__main__":
    app.run()

