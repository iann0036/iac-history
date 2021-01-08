import os
import pprint
import csv
import re
import json
from datetime import datetime

# TF

tftypes = []
with open('./tftypes.txt') as f:
    for line in f.read().split("\n"):
        tftypes.append(line)

tfh = ''
with open('./tfhistory.txt') as f:
    tfh = f.read().split("\n")

tfresources = []
versiondate = ""

for line in tfh:
    if line.startswith('##'):
        versiondate = line[2:].strip()
    elif 'New Resource' in line:
        tfresources.append({
            'version': versiondate.split(" ")[0],
            'date': versiondate[ versiondate.index("(")+1 : versiondate.index(")") ],
            'type': line[ line.index("`")+1 : line.index("`", line.index("`")+1) ]
        })

for tftype in tftypes:
    found = False
    for tfresource in tfresources:
        if tfresource['type'] == tftype:
            found = True
            break
    
    if not found:
        tfresources.insert(0, {
            'version': "0.1.0",
            'date': "June 20, 2017",
            'type': tftype
        })

# CFN

cfntypes = []
with open('./cfntypes.txt') as f:
    for line in f.read().split("\n"):
        cfntypes.append(line)

last_date = ''
cfnresources = [
    ## Undocumented
    {"type": "AWS::CloudFormation::WaitCondition", "date": "November 6, 2014"},
    {"type": "AWS::CloudFormation::WaitConditionHandle", "date": "November 6, 2014"},
    {"type": "AWS::DataBrew::Dataset", "date": "November 12, 2020"},
    {"type": "AWS::DataBrew::Job", "date": "November 12, 2020"},
    {"type": "AWS::DataBrew::Project", "date": "November 12, 2020"},
    {"type": "AWS::DataBrew::Recipe", "date": "November 12, 2020"},
    {"type": "AWS::DataBrew::Schedule", "date": "November 12, 2020"},
    {"type": "AWS::ElastiCache::ParameterGroup", "date": "February 25, 2011"},
    {"type": "AWS::ElastiCache::SecurityGroup", "date": "February 25, 2011"},
    {"type": "AWS::ElastiCache::SecurityGroupIngress", "date": "February 25, 2011"},
    {"type": "AWS::IAM::AccessKey", "date": "February 25, 2011"},
    {"type": "AWS::IAM::Policy", "date": "February 25, 2011"},
    {"type": "AWS::IAM::UserToGroupAddition", "date": "February 25, 2011"},
    {"type": "Alexa::ASK::Skill", "date": "November 20, 2018"},
    {"type": "AWS::SDB::Domain", "date": "February 25, 2011"},
    {"type": "AWS::Kendra::Faq", "date": "September 10, 2020"},
    {"type": "AWS::Kendra::Index", "date": "September 10, 2020"},
    {"type": "AWS::SQS::Queue", "date": "February 25, 2011"},
    {"type": "AWS::SQS::QueuePolicy", "date": "February 25, 2011"},
    {"type": "AWS::Signer::ProfilePermission", "date": "November 23, 2020"},
    {"type": "AWS::Signer::SigningProfile", "date": "November 23, 2020"},
    {"type": "AWS::SageMaker::Project", "date": "May 31, 2018"},
    {"type": "AWS::SageMaker::Workteam", "date": "May 31, 2018"},
    {"type": "AWS::IoTWireless::Destination", "date": "December 18, 2020"},
    {"type": "AWS::IoTWireless::DeviceProfile", "date": "December 18, 2020"},
    {"type": "AWS::IoTWireless::ServiceProfile", "date": "December 18, 2020"},
    {"type": "AWS::IoTWireless::WirelessDevice", "date": "December 18, 2020"},
    {"type": "AWS::IoTWireless::WirelessGateway", "date": "December 18, 2020"},
    {"type": "AWS::EC2::NetworkInterfaceAttachment", "date": "February 25, 2011"},
    {"type": "AWS::EC2::SubnetNetworkAclAssociation", "date": "February 25, 2011"},
    {"type": "AWS::EC2::SubnetRouteTableAssociation", "date": "February 25, 2011"},
    {"type": "AWS::EC2::VPCDHCPOptionsAssociation", "date": "February 25, 2011"},
    {"type": "AWS::EC2::VPCGatewayAttachment", "date": "February 25, 2011"},
    {"type": "AWS::EC2::VolumeAttachment", "date": "February 25, 2011"},
    {"type": "AWS::EMR::InstanceFleetConfig", "date": "February 26, 2016"},
    {"type": "AWS::OpsWorks::ElasticLoadBalancerAttachment", "date": "March 3, 2014"},
    {"type": "AWS::WAFv2::IPSet", "date": "November 25, 2019"},
    {"type": "AWS::WAFv2::RegexPatternSet", "date": "November 25, 2019"},
    {"type": "AWS::IoT::Authorizer", "date": "July 20, 2016"},
    {"type": "AWS::IoT::ProvisioningTemplate", "date": "July 20, 2016"},
    {"type": "AWS::IoTSiteWise::Dashboard", "date": "October 28, 2020"},
    {"type": "AWS::MWAA::Environment", "date": "December 21, 2020"},
    {"type": "AWS::RDS::DBParameterGroup", "date": "February 25, 2011"},
    {"type": "AWS::CloudFormation::Stack", "date": "February 25, 2011"},
    {"type": "AWS::CloudWatch::MetricStream", "date": "December 18, 2020"},
    {"type": "AWS::Redshift::ClusterSecurityGroupIngress", "date": "February 10, 2014"},
    {"type": "AWS::Timestream::Database", "date": "October 6, 2020"},
    {"type": "AWS::Timestream::Table", "date": "October 6, 2020"},
    ## Initial spec
    {"type": "AWS::Route53::RecordSet", "date": "February 25, 2011"},
    {"type": "AWS::OpsWorks::Volume", "date": "February 25, 2011"},
    {"type": "AWS::SNS::Topic", "date": "February 25, 2011"},
    {"type": "AWS::KinesisFirehose::DeliveryStream", "date": "February 25, 2011"},
    {"type": "AWS::ECR::Repository", "date": "February 25, 2011"},
    {"type": "AWS::IAM::InstanceProfile", "date": "February 25, 2011"},
    {"type": "AWS::EC2::VPNConnection", "date": "February 25, 2011"},
    {"type": "AWS::Redshift::ClusterSecurityGroup", "date": "February 25, 2011"},
    {"type": "AWS::Redshift::ClusterParameterGroup", "date": "February 25, 2011"},
    {"type": "AWS::Events::Rule", "date": "February 25, 2011"},
    {"type": "AWS::Redshift::ClusterSubnetGroup", "date": "February 25, 2011"},
    {"type": "AWS::CloudWatch::Alarm", "date": "February 25, 2011"},
    {"type": "AWS::CertificateManager::Certificate", "date": "February 25, 2011"},
    {"type": "AWS::EC2::Route", "date": "February 25, 2011"},
    {"type": "AWS::EC2::FlowLog", "date": "February 25, 2011"},
    {"type": "AWS::ElasticBeanstalk::Application", "date": "February 25, 2011"},
    {"type": "AWS::Redshift::ClusterSecurityGroup", "date": "February 25, 2011"},
    {"type": "AWS::Redshift::ClusterParameterGroup", "date": "February 25, 2011"}
]
seen_types = []
for cfnresource in cfnresources:
    seen_types.append(cfnresource['type'])

cfnh = ''
with open('./cfnhistory.csv', newline='') as f:
    cfnh = csv.reader(f, delimiter=',', quotechar='"')

    for row in reversed(list(cfnh)):
        last_date = row[2]
        matches = re.findall(r"AWS\:\:\w+\:\:\w+", row[1])

        for match in matches:
            if match not in seen_types and match in cfntypes:
                cfnresources.append({
                    'date': last_date,
                    'type': match
                })
                seen_types.append(match)

                if last_date == "November 22, 2016":
                    with open('./spec1.json') as f:
                        spec1 = json.loads(f.read())
                        specres = list(spec1['ResourceTypes'].keys())
                        for res in specres:
                            found = False
                            for cfnresource in cfnresources:
                                if cfnresource['type'] == res:
                                    found = True
                                    break
                            if not found:
                                print('    {"type": "' + res + '", "date": "February 25, 2011"},')

pprint.pprint(cfntypes)

for cfntype in cfntypes:
    found = False
    for cfnresource in cfnresources:
        if cfnresource['type'] == cfntype:
            found = True
            break
    
    if not found:
        print(cfntype + " not found")

# Output

ldate = ''
count = 0
cfnresources.sort(key=lambda x: datetime.strptime(x['date'], '%B %d, %Y').timestamp())

for cfnresource in cfnresources:
    cdate = datetime.strptime(cfnresource['date'], '%B %d, %Y').strftime("%Y-%m-%d")
    if cdate != ldate:
        if ldate != '':
            print(str(count) + "," + ldate)
        ldate = cdate
    count += 1
print(str(count) + "," + ldate)

print("---")

ldate = ''
count = 0
tfresources.sort(key=lambda x: datetime.strptime(x['date'], '%B %d, %Y').timestamp())

for tfresource in tfresources:
    cdate = datetime.strptime(tfresource['date'], '%B %d, %Y').strftime("%Y-%m-%d")
    if cdate != ldate:
        if ldate != '':
            print(str(count) + "," + ldate)
        ldate = cdate
    count += 1
print(str(count) + "," + ldate)
