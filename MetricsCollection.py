#!/bin/python
import os
import commands
import boto3
import time
TimeStamp = time.strftime("%Y-%m-%dT%H:%M:%SZ")



def PullMetricData():
        print ("[INFO]: Pulling data for metrics DiskSpace, MemoryUtilization, CPU-Utilization")
        status, DiskSpaceMount=commands.getstatusoutput("df -kh | grep 'dev' | head -1 | awk -F' ' '{print $5}' | tr -d [%]")
        PutMetricData('DiskSpaceUtilizationMount', DiskSpaceMount, 'DiskSpaceMount')
        status, DiskSpaceRoot=commands.getstatusoutput("df -kh | grep '/$' | awk -F' ' '{print $5}' | tr -d [%]")
        PutMetricData('DiskSpaceUtilizationRoot', DiskSpaceRoot, 'DiskSpaceRoot')

        status, MemFree=commands.getstatusoutput("cat /proc/meminfo | grep 'MemFree' | awk -F' ' '{print $2}'")
        status, Buffer=commands.getstatusoutput("cat /proc/meminfo | grep 'Buffers' | awk -F' ' '{print $2}'")
        status, Cache=commands.getstatusoutput("cat /proc/meminfo | grep '^Cached' | awk -F' ' '{print $2}'")
        status, MemTotal=commands.getstatusoutput("cat /proc/meminfo | grep 'MemTotal' | awk -F' ' '{print $2}'")
        MemAvail=int(MemFree)+int(Buffer)+int(Cache)
        MemUsed=int(MemTotal)-int(MemAvail)
        MemUtil=(MemUsed *100)/int(MemTotal)
        PutMetricData('MemoryUtilization', MemUtil, 'MemUtil')
        print (DiskSpaceMount, DiskSpaceRoot, MemFree, Buffer, Cache, MemTotal, MemUtil)

def PutMetricData(MetricName, Value, Dimension):
        print ("[INFO]: Going to create/put metrics - " + str(MetricName) + " data in cloudwatch")
        cloud = boto3.client('cloudwatch', region_name='us-east-1')
        response  = cloud.put_metric_data(
        Namespace='ServerMonitoring',
        MetricData=[
                {
                'MetricName': MetricName,
                'Dimensions': [
                        {
                        'Name': 'ComponentName',
                        'Value': Dimension
                        },
                ],
                'Timestamp': TimeStamp,
                'Value': int(Value),
                'Unit': 'Percent'
                },
        ]
        )

        if str(response['ResponseMetadata']['HTTPStatusCode']).startswith('20'):
                print ("[INFO]: " + str(MetricName) + " metrics data pushed successfully on cloudwatch")
        else:
                print ("[ERROR]: Error encountered while pushing data for metrics - " + str(MetricName) + " on cloudwatch")


def main():
        #Exexuting shell script to push Apache logs to cloudwatch
        os.system("sh /root/LogMonitoring.sh")
        PullMetricData()

if __name__ == '__main__':
        main()
