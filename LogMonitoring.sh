#!/bin/bash

if [[ ! -f "/root/amazon-cloudwatch-agent.rpm" ]]; then
echo "[INFO]: Going to install aws cloudwatch agent"
cd  /root
git clone https://github.com/am2308/Dashboard.git
wget https://s3.amazonaws.com/amazoncloudwatch-agent/centos/amd64/latest/amazon-cloudwatch-agent.rpm
rpm -U ./amazon-cloudwatch-agent.rpm
cp /root/Dashboard/config.json /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.d/default
systemctl start amazon-cloudwatch-agent.service
systemctl enable amazon-cloudwatch-agent.service
else
echo "[INFO]: AWS Cloudwatch agent already installed"
fi
