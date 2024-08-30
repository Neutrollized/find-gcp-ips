import os
import pandas as pd
from tabulate import tabulate
from google.cloud import asset_v1

PROJECT_ID=os.environ['GCP_PROJECT']


def find_gcp_ips():
  df = pd.DataFrame(columns=['ASSET TYPE', 'DISPLAY NAME', 'LOCATION', 'IP ADDRESS(ES)']) 

  # create client
  client = asset_v1.AssetServiceClient()

  #-------------------------------------------------
  # RESERVED IPs + FORWARDING RULES 
  #-------------------------------------------------
  request = asset_v1.SearchAllResourcesRequest(
    scope="projects/" + PROJECT_ID,
    asset_types=[
      "compute.googleapis.com/Address",
      "compute.googleapis.com/ForwardingRule",
    ],
  )

  # make request
  page_result = client.search_all_resources(request=request)

  # handle response
  for response in page_result:
    try:
      df.loc[len(df)] = [response.asset_type, response.display_name, response.location, response.additional_attributes['IPAddress']]
    except KeyError:
      df.loc[len(df)] = [response.asset_type, response.display_name, response.location, response.additional_attributes['address']]


  #-------------------------------------------------
  # ALLOYDB
  #-------------------------------------------------
  request = asset_v1.SearchAllResourcesRequest(
    scope="projects/" + PROJECT_ID,
    asset_types=[
      "alloydb.googleapis.com/Instance",
    ],
  )

#  for response in client.search_all_resources(request=request):
#      print(response)


  #-------------------------------------------------
  # COMPUTE ENGINES (private + public)
  # - compute engines
  # - gke nodes
  # - dataproc master & workers
  #-------------------------------------------------
  request = asset_v1.SearchAllResourcesRequest(
    scope="projects/" + PROJECT_ID,
    asset_types=[
      "compute.googleapis.com/Instance",
    ],
  )

  for response in client.search_all_resources(request=request):
    try: 
      gce_int_ext_ips = response.additional_attributes['internalIPs'][0] + ', ' + response.additional_attributes['externalIPs'][0]
      df.loc[len(df)] = [response.asset_type, response.display_name, response.location, gce_int_ext_ips]
    except KeyError:
      df.loc[len(df)] = [response.asset_type, response.display_name, response.location, response.additional_attributes['internalIPs'][0]]


  #-------------------------------------------------
  # CLOUD DATA FUSION
  # instances are in a tenant project (external)
  #-------------------------------------------------
  request = asset_v1.SearchAllResourcesRequest(
    scope="projects/" + PROJECT_ID,
    asset_types=[
      "datafusion.googleapis.com/Instance",
    ],
  )

#  for response in client.search_all_resources(request=request):
#    print(response)


  #-------------------------------------------------
  # CLOUD SPANNER
  # does not show any assets (maybe becuase I provisioned a fractional instance?)
  #-------------------------------------------------
  request = asset_v1.SearchAllResourcesRequest(
    scope="projects/" + PROJECT_ID,
    asset_types=[
      "spanner.googleapis.com/Instance",
    ],
  )

#  for response in client.search_all_resources(request=request):
#    print(response)


  #-------------------------------------------------
  # CLOUD SQL
  # https://issuetracker.google.com/issues/207842547
  #-------------------------------------------------
  request = asset_v1.SearchAllResourcesRequest(
    scope="projects/" + PROJECT_ID,
    asset_types=[
      "sqladmin.googleapis.com/Instance",
    ],
  )

#  for response in client.search_all_resources(request=request):
#    print(response)


  #-------------------------------------------------
  # CLOUD TPU
  #-------------------------------------------------
  request = asset_v1.SearchAllResourcesRequest(
    scope="projects/" + PROJECT_ID,
    asset_types=[
      "tpu.googleapis.com/Node",
    ],
  )

  for response in client.search_all_resources(request=request):
    df.loc[len(df)] = [response.asset_type, response.display_name, response.location, response.additional_attributes['networkEndpoint'][0]['ipAddress']]


  #-------------------------------------------------
  # DATAPROC
  # only shows cluster status, nodes show up in compute engines
  #-------------------------------------------------
  request = asset_v1.SearchAllResourcesRequest(
    scope="projects/" + PROJECT_ID,
    asset_types=[
      "dataproc.googleapis.com/Cluster",
    ],
  )

#  for response in client.search_all_resources(request=request):
#      print(response)


  #-------------------------------------------------
  # FILESTORE
  #-------------------------------------------------
  request = asset_v1.SearchAllResourcesRequest(
    scope="projects/" + PROJECT_ID,
    asset_types=[
      "file.googleapis.com/Instance",
    ],
  )

  for response in client.search_all_resources(request=request):
    df.loc[len(df)] = [response.asset_type, response.display_name, response.location, response.additional_attributes['networks'][0]['ipAddresses'][0]]


  #-------------------------------------------------
  # GKE
  #-------------------------------------------------
  request = asset_v1.SearchAllResourcesRequest(
    scope="projects/" + PROJECT_ID,
    asset_types=[
      "container.googleapis.com/Cluster",
    ],
  )

  for response in client.search_all_resources(request=request):
    df.loc[len(df)] = [response.asset_type, response.display_name, response.location, response.additional_attributes['endpoint']]


  #-------------------------------------------------
  # MEMORYSTORE - REDIS
  # much like Cloud SQL, this doesn't return any IPs, even though it has an IP on VPC
  #-------------------------------------------------
  request = asset_v1.SearchAllResourcesRequest(
    scope="projects/" + PROJECT_ID,
    asset_types=[
      "redis.googleapis.com/Instance",
    ],
  )

#  for response in client.search_all_resources(request=request):
#    print(response)


  #-------------------------------------------------
  # SERVERLESS VPC ACCESS
  # does not show IPs of connector instances
  #-------------------------------------------------
  request = asset_v1.SearchAllResourcesRequest(
    scope="projects/" + PROJECT_ID,
    asset_types=[
      "vpcaccess.googleapis.com/Connector",
    ],
  )

#  for response in client.search_all_resources(request=request):
#    print(response)



  #-------------------------------------------------
  # OUTPUT
  #-------------------------------------------------
  print(tabulate(df, headers=['ASSET TYPE', 'DISPLAY NAME', 'LOCATION', 'IP ADDRESS(ES)'], tablefmt='psql'))



if __name__ == "__main__":
  find_gcp_ips()
