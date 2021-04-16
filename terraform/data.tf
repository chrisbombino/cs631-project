data "aws_ami" "cs631" {
  most_recent = true

  filter {
    name   = "name"
    values = ["cs631-project"]
  }

  owners = ["601626918072"] # Canonical
}
