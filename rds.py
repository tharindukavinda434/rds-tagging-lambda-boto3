import json
import boto3
from  pprint import pprint

def lambda_handler(event, context):
  
  regions = ["eu-west-1","eu-west-2","us-east-1","us-east-2"]
  #remove ,"us-east-2" when in LE accounts
  
  tagged_now = 0
  cant_tag   = 0
  alrdy_tagged =0
  all_rds_count = 0
  
  for region in regions:
    
    rds_client = boto3.client('rds',region_name=region)
    paginator = rds_client.get_paginator('describe_db_instances')
    
    response_iterator = paginator.paginate()
    
    for page in response_iterator:
      for i in page['DBInstances']:
        all_rds_count += 1
        rds_arn = i['DBInstanceArn']
        
        
        response = rds_client.list_tags_for_resource(ResourceName=rds_arn)
        flag =0
        for tag in response['TagList']:
          if ( tag['Key'] == 'abcd'  ):
            flag =1
            alrdy_tagged += 1
            
        if ( flag == 0  ):
          
          
          try:
    
            response = rds_client.add_tags_to_resource(
            ResourceName=rds_arn,
            Tags=[
            {
              'Key': 'abcd',
              'Value': 'abcd'
            }])
            
            tagged_now += 1
            
            
          except Exception as e:
            print( e)
            cant_tag += 1
            
  print('all rds count',all_rds_count)
  print('already tagged count' ,alrdy_tagged )
  print('tagged from this attempt',tagged_now)
  print('refused to tag',cant_tag )