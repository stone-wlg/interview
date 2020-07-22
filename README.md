# Assumption of the Case 

a small gaming startup company would develop v2.0 game, migrated data from v1.0
- Currently we are focus on China and three datacenters located in Beijing, Shanghai and Guangzhou respectively, in the future maybe in other regions, America, Europe.
- We need 1 year data for most case, which is about 10TB
- Write / Read ratio is about 1:9, and most of the operation of the data is quite simple query, but also has some complex query.
- They would store various data in database such as metadata, transaction data, session data, log data etc.

- The number of concurrent access to database could be very large and not stable.
- They want the performance won’t be degrade even the size of data grows up rapidly.
- The history data in v1.0 database should be migrated to v2.0 database.
- Their games just need 1 year data in most case, the history data would be used for analytics.
- They would like to develop the global uniform game in the future. So they need the database can be launched in many regions to speed up the data access of the players in the world. But currently we are focus on China.
- They would like to add recommendation feature based on relationships between information such as player interests, friends, and purchase history etc.

#	Executive Summary

## Requirements Analysis 

- transaction data would be in mysql or postgresql database
- session data, log data and others would be in Nosql database 
- 1 year data in OLTP database, history data would be in OLAP database
- data migration from v1.0 to v2.0
- Scaling to meet the demand, but with uncertainty around when and how much this demand will be they are very concerned about buying too much infrastructure too soon or not enough too late!
- Their lack of provision for Disaster Recovery their ability to configure their database and data access layer for high performance and throughput
- Making the player experience very low latency even though a large portion of their user base will be from far away
- Effective distribution of load a self-healing infrastructure that recovers

## Solution Abstract and Benefits

Solution Abstract:
- Load Balance: nginx
- Microservices: Kubernetes
- Storage: 
  - metadata and transaction data: mysql or postgresql

  - session data: redis
  - log data: elasticsearch, fluentd and kibana
  - history data: hadoop, cassandra

Benefits:
- free
- open source


# Solution Design

## Architecture Overview 

## Design Details 

### xxx 

### xxx 
 
## Summary 

# References 
