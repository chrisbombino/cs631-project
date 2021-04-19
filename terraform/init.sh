#! /bin/bash -xe
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
git clone https://github.com/chrisbombino/cs631-project.git /home/ec2-user/cs631-project
python3 -m pip install -r /home/ec2-user/cs631-project/scripts/requirements.txt
cd /home/ec2-user/cs631-project/scripts
nohup python3 /home/ec2-user/cs631-project/scripts/producer_twitter_streaming_api.py &
nohup python3 /home/ec2-user/cs631-project/scripts/consumer_sentiment_analyzer.py &
nohup python3 /home/ec2-user/cs631-project/scripts/consumer_elasticsearch.py &
