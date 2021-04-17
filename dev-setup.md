## Steps to Setup Development Environment

#### Twitter

1. Create account on Twitter and apply for developer account. fill in application. approved within seconds. get keys (more on this later)
2. Under Projects & Apps, create an app and copy the API keys that are generated
3. In the app, go to Keys and tokens and generate new Access Token and Secret

ENSURE YOU HAVE COPIED THE FOLLOWING:

- CONSUMER_KEY

- CONSUMER_SECRET

- ACCESS_TOKEN

- ACCESS_SECRET


#### Kafka

1. Download JRE to run java programs (zookeeper). JRE developed by Oracle: https://www.oracle.com/ca-en/java/technologies/javase-jre8-downloads.html


2. Download zookeeper: https://zookeeper.apache.org/releases.html#download


Apache ZooKeeper 3.7.0

for checksum: certUtil -hashfile path_to_file SHA512

Compare output with the one on downloads page

3. followed https://shaaslam.medium.com/installing-apache-zookeeper-on-windows-45eda303e835#.fgofwm6n6

but had errors:

a. ZOOKEEPER_HOME should be tools/zookeeper/zookeeper-{version_number} and not tools/zookeeper-{version_number}

NOTE: While specifying paths in config files, use double backslash \\ for windows. While specifying system variables and paths, just specify forward slash /.

b. JAVA_HOME is not set.

Next step is to set JAVA_HOME path variable in the user environment.
as specified earlier, installation path for JRE was:

C:\Program Files\Java\jre1.8.0_281


zkserver

4. finally, apache kafka:

https://www.apache.org/dyn/closer.cgi?path=/kafka/2.7.0/kafka_2.13-2.7.0.tgz

checksum using the same process

followed https://shaaslam.medium.com/installing-apache-kafka-on-windows-495f6f2fd3c8

but for consistency, just like zookeeper, I added a parent folder "kafka" to "kafka_2.13-2.7.0".

so my directory looks like:

tools
- kafka
-- kafka_2.13-2.7.0
- zookeeper
-- apache-zookeeper-3.7.0-bin

run .\bin\windows\kafka-server-start.bat .\config\server.properties

but if zookeeper not running, it will shut down automatically. so run zkserver in another CMD and try again.

5. create new empty conda environment

conda create -n cs631
conda activate cs631

Will pip freeze later but for now, new libraries installed were:

pip install tweepy
pip install kafka-python
conda install -c conda-forge kafka-python

6. kafka commands

first: zkserver

make sure to CD to the kafka root before runnign following commands:
start kafka: .\bin\windows\kafka-server-start.bat .\config\server.properties

.\bin\windows\kafka-topics.bat --describe --zookeeper localhost:2181 --topic test

.\bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic newapple --from-beginning

.\bin\windows\kafka-console-producer.bat --broker-list localhost:9092 --topic test

if it produces:

2021-04-06 16:44:03,412] WARN [Producer clientId=console-producer] Bootstrap broker localhost:9092 (id: -1 rack: null) disconnected (org.apache.kafka.clients.NetworkClient)

then I pressed enter in the console running kafka cluster. not sure why I had to do that. but the producer started working after that.

.\bin\windows\kafka-topics.bat --list --zookeeper localhost:2181

.\bin\windows\kafka-topics.bat --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

### Model

== twitter sentiment prediction

== 3 categories: 0 = negative, 1 = neutral, 2 = positive

1. packages

    To load the model, remember to have keras and tf in your machine.

    Simply `pip install keras` and `pip install tensorflow` would be okay.

    Mine: Keras 2.2.5, tensorflow2.4.1

    Please install nltk in advance.

2. dataset

    It is hard to find a perfect dataset containing all 3 categories (most datasets only contain 2 categories: positive and negative and not big enough). If we only use one dataset to train, the model will perform badly on other datasets and therefore lack generalization.

    So we merge several datasets into one, select the data and keep the count of 3 catogories almost equal, and shuffle the data. Finally a dataset containing about 60,000 tweets are formed.

    Dataset we use:
    - Twitter US Airline Sentiment [https://www.kaggle.com/crowdflower/twitter-airline-sentiment](https://www.kaggle.com/crowdflower/twitter-airline-sentiment)
    - Tweet Sentiment Extraction https://www.kaggle.com/c/tweet-sentiment-extraction/data
    - Preprocessed twitter tweets https://www.kaggle.com/shashank1558/preprocessed-twitter-tweets
    - Apple Twitter sentiment https://data.world/crowdflower/apple-twitter-sentiment/discuss/apple-twitter-sentiment/miztcmjq#mjczxd3y
    - Sentiment 140 http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip

3. training

    We have tried CNN, LSTM and Bi-LSTM to train the sentiment analysis model. Among them, Bi-LSTM is the best method we have tried. For details, see model/twitter_sentiment_training_bilstm.ipynb

    The accuracy on test dataset is about 0.71. The model performed well in classifying + and -. Most confusion is between neutruality and other 2 categories.  

4. pyspark training

    Load the data as a rdd and fit the data into a keras model using pyspark and elephas.

    The drawback of this pyspark method is that we can only save the fitted pipeline, not the model. It is not convenient for our project. Also the prediction process is slower than general model. So for now we did not use this pyspark method.

    In summary, this is an innovative and useful method. It is worthy to explore more in future.

    For details, see model/pyspark.ml/pyspark_elephas_deep_learning_Demo.ipynb
