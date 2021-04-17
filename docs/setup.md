# AWS AMI Configuration
The configuration of the server is being done on a custom AMI that was made from a basic Amazon Linux 2 image. The AMI configuration can be replicated based on the following steps:

All commands are run as default ec2-user

### Dependencies
`sudo yum update -y`

`sudo yum install git -y`

`sudo python3 -m pip install --upgrade pip`


## Kafka
Download JRE

`sudo amazon-linux-extras install java-openjdk11 -y`

Download kafka

`wget https://mirror.its.dal.ca/apache/kafka/2.7.0/kafka_2.13-2.7.0.tgz`

Extract tarball

`tar -xvf kafka_2.13-2.7.0.tgz && mv kafka_2.13-2.7.0 /home/ec2-user/kafka && rm -f kafka_2.13-2.7.0.tgz && cd /home/ec2-user/kafka`

Place zookeeper.service and kafka.service inside `/etc/systemd/system/` directory (see this [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-ubuntu-18-04) article for more details)

`sudo systemctl enable kafka`


## Elasticsearch & Kibana

Install Elasticsearch package

`sudo rpm -i https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.12.0-x86_64.rpm`

`sudo systemctl enable elasticsearch`

Install Kibana

`sudo rpm -i https://artifacts.elastic.co/downloads/kibana/kibana-7.12.0-x86_64.rpm`

`sudo systemctl enable kibana`

Set the following in `/etc/kibana/kibana.yml`

`server.port: 5601`

`server.host: "0.0.0.0"`

`elasticsearch.hosts: ["http://localhost:9200"]`
