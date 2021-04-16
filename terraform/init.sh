#! /bin/bash -xe
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
/home/ec2-user/kafka/bin/kafka-topics.sh --create --topic tweets --bootstrap-server localhost:9092
/home/ec2-user/kafka/bin/kafka-topics.sh --create --topic processed_tweets --bootstrap-server localhost:9092
git clone https://github.com/chrisbombino/cs631-project.git /home/ec2-user/cs631-project
python3 -m pip install -r /home/ec2-user/cs631-project/scripts/requirements.txt
