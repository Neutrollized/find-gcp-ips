import os
import pandas as pd
from tabulate import tabulate
from google.cloud import asset_v1

PROJECT_ID=os.environ['GCP_PROJECT']

# https://cloud.google.com/python/docs/reference/cloudasset/latest/google.cloud.asset_v1.services.asset_service.AssetServiceClient#google_cloud_asset_v1_services_asset_service_AssetServiceClient_search_all_resources
# SUPPORTED ASSET TYPES: https://cloud.google.com/asset-inventory/docs/supported-asset-types

def search_all_ips():
  df = pd.DataFrame(columns=['ASSET TYPE', 'DISPLAY NAME', 'LOCATION', 'IP ADDRESS(ES)']) 


  # create client
  client = asset_v1.AssetServiceClient()

  #-------------------------------------------------
  # IP + FORWARDING RULES (public)
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
  # COMPUTE ENGINES (private + public)
  #-------------------------------------------------
  request = asset_v1.SearchAllResourcesRequest(
    scope="projects/" + PROJECT_ID,
    asset_types=[
      "compute.googleapis.com/Instance",
    ],
  )

  for response in client.search_all_resources(request=request):
    try: 
      int_ext_ips = response.additional_attributes['internalIPs'][0] + ', ' + response.additional_attributes['externalIPs'][0]
      df.loc[len(df)] = [response.asset_type, response.display_name, response.location, int_ext_ips]
    except KeyError:
      df.loc[len(df)] = [response.asset_type, response.display_name, response.location, response.additional_attributes['internalIPs'][0]]


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
    #print(response)
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
#      print(response)



  #-------------------------------------------------
  # OUTPUT
  #-------------------------------------------------
  print(tabulate(df, headers=['ASSET TYPE', 'DISPLAY NAME', 'LOCATION', 'IP ADDRESS(ES)'], tablefmt='psql'))




# TEST
search_all_ips()
