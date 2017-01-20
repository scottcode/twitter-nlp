#Twitter NLP
Twitter NLP is a microservice-based web application for analyzing Twitter sentiment in real time. The goal of the project is to show how to deploy a machine learning model, apply it in real time, and scale the model.

Check out this [blog post](https://blog.pivotal.io/data-science-pivotal/p-o-v/how-to-scaling-a-machine-learning-model-using-pivotal-cloud-foundry) for more information.

Try the application: [Twitter NLP](http://twitternlp.cfapps.pez.pivotal.io/)

## Architecture

![Alt text](/readme/architecture.png?raw=true "architecture")

Dashboard information:

* Server Side: Python + Flask + SSE
* Client Side: D3 for visualization and Server Sent Events (SSE) for real-time data streaming

## Microservices

* compute-tweet-stats: flask app for computing sentiment analysis stats (tweets/second and avg. sentiment)
* firehose: connects to Twitter firehose and publishes Tweets to redis for the dashboard
* gen-tweet-stats: gets the performance statistics generated from "compute-tweet-stats"
* load-test-twitter-nlp: a load testing application for scale testing
* sentiment-compute-app: [sentiment analysis model](https://github.com/crawles/gpdb_sentiment_analysis_twitter_model) accessible via a RESTful API
* twitter-nlp: the dashboard

## Deploying the app on Pivotal Cloud Foundry
Step 1<br> 
* Rename manifest.example.yml to manifest.yml
* In manifest.yml replace both \*URL for compute-tweet-stats\* and \*URL for sentiment-compute-app\* with appropriate URLs

Step 2<br>
* Add your Twitter credentials to CF environmental variables
```
cf set-env APP_NAME ACCESS_TOKEN ENV_VAR_VALUE
cf set-env firehose ACCESS_TOKEN_SECRET ENV_VAR_VALUE
cf set-env firehose CONSUMER_KEY ENV_VAR_VALUE
cf set-env firehose CONSUMER_SECRET ENV_VAR_VALUE
```

Step 3
```
cf create-service p-redis shared-vm twitter-nlp-redis
cf push
```

## Notes

The project was inspired in part by [BirdWatch](https://github.com/matthiasn/BirdWatch)
