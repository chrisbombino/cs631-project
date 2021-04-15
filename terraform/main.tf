provider "aws" {
  region = "us-east-2"
  access_key = var.access_key
  secret_key = var.secret_key
}

resource "aws_security_group" "cs631" {
  name = "cs631"
  description = "Allow SSH access and traffic to port 5601 for Kibana"

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 5601
    to_port = 5601
    protocol = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }


}

resource "aws_instance" "server" {
  ami = data.aws_ami.cs631.id
  instance_type = "t2.large"

  key_name = "cs631-project"
  security_groups = ["cs631"]

  user_data = "${file("init.sh")}"

  tags = {
    Name = "cs631"
  }
}

output "instance_ip" {
  value = aws_instance.server.public_ip
}
