# CS 631 Course Project
### University of Waterloo W2021

#### Overview

The goal of this project is to analyze the sentiment towards a number of companies using both historical and real time tweets. The data will be analyzed in a Kibana dashboard.


## Temp Notes


0. create account on twitter and apply for developer account. fill in application. approved within seconds. get keys (more on this later)

  a. create app in https://developer.twitter.com/en/portal/projects-and-apps
  b. Go to the app > keys and tokens

generate and copy:

- CONSUMER_KEY

- CONSUMER_SECRET

- ACCESS_TOKEN

- ACCESS_SECRET


1. download JRE to run java programs (zookeeper). JRE developed by Oracle.

https://www.oracle.com/ca-en/java/technologies/javase-jre8-downloads.html


jre-8u281-windows-x64.exe

installation path:
C:\Program Files\Java\jre1.8.0_281

2. download zookeeper

https://zookeeper.apache.org/releases.html#download


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
