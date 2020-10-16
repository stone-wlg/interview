# Key Features

- Amazon Keyspaces is serverless, so you pay for only the resources that you use, and the service automatically scales tables up and down in response to application traffic.
- Amazon Keyspaces offers two throughput capacity modes for reads and writes: on-demand and provisioned, You can choose your table’s throughput capacity mode to optimize the price of reads and writes based on the predictability and variability of your workload.
- Amazon Keyspaces (for Apache Cassandra) stores three copies of your data in multiple Availability Zones for durability and high availability.
- Encryption at rest is automatically enabled when you create a new Amazon Keyspaces table and all client connections require Transport Layer Security (TLS). 
- Additional AWS security features include monitoring, AWS Identity and Access Management, and virtual private cloud (VPC) endpoints.
- When you choose on-demand mode, Amazon Keyspaces can scale the throughput capacity for your table up to any previously reached traffic level instantly, and then back down when application traffic decreases. 
- Read Request Units and Write Request Units per seconds: 
  - 1 RRU = 1 LOCAL_QUORUM (4KB) = 2 LOCAL_ONE (8KB)
  - 1 WRU = 1 LOCAL_QUORUM (1KB), All writes are using LOCAL_QUORUM consistency, and there is no additional charge for using lightweight transactions (LWTs).
- Peak Traffic and Scaling Properties:
  Amazon Keyspaces tables that use on-demand capacity mode automatically adapt to your application’s traffic volume. On-demand capacity mode instantly accommodates up to double the previous peak traffic on a table.
  - You might observe insufficient throughput capacity errors if you exceed double your previous peak within 30 minutes.
- Initial Throughput for On-Demand Capacity Mode
  - Newly created table with on-demand capacity mode: The previous peak is 2,000 WRUs or 6,000 RRUs. You can drive up to double the previous peak immediately. Doing this enables newly created on-demand tables to serve up to 4,000 WRUs or 12,000 RRUs, or any linear combination of the two.
  - Existing table switched to on-demand capacity mode: The previous peak is half the previous WCUs and RCUs provisioned for the table or the settings for a newly created table with on-demand capacity mode, whichever is higher.
- Provisioned Throughput Capacity Mode: 
  If you choose provisioned throughput capacity mode, you specify the number of reads and writes per second that are required for your application. 
  - Provisioned throughput capacity mode is a good option if any of the following is true:
    - You have predictable application traffic.
    - You run applications whose traffic is consistent or ramps up gradually.
    - You can forecast capacity requirements to optimize price.
- If your application reads or writes larger rows (up to the Amazon Keyspaces maximum row size of 1 MB), it consumes more capacity units. For example, suppose that you create a provisioned table with 6 RCUs and 6 WCUs. With these settings, your application could do the following:
  - Perform LOCAL_QUORUM reads of up to 24 KB per second (4 KB × 6 RCUs).
  - Perform LOCAL_ONE reads of up to 48 KB per second (twice as much read throughput).
  - Write up to 6 KB per second (1 KB × 6 WCUs).
- You can switch between read/write capacity modes once every 24 hours.
- Managing Amazon Keyspaces Throughput Capacity with Application Auto Scaling
  - Another example might be a new mobile gaming app that is experiencing rapid adoption. If the game becomes very popular, it could exceed the available database resources, which would result in slow performance and unhappy customers. These kinds of workloads often require manual intervention to scale database resources up or down in response to varying usage levels.
- Amazon Keyspaces (for Apache Cassandra) appears as a nine-node
- Amazon Keyspaces is serverless, so there are no clusters, hosts, or Java virtual machines (JVMs) to configure. Cassandra’s settings for compaction, compression, caching, garbage collection, and bloom filtering are not applicable to Amazon Keyspaces and are ignored if specified
- Amazon Keyspaces supports up to 3000 CQL queries per TCP connection per second, but there is no limit on the number of connections a driver can establish.
- Amazon Keyspaces supports three read consistency levels: ONE, LOCAL_ONE, and LOCAL_QUORUM. 
- Writes are durably stored before they are acknowledged using the LOCAL_QUORUM consistency level.
- Modify the default for the COPY FROM option in the configuration file path_to_file/.cassandra/cqlshrc and add the following lines.
```txt
[copy-from]
CHUNKSIZE=50
```
- Point-in-time recovery (PITR) helps protect your Amazon Keyspaces tables from accidental write or delete operations by providing you continuous backups of your table data for 35 days (at no additional cost),
- The following are some considerations for restore times.
  - You restore backups to a new table. It can take up to 20 minutes (even if the table is empty) to perform all the actions to create the new table and initiate the restore process.
  - Restore times for large tables with well distributed data models can be several hours or longer.
    If your source table contains data that is significantly skewed, the time to restore might increase. For example, if your table’s primary key is using the month of the year as a partition key, and all your data is from the month of December, you have skewed data.


Charge type	Price
Write request units	$1.6508 per million write request units
Read request units	$0.331 per million read request units

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

Server-side encryption at rest is enabled on all Amazon Keyspaces table data and cannot be disabled. You cannot encrypt only a subset of items in a table.

