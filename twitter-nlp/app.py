"""
twitter nlp
~~~~~~~~~~~

Serves the web application and sends tweets and tweet data using Server Side Events (SSE)

"""

import json
import os
import time

import redis
from flask import Flask, request, Response, render_template, jsonify
from gevent import monkey, sleep, socket
from gevent.pywsgi import WSGIServer

import helper_functions

monkey.patch_all()

app = Flask(__name__)
redis.connection.socket = socket

# connect to redis for storing logging info
r = helper_functions.connect_redis_db()

# twitter compute and stats URL, from manifest
SENTIMENT_COMPUTE_URL=os.getenv('SENTIMENT_COMPUTE_URL',None)
SENTIMENT_STATS_URL=os.getenv('SENTIMENT_STATS_URL',None)

def gen_dashboard_tweets():
    n = 5  # min number of seconds between each tweet
    pubsub = r.pubsub()
    pubsub.subscribe('tweet_msgs')
    for message in pubsub.listen():
        is_a_tweet = message['type'] == 'message'
        is_tweet_message = message['channel'] == 'tweet_msgs'
        if not is_a_tweet or not is_tweet_message:
            continue
        msg = json.loads(message['data'])
        tweet_sent = {"data": json.dumps({"tweet": msg['text'],
                                          "polarity": '{:1.2f}'.format(msg['polarity'])})}
        yield (helper_functions.sse_pack(tweet_sent))
        sleep(n-2) # new tweet won't get published for n seconds, let python rest


def get_tweet_stats():
    pubsub = r.pubsub()
    pubsub.subscribe('tweet_stats')
    for message in pubsub.listen():
        time_start = time.time()
        is_a_tweet = message['type'] == 'message'
        is_a_tweet_stat = message['channel'] == 'tweet_stats'
        if not is_a_tweet or not is_a_tweet_stat:
            continue
        tweet_stats = json.loads(message['data'])
        time_start = time.time()
        yield helper_functions.sse_pack({"data": json.dumps({"tweetRate": tweet_stats['tweet_rate'],
                                                             "avgPolarity": tweet_stats['avg_polarity']})})

@app.route('/live_tweets')
def live_tweets_sse():
    return Response(gen_dashboard_tweets(),mimetype='text/event-stream')

@app.route('/tweet_rate')
def tweet_rate_sse():
    return Response(get_tweet_stats(),mimetype='text/event-stream')

@app.route('/')
def page():
    return render_template('index.html',
                           SENTIMENT_COMPUTE_URL = SENTIMENT_COMPUTE_URL,
                           SENTIMENT_STATS_URL = SENTIMENT_STATS_URL)

@app.route('/rate')
def rate_tweets():
    cur_tweet = r.lrange('training_backlog',0,0)[0]
    cur_tweet_escaped = cur_tweet.replace('\\', '\\\\')
    return render_template('rate.html',
                           curTweet = cur_tweet_escaped)

@app.route('/collect_tweet', methods=['POST'])
def collect_tweet():
    # print request.data
    # print type(request.data)
    r.lpush('labeled_tweets', request.data)
    return '{"success": true}'

@app.route('/next_tweet_to_label', methods=['GET'])
def next_tweet_to_label():
    r.lpop('training_backlog')
    cur_tweet = r.lrange('training_backlog',0,0)[0]
    cur_tweet_escaped = json.loads(cur_tweet)
    return jsonify({"tweet": cur_tweet_escaped})


@app.route('/redis_info', methods=['GET'])
def redis_info():
    return jsonify({
        "info_time": time.strftime('%c', time.gmtime()),
        "redis_info": r.info()
    })


@app.route('/redis_list_len', methods=['GET'])
def redis_list_len():
    listname = request.args.get('list')
    if listname is not None:
        return jsonify({
            "listname": listname,
            "length": r.llen(listname)
        })
    else:
        return jsonify({
            "listname": "",
            "length": 0
        })



if __name__ == '__main__':
    if os.environ.get('VCAP_SERVICES') is None: # running locally
        PORT = 5001
        app.debug = True
    else:                                       # running on CF
        PORT = int(os.getenv("PORT"))
    http_server = WSGIServer(('0.0.0.0',PORT), app)
    http_server.serve_forever()