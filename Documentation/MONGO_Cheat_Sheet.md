# MongoDB Cheat Sheet

## Connection

- **Connect MongoDB shell**: `mongo --host <host> --port <port> -u <user>`
- **Connect to 127.0.0.1:27017 (default)**: `mongo`

## Basics

- **Help (list common commands)**: `db.help()`
- **Find Mongo binary location**: `which mongo`
- **Show all available DBs**: `show dbs`
- **Show collections**: `show collections`
- **Connect/use a DB**: `use <databasename>`
- **Drop a DB**: `db.dropDatabase()`

## Document Operations

- **Create a document**: `db.coll.insertOne({name: "Max"})`
- **Find a single document**: `db.coll.findOne()`
- **Find with conditions**: `db.coll.find({name: "Max", age: 32})`
- **Find with comparison**: `db.coll.find({"year": {$gt: 1970}})`
- **Count documents**: `db.coll.countDocuments()`
- **Quick document count**: `db.coll.estimatedDocumentCount()`

## Collection Info

- **View collection stats**: `db.myCollectionName.stats()`

## Aggregation Pipeline

```javascript
db.coll.aggregate([
  {$match: {status: "A"}},
  {$group: {_id: "$cust_id", total: {$sum: "$amount"}}},
  {$sort: {total: -1}}
])
```

## Updates

- **Update a single doc**: `db.coll.update({"_id": 1}, {"year": 2016})`
- **Update many docs**: `db.coll.updateMany({"year": 1999}, {$set: {"decade": "90's"}})`

## Export and Logs

- **Export command**: `mongoexport --collection=<coll> <options> <connection-string>`
- **Review logs**: `tail -50 mongodb.log | jq | more`

## Working with Collections

- **Find document with condition**: `db.<collection>.find({ "items.price": { $lt: 50 } })`
- **Show collections**: `show collections`
- **Check indexes**: `db.people.getIndexes()`
- **Return formatted results**: `db.coll.find().pretty()`

## Monitoring & Admin

- **Check if Mongo is running on Linux**: `ps -ef | grep -i mongo`
- **Check replica set status**: `rs.status()`
- **Check current operation**: `db.currentOp()`
- **Rotate log (on ADMIN DB)**: `db.adminCommand({ logRotate: 1 })`

## Backup

- **Perform a backup**: `./mongodump --out=/opt/backup/mongodump-1`

## MongoDB Init System & GCP Access Notes

## Using System V init

- **Start MongoDB**: `sudo service mongod start`
- **Stop MongoDB**: `sudo service mongod stop`
- **Restart MongoDB**: `sudo service mongod restart`
- **Check MongoDB status**: `sudo service mongod status`

## Using systemd

- **Start MongoDB**: `sudo systemctl start mongod`
- **Stop MongoDB**: `sudo systemctl stop mongod`
- **Restart MongoDB**: `sudo systemctl restart mongod`
- **Check MongoDB status**: `sudo systemctl status mongod`
