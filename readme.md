# Twitter Sentiment Analyzer

## Project Description
The full scope of this project is to have an app that streams the trends of Twitter using a sentiment analyzer. 



## How It Works
Currently this project uses Twitter OAuth to log a user into the application. The user can then enter a word or phrase into a search box which searches Twitter using the word or phrase. Text from tweets are analyzed using a sentiment analyzer API. Tweets are displayed and color coded based on their sentiment.

![](twitter_sentiment_analyzer_app.gif)




## Vision for Project
- Pull Tweets, write to S3, schedule with Airflow.
- Upon completion, enrich data with sentiment analyzer (will brainstorm other ways to add on to Twitter trends; news tracker?), write results to a database (determine schema).
- Make a view on that table in the database and display a dashboard of sentiment trends over various periods of time.

## Technologies
- Python
- Flask
- S3
- PostgreSQL
- Airflow as a Lambda Function
- Twitter API
- Sentiment Analyzer API
- Dash (Dashboard framework)

