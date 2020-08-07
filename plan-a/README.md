# Assumption of the Case 

Imagine that you meet with a small gaming startup company in the early stages of their operations. They have already launched 1 light games. Currently they use single MYSQL database running on one host to store all the data. Like many small start-ups they are confident that they will be the next big thing and expect significant, rapid, yet unquantified growth in the next few months. Actually they would develop v2.0 game which would be a more complex game. They want to review the design of database before the development. In v2.0 game, the requirement of database would be:
- They would store various data in database such as metadata, transaction data, session data, log data etc.
- Most of the operation of the data is quite simple query, but also has some complex query.
- The number of concurrent access to database could be very large and not stable.
- They want the performance won’t be degrade even the size of data grows up rapidly.
- The history data in v1.0 database should be migrated to v2.0 database.
- Their games just need 1 year data in most case, the history data would be used for analytics.
- They would like to develop the global uniform game in the future. So they need the database can be launched in many regions to speed up the data access of the players in the world.
- They would like to add recommendation feature based on relationships between information such as player interests, friends, and purchase history etc.

#	Executive Summary

## Requirements Analysis 

- Scaling to meet the demand, but with uncertainty around when and how much this demand will be they are very concerned about buying too much infrastructure too soon or not enough too late!
- Their lack of provision for Disaster Recovery their ability to configure their database and data access layer for high performance and throughput
- Making the player experience very low latency even though a large portion of their user base will be from far away
- Effective distribution of load a self-healing infrastructure that recovers

# Solution Design

## Architecture Overview 

![img](./aws-interview-architecture-overview.png)

## Design Details 

### Keyspaces

![img](./aws-interview-architecture-keyspaces.png)

Features: Why do we choose Apache Cassandra or Amazon Keyspaces

*** Note: Keyspaces is compatible with Apache Cassandra ***

- Fault Tolerant: Data is automatically replicated to multiple nodes for fault-tolerance. Replication across multiple data centers is supported. Failed nodes can be replaced with no downtime.
- Decentralized: There are no single points of failure. There are no network bottlenecks. Every node in the cluster is identical.
- Scalable: Some of the largest production deployments include Apple's, with over 75,000 nodes storing over 10 PB of data, Netflix (2,500 nodes, 420 TB, over 1 trillion requests per day), Chinese search engine Easou (270 nodes, 300 TB, over 800 million requests per day), and eBay (over 100 nodes, 250 TB).
- Durable: Cassandra is suitable for applications that can't afford to lose data, even when an entire data center goes down.
- Elastic: Read and write throughput both increase linearly as new machines are added, with no downtime or interruption to applications.
- Guarantee Replication: Choose between synchronous or asynchronous replication for each update. Highly available asynchronous operations are optimized with features like Hinted Handoff and Read Repair.

Maintains: How do we use Apache Cassandra or Amazon Keyspaces

*** Note: Differences between Amazon Keyspaces and Apache Cassandra ***

| Item | Apache Cassandra | Amazon Keyspaces |
| - | - | - |
| Monitoring | Self managed | There is a Dashboard for monitoring Performance and Error |
| Encryption | Self managed | Encryption at rest is automatically enabled when you create a new Amazon Keyspaces table and all client connections require Transport Layer Security (TLS).  |
| No servers to manage | Self managed | You don’t have to provision, patch, or manage servers, which allows you to focus on building better applications. Capacity is on-demand—you pay for only the resources you use and you don’t have to plan for peak workloads. |
| Highly available and secure | Self managed | Tables are encrypted by default and replicated three times in multiple AWS Availability Zones for high availability. Secure your data with access management, and use performance monitoring to keep your applications running smoothly. |
| Performance at scale | Self managed | Consistent, single-digit-millisecond response times at any scale. Build applications with virtually unlimited throughput and storage, that can serve thousands of requests per second without capacity planning. |
| Recovery | Self managed | Point-in-time recovery (PITR) helps protect your Amazon Keyspaces tables from accidental write or delete operations by providing you continuous backups of your table data for 35 days (at no additional cost) |

Costs: If we plan to use Apache Cassandra on AWS, there is differences between EC2 and Keyspaces
- 40,000 write per sec, data request size is 1KB
- 40,000 read per sec, data return size is 4KB
- total data size 1TB

- Apache Cassandra on EC2:
  - 3 nodes
- Amazon Keyspaces:
  - On-Demand Capacity Mode: Amazon Keyspaces can scale the throughput capacity for your table up to any previously reached traffic level instantly, and then back down when application traffic decreases. 
    - On-demand mode is a good option if any of the following is true:
      - You create new tables with unknown workloads. 
      - You have unpredictable application traffic.
      - You prefer the ease of paying for only what you use.
  - Provisioned Throughput Capacity Mode: You specify the number of reads and writes per second that are required for your application.
    - Provisioned throughput capacity mode is a good option if any of the following is true:
      - You have predictable application traffic.
      - You run applications whose traffic is consistent or ramps up gradually.
      - You can forecast capacity requirements to optimize price.

| Charge Type | Price |
| - | - |
| On-demand mode, WRU (The maximum write throughput per second 40,000), 1 WRU = 1 LOCAL_QUORUM (1KB) | $1.6508 per million (1GB) |
| On-demand mode, RRU (The maximum read throughput per second 40,000), 1 RRU = 1 LOCAL_QUORUM (4KB) = 2 LOCAL_ONE (8KB) | $0.331 per million (4GB/8GB) |
| Provision mode, WCU (The maximum write throughput per second 40,000), 1 WCU = 1 LOCAL_QUORUM (1KB) | $0.0008538 per hour |
| Provision mode, RCU (The maximum read throughput per second 40,000), 1 RCU = 1 LOCAL_QUORUM (4KB) = 2 LOCAL_ONE (8KB) | $0.0001708 per hour |
| Storage | $0.34 per GB-month |
| PITR | $0.272 per GB-month |
| Backup restore | $0.171 per GB |
| All data transfer in |	$0.00 per GB |
| Data Transfer OUT | |
| | Up to 1 GB/month	$0.00 per GB |
| | Next 9.999 TB/month	$0.12 per GB |
| | Next 40 TB/month	$0.085 per GB | 
| | Next 100 TB/month	$0.082 per GB | 
| | Greater than 150 TB/month	$0.08 per GB |

*** As part of the AWS Free Tier, you can get started with Amazon Keyspaces for free. For the first three months, you are offered a monthly free tier of 30 million on-demand write request units, 30 million on-demand read request units, and 1 GB of storage (limit of one free tier per payer account). Your free tier starts from the first month when you create your first Amazon Keyspaces resource. ***

Summary:
| Item | Apache Cassandra | Amazon Keyspaces |
| - | - | - |
| Features | Same | Same |
| Maintains | Self managed | Most of works managed by AWS |
| Costs | High | Low | 

QAs:

Q: They would store various data in database such as metadata, transaction data, session data, log data etc. 
- Yes

Q: Most of the operation of the data is quite simple query, but also has some complex query.
- For quite simple query, it must be query by primay key, although we can make secondary index.
- For some complex query, we can make materialized view or wide table.

Q: The number of concurrent access to database could be very large and not stable.
- We could setup a small datacenter at beginning for saving cost
- We could scale datacenter by adding new nodes, cassandra will balance data by itself. 

Q: They want the performance won’t be degrade even the size of data grows up rapidly.
- We could do read/write splitting, ex: setup 2 datacenters, one for read, one for write.

Q: The history data in v1.0 database should be migrated to v2.0 database.
- We could use [COPY FROM](https://docs.datastax.com/en/ddaccql/doc/cql/cql_reference/cqlsh_commands/cqlshCopyFrom.html) to import data with csv format
- Modify the default for the COPY FROM option in the configuration file path_to_file/.cassandra/cqlshrc and add the following lines.[Optimize](https://amazonaws-china.com/blogs/database/loading-data-into-amazon-mcs-with-cqlsh/)

Q: Their games just need 1 year data in most case, the history data would be used for analytics.
- We could set TTL for the data which need only 1 year

Q: They would like to develop the global uniform game in the future. So they need the database can be launched in many regions to speed up the data access of the players in the world.
- We could setup new datacenters in many regions
- Authentication provider: Create the authentication provider with the PlainTextAuthProvider class. ServiceUserName and ServicePassword should match the user name and password you obtained when you generated the service-specific credentials by following the steps in Generate Service-Specific Credentials.
- Local data center: Set the value for local-datacenter to the Region you're connecting to. For example, if the application is connecting to cassandra.us-east-2.amazonaws.com, then set the local data center to us-east-2. For all available AWS Regions, see Service Endpoints for Amazon Keyspaces.
- SSL/TLS: Initialize the SSLEngineFactory by adding a section in the configuration file with a single line that specifies the class with class = DefaultSslEngineFactory. Provide the path to the trustStore file and the password that you created previously.

### Elasticsearch Service

![img](./aws-interview-architecture-elasticsearch.png)

QAs:

Q: How to load streaming data into Elasticsearch
- Application write directly
- Logstash
- Lambda

```python
import boto3
import json
import requests
from requests_aws4auth import AWS4Auth

region = '' # e.g. us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = '' # the Amazon ES domain, including https://
headers = { "Content-Type": "application/json" }

def lambda_handler(event, context):
  #print("Received event: " + json.dumps(event, indent=2))

  index = event['index']
  url = host + '/' + index + '/_doc/'

  operation = event['httpMethod']
  if operation == 'DELETE':
    id = event['id']
    return requests.delete(url + id, auth=awsauth)
  else:
    document = event['doc']
    return requests.post(url, auth=awsauth, json=document, headers=headers)     
```

Q: Most of the operation of the data is quite simple query, but also has some complex query.
- We could use elasticsearch for complex query, ex: query friends by name, age or email
- We could only use keyword type for string in elasticsearch for query if we do not care about fulltext search.


### ElatiCache

QAs:

Q: They would like to develop the global uniform game in the future. So they need the database can be launched in many regions to speed up the data access of the players in the world.
- We could load some data (lookup, static, session or hot data) from cassandra into Redis Cluster to speed up the data access


### Glue for ETL

QAs:

Q: Their games just need 1 year data in most case, the history data would be used for analytics.
- We could archive history data into S3 with csv format for analytics, like recommendation feature. [Connect to Cassandra Data in AWS Glue Jobs Using JDBC](https://www.cdata.com/kb/tech/cassandra-jdbc-aws-glue.rst)


### Personalize for recommendation

QAs:

Q: They would like to add recommendation feature based on relationships between information such as player interests, friends, and purchase history etc.
- Yes
 