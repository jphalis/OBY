import os.path

fabconf = {}

#  Do not edit
fabconf['FAB_CONFIG_PATH'] = os.path.dirname(__file__)

# Project name
fabconf['PROJECT_NAME'] = "oby"

# Username for connecting to EC2 instaces - Do not edit
# unless you have a reason to
fabconf['SERVER_USERNAME'] = "ubuntu"

# Full local path for .ssh
fabconf['SSH_PATH'] = "~/.ssh"

# Name of the private key file you use to connect to EC2 instances
fabconf['EC2_KEY_NAME'] = "oby_key_pair.pem"

# Don't edit. Full path of the ssh key you use to connect to EC2 instances
fabconf['SSH_PRIVATE_KEY_PATH'] = '{}/{}'.format(
    fabconf['SSH_PATH'], fabconf['EC2_KEY_NAME'])

# Where to install apps
fabconf['APPS_DIR'] = "/home/{}/obystudio.com".format(
    fabconf['SERVER_USERNAME'])

# Where you want your project installed: /APPS_DIR/PROJECT_NAME
fabconf['PROJECT_PATH'] = "{}/{}".format(
    fabconf['APPS_DIR'], fabconf['PROJECT_NAME'])

# App domains
fabconf['DOMAINS'] = "obystudio.com www.obystudio.com *.obystudio.com"

# Path for virtualenvs
fabconf['VIRTUALENV_DIR'] = "/home/{}/.virtualenvs".format(
    fabconf['SERVER_USERNAME'])

# Email for the server admin
fabconf['ADMIN_EMAIL'] = "halis@obystudio.com"

# Git username for the server
fabconf['GIT_USERNAME'] = "OBY"

# Name of the private key file used for github deployments
fabconf['BITBUCKET_DEPLOY_KEY_NAME'] = "id_rsa"

# Don't edit. Local path for deployment key you use for github
fabconf['BITBUCKET_DEPLOY_KEY_PATH'] = "{}/{}".format(
    fabconf['SSH_PATH'], fabconf['BITBUCKET_DEPLOY_KEY_NAME'])

# Path to the repo of the application you want to install
fabconf['BITBUCKET_USERNAME'] = 'obystudio'
fabconf['BITBUCKET_REPO_NAME'] = 'oby'

# Creates the ssh location of your bitbucket repo from the above details
fabconf['BITBUCKET_REPO'] = "ssh://git@bitbucket.org/{}/{}.git".format(
    fabconf['BITBUCKET_USERNAME'], fabconf['BITBUCKET_REPO_NAME'])

# Virtualenv activate command
fabconf['ACTIVATE'] = "source /home/{}/.virtualenvs/{}/bin/activate".format(
    fabconf['SERVER_USERNAME'], fabconf['PROJECT_NAME'])

# Name tag for your server instance on EC2
fabconf['INSTANCE_NAME_TAG'] = "OBYInstance"

# EC2 key. http://bit.ly/j5ImEZ
fabconf['AWS_ACCESS_KEY'] = 'AKIAJS5O4GAHA4MJH4NA'

# EC2 secret. http://bit.ly/j5ImEZ
fabconf['AWS_SECRET_KEY'] = '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'

# EC2 region. http://amzn.to/12jBkm7
ec2_region = 'us-east-1'

# AMI ID. http://bit.ly/liLKxj
ec2_amis = ['ami-d05e75b8']

# Name of the keypair you use in EC2. http://bit.ly/ldw0HZ
ec2_keypair = 'oby_key_pair'

# Name of the security group. http://bit.ly/kl0Jyn
ec2_secgroups = ['ObySecurityGroup']

# API Name of instance type. http://bit.ly/mkWvpn
ec2_instancetype = 't2.micro'

# Existing instances - add the public dns of your instances here
# If you are using an Elastic IP, add that instead
fabconf['EC2_INSTANCES'] = ["ec2-54-86-53-126.compute-1.amazonaws.com"]

# Spawn a new instance
# fab spawn instance

# Update git files
# fab deploy
# fab update_packages
# fab reload_nginx
# fab reload_supervisor
# fab manage:command="some command"
