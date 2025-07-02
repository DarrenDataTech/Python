# Master Cheat Sheet

A structured cheat sheet for work.

---

## Table of Contents

- [Technologies](#technologies)
  - [DB2](#db2)
    - [DB2 Execute SQL file](#db2-execute-sql-file)
    - [DB2 Health Checks](#db2-health-checks)
    - [DB2 HADR](#db2-hadr)
    - [DB2 DUMP](#db2-dump)
  - [Linux/Ubuntu](#linuxubuntu)
    - [Linux Cheat Sheet](#linux-cheat-sheet)
  - [MongoDB](#mongodb)
    [MongoDB Import/Export](#mongodb-importexport)
    - [MongoDB DUMP](#mongodb-dump)
  - [SQL](#sql)
    - [SQL Cheat Sheet](#sql-cheat-sheet)
  - [PostgreSQL](#postgresql)
  - [Docker](#docker)
  - [Git](#git)
    - [Git & GitHub Cheat Sheet](#git--github-cheat-sheet)
  - [Jenkins](#jenkins)
- [Common Tasks](#common-tasks)
- [Troubleshooting](#troubleshooting)
- [References & Links](#references--links)

---

## Technologies

## DB2

### DB2 Backup/Restore

Complete an ONLINE backup.

```bash
db2 backup db database_name online to /PATH

nohup db2 backup db cdb online to /db/backup compress &
```

Complete an OFFLINE backup.

```bash
db2 backup database cdb to /PATH COMPRESS

nohup db2stop force && db2start && db2 backup database cdb to '/db/backup' COMPRESS &
```

If you are unable to perform an  OFFLINE backup due to the below message, attempt deactivating the db first.

*SQL1035N  The operation failed because the specified database cannot be connected to in the mode requested.  SQLSTATE=57019

```bash
db2 force applications all;db2 deactivate database cdb; db2 backup database cdb to /db/backup; db2 activate cdb
```

Backup database to /dev/null (Complete to activate ONLINE backups).

```bash
db2 backup db database_name to /dev/null
```

View the progress of a backup.

```bash
db2 list utilities show detail
```

List recent backups.

```bash
db2 list history backup all for database_name
```

Restore database ON and FROM.

```bash
db2 "restore db database_name from /db/backup/ ON /db"
```

Restore database and accept the override warning.

```bash
db2 deactivate db cdb;db2 FORCE APPLICATIONS ALL;db2stop force;db2start; echo "y" | nohup db2 restore db cdb &
```

Restore logs from backup image.

```bash
db2 restore db cdb logs logtarget /opt/db2/dbfiles/CDBLOGS/HUUS_DB2_CDB_LOGS/NODE0000/LOGSTREAM0000/
```

Roll forward database to end of the newly restored logs.

```bash
db2 rollforward db cdb to end of logs and stop overflow log path '(/opt/db2/dbfiles/CDBLOGS/HUUS_DB2_CDB_LOGS/NODE0000/LOGSTREAM0000)'
```

Generate restore redirect script.

```bash
db2 restore db cdb redirect generate script restore.sh
db2 -tvf restore.sh
```

'DBPATH' to '/db'
'STOGROUP PATHS' to '/db/CDB/'
'LOGTARGET'/'NEWLOGPATH' to '/db/cdb-logs/'
Change table spaces from /db2-data/cdb to /db/CDB

### DB2 Execute SQL file

Execute SQL file with @ terminator.

```bash
db2 -v -td@ -s -f
```

Execute SQL file with @ terminator and continue after error.

```bash
db2 -v -td@ -f
```

Execute SQL file with ; terminator.

```bash
db2 -tvf
```

### DB2 Health Checks

Below are basic health checks to complete for a IBM DB2 database.
All checks can be complete via db2_healther_checker_MASTER.sh.

### DB2 Invalid entites

Check for invalid objects

```bash
db2 "select * from SYSCAT.INVALIDOBJECTS"
```

Check for invalid triggers

```bash
db2 "select TRIGNAME,valid from syscat.triggers where valid != 'Y'"
```

Re-validate objects

```bash
db2 "CALL SYSPROC.ADMIN_REVALIDATE_DB_OBJECTS(NULL, NULL, NULL)"
```  

#### DB2 Recreate Aliases

Public alias version.

```bash
db2 -tx "select 'create or replace public alias ' ||a.tabname || ' for table '|| rtrim(a.tabschema)||'.'||a.tabname ||';' from syscat.tables a where a.tabschema='PCMSDM' and  a.type in ('T','G')" > create_synonyms.sql
db2 -tx "select 'create or replace public alias ' ||a.viewname || ' for '|| rtrim(a.viewschema)||'.'||a.viewname ||';' from syscat.views a where a.viewschema='PCMSDM'" >> create_synonyms.sql
db2 -tvf create_synonyms.sql
```

Synonym version.

```bash
db2 terminate
db2 connect to cdb
db2 -tx "select 'create or replace synonym ' ||a.tabname || ' for table '|| rtrim(a.tabschema)||'.'||a.tabname ||';' from syscat.tables a where a.tabschema='PCMSDM' and type ='T'" > create_aliases.sql
db2 -tvf create_aliases.sql
```

#### DB2 Run stats on all tables

ONLY COMPLETE IF NEEDED.

```bash
db2 "SELECT 'runstats on table ' || rtrim(tabschema) || '.' || rtrim(tabname) || ' with distribution on key COLUMNS AND SAMPLED DETAILED INDEXES ALL ALLOW WRITE ACCESS tablesample system (10) indexsample system (10);' FROM syscat.tables WHERE tabschema = 'PCMSDM' AND type = 'T'" > run_runstats.sql
db2 -tvf run_runstats.sql
```

Tables with changes in the last 3 hours.

```bash
db2 -tx "select 'RUNSTATS ON TABLE '||rtrim(a.tabschema)||'.'||a.tabname ||'  with distribution on key COLUMNS AND SAMPLED DETAILED INDEXES ALL allow write access tablesample system (10) indexsample system (10);' from syscat.tables a where a.tabschema='PCMSDM' and type ='T' and create_time > (current timestamp - 3 hours)" > stats.out
db2 -tvf stats.out
```

#### DB2 Recreate read ONLY role

```bash
db2 "drop role rorole"
 
db2 "CREATE ROLE ROROLE"

db2 -tx "select 'grant select on ' || rtrim(a.tabschema)||'.'||a.tabname ||' to ROROLE;' from syscat.tables a where a.tabschema='PCMSDM' and a.type in ('T','G')" > grants.sql
 
db2 -tx "select 'grant select on ' || rtrim(b.viewschema)||'.'||b.viewname ||' to ROROLE;' from syscat.views b where b.viewschema='PCMSDM'">> grants.sql
 
db2 -tvf grants.sql

db2 "grant rorole to user cdbro"  --> for CDB
 
db2 "grant rorole to user mrepro" -- for MREP
```

## DB2 HADR

The below example is for CDB.

### Backup Prod1 & restore Prod2

1.Online backup of Prod1 CDB

```bash
nohup db2 backup db cdb online to /db/backup compress &
```

2.Upload backup to the bucket

```bash
nohup gsutil cp /db/backup/CDB.0.db2inst1.DBPART000.20241121145405.001 gs://applegreen-20231010/db2_backups/standby_backups &
```

3.Download backup from the bucket to Prod2 CDB

```bash  
nohup gsutil cp gs://applegreen-20231010/db2_backups/standby_backups/CDB.0.db2inst1.DBPART000.20241121145405.001 /db/backup &
```

### Drop and restore database

4.Drop Prod2 database

```bash
db2 force applications all;db2 deactivate db cdb;db2 drop db cdb
```

5.Restore Prod1 database on Prod2

```bash
db2 restore db cdb on /db
```

6.Check restore progress in another session

```bash
db2 list utilities show detail
```

### Set HADR config for Prod1 (primary)

```bash
db2 update db cfg for cdb using LOGARCHMETH1 DISK:/db/cdb-arch-logs/ immediate 
db2 update db cfg for cdb using HADR_SYNCMODE SUPERASYNC immediate
db2 update db cfg for cdb using HADR_LOCAL_HOST db-cdb.prod1.apgr.gcp.flooidcloudhosting.com;
db2 update db cfg for cdb using HADR_LOCAL_SVC 51000;
db2 update db cfg for cdb using HADR_REMOTE_HOST db-cdb.prod2.apgr.gcp.flooidcloudhosting.com;
db2 update db cfg for cdb using HADR_REMOTE_SVC 51000;
db2 update db cfg for cdb using HADR_REMOTE_INST db2inst1;
db2 update db cfg for cdb using LOGINDEXBUILD ON
```

### Set HADR config for Prod2 (standby)

```bash
db2 update db cfg for cdb using LOGARCHMETH1 DISK:/db/cdb-arch-logs/ immediate 
db2 update db cfg for cdb using HADR_SYNCMODE SUPERASYNC immediate
db2 update db cfg for cdb using HADR_LOCAL_HOST db-cdb.prod2.apgr.gcp.flooidcloudhosting.com;
db2 update db cfg for cdb using HADR_LOCAL_SVC 51000;
db2 update db cfg for cdb using HADR_REMOTE_HOST db-cdb.prod1.apgr.gcp.flooidcloudhosting.com;
db2 update db cfg for cdb using HADR_REMOTE_SVC 51000;
db2 update db cfg for cdb using HADR_REMOTE_INST db2inst1;
db2 update db cfg for cdb using LOGINDEXBUILD ON
```

### Check the config is correct

```bash
db2 get db cfg for cdb | grep -i hadr 
db2 get db cfg for cdb | grep LOGARCHMETH1
db2 get db cfg for cdb | grep LOGINDEXBUILD
```

### Start HADR

1.Set Prod2 as standby

```bash
db2 START HADR on database cdb as standby
```
  
2.Set Prod1 as standby

```bash  
db2 START HADR on database cdb as primary 
```
  
3.Check HADR_CONNECT_STATUS and log files are in sync

```bash
db2pd -d cdb -hadr
```

4.Archive a few logs

```bash
db2 archive log for database cdb 
```

5.Check logs files are in sync

```bash
db2pd -d cdb -hadr
```

## DB2 DUMP

### DB2 Database Connection and Session Management

- **Connect to a database**: `db2 connect to database_name`
- **Disconnect from a database**: `db2 disconnect`
- **Check connection**: `db2 connect show`
- **Start DB2**: `db2start`
- **Start DB2 with encryption**: `db2start open keystore using "kothadaputhr999p"`
- **Stop DB2**: `db2stop force`
- **Open DB2 CMD (Windows)**: `db2cmd`
- **Terminate connection**: `db2 terminate`
- **Stop/terminate all applications**: `db2 FORCE APPLICATIONS ALL`
- **Force specific application**: `db2 "force application (8426)"`

### DB2 Database Management

- **List all databases**: `db2 list database directory`
- **List all nodes**: `db2 list node directory`
- **Display current connection**: `db2 get connection`
- **Create a database**: `db2 create database <database_name>`
- **Drop a database**: `db2 drop database <database_name>`
- **Catalog a database**: `db2 catalog db <database_name> on /db`
- **Uncatalog a database**: `db2 uncatalog database <database_name>`
- **Upgrade database**: `db2 upgrade db <database_name>`

### DB2 Tables and Schemas

- **List all tables**: `db2 list tables for all`
- **Describe table structure**: `db2 describe table table_name`
- **Describe indexes**: `db2 describe indexes for table schema_name.table`
- **List all schemas**: `db2 "select schemaname from syscat.schemata"`
- **Check current schema**: `db2 "select current schema from sysibm.sysdummy1"`

### DB2 Configuration and Environment

- **Check DB config**: `db2 get db cfg`
- **Check DBM config**: `db2 get dbm cfg`
- **Check db2set**: `db2set -all`
- **Set db2set parameter**: `db2set <param>=<value>`
- **Update DB config**: `db2 update db cfg for cdb using LOGARCHMETH1 OFF`

### DB2 Backup and Recovery

- **Backup database**: `db2 backup database database_name to /path/backup_name`
- **Online backup with nohup**: `nohup db2 backup db <database_name> online compress &`
- **Restore database**: `db2 restore database database_name from /path/backup_name`
- **Restore to another location**: `db2 "restore db database_name from /db/backup/ ON /db"`
- **Restore via script**: `db2 restore db cdb redirect generate script restore.sh`
- **Restore logs**: `db2 restore db cdb logs logtarget /directory/`
- **Roll forward with restored logs**: `db2 "rollforward db cdb to end of logs and stop overflow log path (/directory/)"`
- **Check backup history**: `db2 list history backup all for database_name`
- **Check backup status**: `db2 list utilities show detail`
- **Check backup image**: `db2ckbkp <IMAGE_NAME>`

### DB2 Performance and Monitoring

- **Run command file**: `db2 -tvf file.sql`
- **Run SQL file with @ terminator**: `db2 -v -td@ -s -f your_script_file.sql`
- **Run SQL file with ; terminator**: `db2 -tvf your_script_file.sql`
- **Check DB activity**: `db2top`
- **Check DB performance**: `db2pd -dbnames`
- **Check locks**: `db2 lock list`
- **Check memory usage**: `db2mtrk -i`
- **Check statistics**: `db2 runstats on table table_name with distribution and detailed indexes all`
- **Check reorg requirement**: `db2 "REORGCHK CURRENT STATISTICS ON TABLE SCHEMA.TABLE_NAME"`
- **Check reorg progress**: `db2pd -d cdb -reorg <index/table>`
- **Check reorg status**: `db2pd -db cdb -reorgs index`
- **Check restore progress**: `db2pd -d cdb -recovery`

### DB2 High Availability and Disaster Recovery (HADR)

- **Check HADR status**: `db2pd -d <database_name> -hadr`
- **Start HADR**: `db2 start hadr on database <database_name> as standby`
- **Stop HADR**: `db2 stop hadr on db <database_name>`
- **Take over HADR**: `db2 takeover hadr on db <database_name>`

### DB2 Storage and Logs

- **Find archive log path**: `db2 get db cfg for <database_name> | grep -i "Archive"`
- **Find archive log path**: `db2 get db cfg for <database_name> | findstr /i "Archive"`

- **Find online log path**: `db2 get db cfg for <database_name> | grep -i "Path to log files"`
- **Switch/archive logs**: `db2 archive log for database <database_name>`
- **Check bufferpool**: `db2pd -db <database_name> -bufferpool`
- **Review bufferpools**: `db2pd -db <db> -bufferpools`
- **Check tablespaces**: `db2 list tablespaces show detail`

### DB2 Tools and Diagnostics

- **DB2 diagnostic log**: `db2diag -f`
- **Archive diag logs**: `db2diag -A`
- **Find DIAGPATH**: `db2 get dbm cfg | grep DIAGPATH`
- **SQL advisor**: `db2advis -d mrep -n pcmsdm -i advis.sql >advis.txt`
- **Check error code**: `db2 "? SQL1639N"`
- **Get DDL from DB**: `db2look -d sample -createdb -f -m -l -a -e -printdbcfg -o db2look.out`

### DB2 Installation and Version Checks

- **Check DB2 version**: `db2level`
- **Check DB2 is running**: `ps -ef | grep -i db2`
- **Check instance owner**: `find . -name sqllib`
- **Check prerequisites**: `./db2prereqcheck -l -I && ./db2prereqcheck -v 11.5.7.0 -i`

### DB2 Network

- **Find DB port**: `db2 get dbm cfg | grep SVCENAME && cat /etc/services | grep [service_name]`
- **Check if port is listening**: `netstat -a -n -o | find /i "60002" && netstat -a -n -o | grep "60002"`

### DB2 Licensing

- **Check license**: `db2licm -l`
- **Apply license**: `db2licm -A`

### DB2 Maintenance

- **Force end DB instance**: `db2nkill 0`
- **Force stop/start**: `db2_kill`

---

## Linux/Ubuntu

## Linux Cheat Sheet

### Linux File Commands

- **List directory contents**: `ls`
- **List with details and hidden files**: `ls -al`
- **Change directory to `dir`**: `cd dir`
- **Change to home directory**: `cd`
- **Show current directory**: `pwd`
- **Create a directory `dir`**: `mkdir dir`
- **Delete file**: `rm file`
- **Delete directory `dir`**: `rm -r dir`
- **Force remove file**: `rm -f file`
- **Force remove directory `dir`**: `rm -rf dir`
- **Copy `file1` to `file2`**: `cp file1 file2`
- **Recursively copy `dir1` to `dir2`**: `cp -r dir1 dir2`
- **Move or rename `file1` to `file2`**: `mv file1 file2`
- **Create symbolic link `link` to `file`**: `ln -s file link`
- **Create or update `file`**: `touch file`
- **Place standard input into `file`**: `cat > file`
- **View contents of `file`**: `more file`
- **Output first 10 lines of `file`**: `head file`
- **Output last 10 lines of `file`**: `tail file`
- **Follow growing file output**: `tail -f file`

### Linux Process Management

- **List active processes**: `ps`
- **Display all running processes**: `top`
- **Kill process by ID**: `kill pid`
- **Kill all processes named `proc`**: `killall proc`
- **List stopped/background jobs; resume in background**: `bg`
- **Bring most recent job to foreground**: `fg`
- **Bring job `n` to foreground**: `fg n`

### Linux File Permissions

- **Change file permissions to octal**: `chmod octal file`
  - `4` – read (r)
  - `2` – write (w)
  - `1` – execute (x)

### Linux Examples

- `chmod 777` – read, write, execute for all
- `chmod 755` – rwx for owner, rx for group and others

### Linux SSH

- **Connect to host as user**: `ssh user@host`
- **Connect on port `port` as user**: `ssh -p port user@host`
- **Add your key to host for passwordless login**: `ssh-copy-id user@host`

### Linux Searching

- **Search for pattern in files**: `grep pattern files`
- **Recursively search in directory**: `grep -r pattern dir`
- **Search output of a command**: `command | grep pattern`
- **Find all instances of a file**: `locate file`

### Linux System Info

- **Show date and time**: `date`
- **Show calendar**: `cal`
- **Show uptime**: `uptime`
- **Display users online**: `w`
- **Show logged-in username**: `whoami`
- **User information**: `finger user`
- **Kernel information**: `uname -a`
- **CPU info**: `cat /proc/cpuinfo`
- **Memory info**: `cat /proc/meminfo`
- **Manual for a command**: `man command`
- **Disk usage**: `df`
- **Directory space usage**: `du`
- **Memory and swap usage**: `free`
- **Possible locations of an app**: `whereis app`
- **Which app will be run**: `which app`

### Linux Compression

- **Create tar file**: `tar cf file.tar files`
- **Extract tar file**: `tar xf file.tar`
- **Create gzip-compressed tar**: `tar czf file.tar.gz files`
- **Extract gzip-compressed tar**: `tar xzf file.tar.gz`
- **Create bzip2-compressed tar**: `tar cjf file.tar.bz2 files`
- **Extract bzip2-compressed tar**: `tar xjf file.tar.bz2`
- **Compress file to .gz**: `gzip file`
- **Decompress .gz file**: `gzip -d file.gz`

### Linux Linux/Ubuntu Network

- **Display network interfaces**: `ifconfig` or `ip addr`
- **Show routing table**: `route -n` or `ip route`
- **Check open ports**: `netstat -tuln` or `ss -tuln`
- **Test network connectivity**: `ping host`
- **Trace route to host**: `traceroute host` or `tracepath host`
- **Display DNS info**: `dig domain` or `nslookup domain`
- **Check listening services**: `lsof -i`
- **Monitor network usage**: `iftop` or `nload`
- **Download file**: `wget url` or `curl -O url`
- **Check firewall rules**: `sudo ufw status` or `sudo iptables -L`

- **Ping host**: `ping host`
- **Get domain whois info**: `whois domain`
- **Get DNS info**: `dig domain`
- **Reverse lookup host**: `dig -x host`
- **Download file**: `wget file`
- **Resume stopped download**: `wget -c file`

### Linux Installation

- **Install .deb package**: `dpkg -i pkg.deb`
- **Install .rpm package**: `rpm -Uvh pkg.rpm`

### Linux Install from Source

- `./configure`
- `make`
- `make install`

### Linux Shortcuts

- `Ctrl+C` – halts the current command
- `Ctrl+Z` – stops the current command
- `fg` – resume job in foreground
- `bg` – resume job in background
- `Ctrl+D` – log out of current session
- `Ctrl+W` – delete one word
- `Ctrl+U` – delete entire line
- `Ctrl+R` – search command history
- `!!` – repeat last command
- `exit` – log out of session
- `:q!` – vim quit without saving
- `:wq!` – vim save and quit vim
- `:1,$d` – vim delete all contents of file

---

## MongoDB

### MongoDB Cheat Sheet

#### Show Databases

```bash
show dbs
```

#### Select / Create Database

```bash
use myDatabase
```

#### Show Collections

```bash
show collections
```

#### Create Document

```javascript
db.myCollection.insertOne({
  name: "Alice",
  age: 30,
  city: "London"
})
```

#### Create Index

```javascript
db.audit_messages.createIndex( { "timestamp": 1 }, {expireAfterSeconds: 23328000 }  ); -- 270 days

db.audit_messages.createIndex( {orguCode:1, timestamp:1, eventType:1}, { "background": true } );    -------- BEST INDEX  117 uses

db.dfm_batch.createIndex(  { batchNo:1}, { "background": true } );
```

#### Find Documents

```javascript
db.myCollection.find()                          // Get all documents
db.myCollection.find({ name: "Alice" })         // Filter by field
db.myCollection.find().limit(5)                 // Limit results
db.myCollection.find().sort({ age: -1 })        // Sort by field descending
```

#### Update Documents

```javascript
db.myCollection.updateOne(
  { name: "Alice" },
  { $set: { age: 31 } }
)

db.myCollection.updateMany(
  { city: "London" },
  { $inc: { age: 1 } }
)
```

#### Delete Documents

```javascript
db.myCollection.deleteOne({ name: "Alice" })
db.myCollection.deleteMany({ age: { $lt: 18 } })
```

#### Drop Collection / Database

```javascript
db.myCollection.drop()
db.dropDatabase()
```

#### Indexes

```javascript
db.myCollection.createIndex({ name: 1 })
db.myCollection.getIndexes()
```

#### Aggregation (Simple Example)

```javascript
db.myCollection.aggregate([
  { $match: { city: "London" } },
  { $group: { _id: "$city", avgAge: { $avg: "$age" } } }
])
```

#### Operators

```javascript
$eq, $gt, $gte, $lt, $lte, $ne, $in, $nin      // Comparison
$and, $or, $not, $nor                          // Logical
$exists, $type                                 // Element
$elemMatch, $size, $all                        // Array
$expr                                          // Evaluation
$geoWithin, $geoIntersects, $near              // Geospatial
$bitsAllSet, $bitsAnySet, $bitsAllClear, $bitsAnyClear  // Bitwise
$text                                          // Text Search
$project, $meta, $slice, $map                  // Projection
$set, $unset, $inc, $push, $addToSet, $pop, $pull  // Update
```

### MongoDB Drop Database

```bash
show dbs
use databasename
db.dropDatabase()
```

### MongoDB Import/Export

To import/export in MongoDB we use the command mongoexport and mongorestore which can be for an entire collection or query.

```bash
mongoexport --collection=<coll> <options> <connection-string>
```

Examples below.

```bash
mongoexport --db=PetHotel --collection=pets --type=csv --fields=_id,name,type,weight --query='{ "type": "Dog" }' --out=data/dogs.csv

/opt/mongodb/bin/mongoexport --db=dfm --collection=dfm_nodeBatchStatus --type=csv --fields=nodeId,batchRef,action,version,storeCode,nodeName,type,status,finished,date --out=/home/mongoadmin/dfm_nodeBatchStatus.csv
```

Import example.

```bash
/opt/mongodb/bin/mongorestore -d starchef_staging --dir=/backup/starchef_staging
```

## MongoDB DUMP

### MongoDB Connection

- **Connect MongoDB shell**: `mongo --host <host> --port <port> -u <user>`
- **Connect to 127.0.0.1:27017 (default)**: `mongo`

### MongoDB Basics

- **Help (list common commands)**: `db.help()`
- **Find Mongo binary location**: `which mongo`
- **Show all available DBs**: `show dbs`
- **Show collections**: `show collections`
- **Connect/use a DB**: `use <databasename>`
- **Drop a DB**: `db.dropDatabase()`

### MongoDB Document Operations

- **Create a document**: `db.coll.insertOne({name: "Max"})`
- **Find a single document**: `db.coll.findOne()`
- **Find with conditions**: `db.coll.find({name: "Max", age: 32})`
- **Find with comparison**: `db.coll.find({"year": {$gt: 1970}})`
- **Count documents**: `db.coll.countDocuments()`
- **Quick document count**: `db.coll.estimatedDocumentCount()`

### MongoDB Collection Info

- **View collection stats**: `db.myCollectionName.stats()`

### MongoDB Aggregation Pipeline

```javascript
db.coll.aggregate([
  {$match: {status: "A"}},
  {$group: {_id: "$cust_id", total: {$sum: "$amount"}}},
  {$sort: {total: -1}}
])
```

### MongoDB Updates

- **Update a single doc**: `db.coll.update({"_id": 1}, {"year": 2016})`
- **Update many docs**: `db.coll.updateMany({"year": 1999}, {$set: {"decade": "90's"}})`

### MongoDB Export and Logs

- **Export command**: `mongoexport --collection=<coll> <options> <connection-string>`
- **Review logs**: `tail -50 mongodb.log | jq | more`

### MongoDB Working with Collections

- **Find document with condition**: `db.<collection>.find({ "items.price": { $lt: 50 } })`
- **Show collections**: `show collections`
- **Check indexes**: `db.people.getIndexes()`
- **Return formatted results**: `db.coll.find().pretty()`

### MongoDB Monitoring & Admin

- **Check if Mongo is running on Linux**: `ps -ef | grep -i mongo`
- **Check replica set status**: `rs.status()`
- **Check current operation**: `db.currentOp()`
- **Rotate log (on ADMIN DB)**: `db.adminCommand({ logRotate: 1 })`

### MongoDB Backup

- **Perform a backup**: `./mongodump --out=/opt/backup/mongodump-1`

### MongoDB Init System & GCP Access Notes

### Using System V init

- **Start MongoDB**: `sudo service mongod start`
- **Stop MongoDB**: `sudo service mongod stop`
- **Restart MongoDB**: `sudo service mongod restart`
- **Check MongoDB status**: `sudo service mongod status`

### Using systemd

- **Start MongoDB**: `sudo systemctl start mongod`
- **Stop MongoDB**: `sudo systemctl stop mongod`
- **Restart MongoDB**: `sudo systemctl restart mongod`
- **Check MongoDB status**: `sudo systemctl status mongod`

---

## SQL

### SQL Monthly Reports

*How to gather SLEPOS INFO*
Reports>Transactions>Monthly Transactions Statistics> Input - Month = All, Type = TPS_Daily, Data Source = CDB, Sort = TXN
Reports>Transactions>Monthly Transactions Statistics> Input - Month = All, Type = TPS_HOURLY, Data Source = CDB, Sort = TXN
Reports>Transactions>POS Numbers and Daily Total Transactions> Input - Data Source = CDB, Days = 28, Graphing label step = 5.

To find INSERT INTO TXN_HEADER on DPA head to 'Find SQL' > Set time to 'Last 30 days' > Search for 'INSERT INTO TXN_HEADER'

```sql
--Check for corrupt caches
SELECT DISTINCT dede_status,
                dede_last_Except,
                devc_name
                ,devc_hardware_id, ou.orgu_code, ou.orgu_name--, DEDE_DATE_TIME ,devc_cache_updated 
  FROM DELIVERY_DELTA dd INNER JOIN device ON dd.devc_id = device.devc_id
  inner join ORG_UNIT ou on device.orgu_id = ou.orgu_id
WHERE DEDE_DATE_TIME > to_char(CURRENT timestamp -5 minutes,'YYYYMMDDHH24MI') AND DEDE_STATUS = 2
FOR READ ONLY

--Check for Devices with over 1000 delta's outstanding
  with
  last_cache as (
   select * from (
    select
     devc_id,
     delc_date_time,
     delc_status,
     row_number() over (partition by devc_id order by devc_id desc, cach_id desc) rn
    from
     delivery_cache
    where
     delc_status in (1)
   )
   where
    rn = 1
  )
  SELECT
   o.orgu_name "ORGU_NAME",
   d.devc_name "Device Name",
   d.devc_hardware_id "HardwareID",
   CASE d.DEVC_DISTRIBUTE_TO
    WHEN 0 THEN 'Do NOT distribute'
    WHEN 1 THEN 'Distribute'
    ELSE        to_char(d.DEVC_DISTRIBUTE_TO)
   END "Device Status",
   CASE dd.DEDE_STATUS
    WHEN 1  THEN 'Successfully received'
      WHEN 2  THEN 'Has been refused by the Application'
    WHEN 3  THEN 'Ready for transmission'
    WHEN 4  THEN 'Has been transmitted'
    WHEN 16 THEN 'Delta delivery received but went off line'
    WHEN 18 THEN 'Delta delivery skipped because a later cache version has been applied'
    ELSE         to_char(dd.DEDE_STATUS)
   END "Delta Status",
   count (*) "Count",
   lc.delc_date_time "last_cache",
   case lc.delc_status
    WHEN 1  THEN 'Success'
    WHEN 2  THEN 'Refused by application'
    WHEN 3  THEN 'Ready for transmission'
    WHEN 4  THEN 'Has been transmitted'
    WHEN 5  THEN 'Cache build required'
    WHEN 10 THEN 'Unreachable host'
    WHEN 11 THEN 'Unknown host'
    WHEN 15 THEN 'Connection refused'
    WHEN 16 THEN 'Cache received by till'
    WHEN 17 THEN 'Cache build failed'
    WHEN 18 THEN 'Skipped because later cache'
    WHEN 19 THEN 'Awaiting creation of JAR file'
    ELSE         to_char(lc.delc_status)
   end "Cache Status"
  FROM
   DELIVERY_DELTA dd
   join DEVICE d on 
    D.DEVC_ID = DD.DEVC_ID
   join org_unit o on
    o.orgu_id = d.orgu_id
   left join last_cache lc on
    dd.devc_id = lc.devc_id
  where
    dd.DEDE_STATUS NOT IN (1, 10, 18)
   and (lc.delc_date_time is null or dd.DEDE_DATE_TIME > lc.delc_date_time)
  GROUP BY
   o.orgu_name,
   d.devc_name,
   d.devc_hardware_id,
   DEVC_DISTRIBUTE_TO,
   dd.DEDE_STATUS,
   lc.delc_date_time,
   lc.delc_status
  HAVING
   count (*) > 1000
  ORDER BY
   orgu_name,
   devc_name
  FOR READ ONLY

--Oldest Cache Check
select distinct
    cach_created,
    cach_id,
    orgu_code,
    orgu_name,
    valc_desc,
    devc_short_desc,
    devc_name,
    DEVICE_STATUS,
    CACHE_STATUS
from
    (
        select distinct
            row_number() over (partition by dc.devc_id, c.orgu_id order by c.cach_created desc) seq,
            c.cach_created,
            c.cach_id,
            o.orgu_code,
            o.orgu_name,
            vc.valc_desc,
            d.devc_short_desc,
            d.devc_name,
               CASE d.DEVC_DISTRIBUTE_TO
                  WHEN 0 THEN 'Do NOT distribute'
                  WHEN 1 THEN 'Distribute'
                  ELSE to_char (d.DEVC_DISTRIBUTE_TO)
               END
                  "DEVICE_STATUS",
            CASE dc.delc_status
                  WHEN 1  THEN 'Success'
                  WHEN 2  THEN 'Refused by application'
                  WHEN 3  THEN 'Ready for transmission'
                  WHEN 4  THEN 'Has been transmitted'
                  WHEN 5  THEN 'Cache build required'
                  WHEN 10 THEN 'Unreachable host'
                  WHEN 11 THEN 'Unknown host'
                  WHEN 15 THEN 'Connection refused'
                  WHEN 16 THEN 'Cache received by till'
                  WHEN 17 THEN 'Cache build failed'
                  WHEN 18 THEN 'Skipped because later cache'
                  WHEN 19 THEN 'Awaiting creation of JAR file'
                  ELSE         to_char(dc.delc_status)
            END 
                "CACHE_STATUS"
        from
            delivery_cache dc
            join cache c on
                c.cach_id = dc.cach_id
            join org_unit o on
                o.orgu_id = c.orgu_id
            join outlet ol on
                ol.outl_id = o.outl_id
            join validation_code vc on
                vc.valc_id = ol.valc_id_status
                join device d on
                d.devc_id = dc.devc_id
        where
                c. cach_status = 1        -- Ready cache
            and dc.delc_status !=  18        -- Successfully received by till
            and vc.valc_code != '19001'   -- For an open or opening store
    ) cache_detail
where
    seq = 1
order by
    cach_created
--fetch first 1 rows only
for read only with ur;

-- If you find device status "Do NOT distribute" then complete the below.
-- Remove delivery caches where device is 'DO NOT DISTRIBUTE'
delete from cache where cach_id in (select distinct cach_id from  cache where cach_id in (select cach_id from delivery_cache where devc_id in( select devc_id from device where DEVC_DISTRIBUTE_TO = 0)))
delete from delivery_cache where devc_id in( select devc_id from device where DEVC_DISTRIBUTE_TO = 0)

--Database Size
SELECT sum ((TBSP_TOTAL_PAGES * TBSP_PAGE_SIZE)) /1024/1024/1024  "Total Size gb",
     sum((TBSP_FREE_PAGES * TBSP_PAGE_SIZE))/1024/1024/1024 "Total Free gb"
     FROM SYSIBMADM.TBSP_UTILIZATION
     --WHERE TBSP_CONTENT_TYPE IN ('ANY','SYSTEMP')

--Number of customers
SELECT COUNT(*) FROM Customer for read only

--PAL ONLY, SALES RECEIPT TYPE BY MONTH (PLEASE CHANGE DATE RANGE)
select substr(txhd_finish_date,1,6),  
 count (case when txhd_receipt = 0 then txhd_receipt end) as "0 - Receipt printed on the POS Receipt Printer"
,count (case when txhd_receipt = 1 then txhd_receipt end) as "1 - Receipt emailed to the Email Address captured in TXN_ADDRESS"
--,count (case when txhd_receipt = 2 then txhd_receipt end) as "2 - Receipt transferred based on Customer ID"
--,count (case when txhd_receipt = 3 then txhd_receipt end) as "3 - Receipt transferred based on the Loyalty Card"
--,count (case when txhd_receipt = 4 then txhd_receipt end) as "4 - Receipt transferred based on the Payment method"
--,count (case when txhd_receipt = 5 then txhd_receipt end) as "5 - Receipt transferred to a mobile device"
,count (case when txhd_receipt = 6 then txhd_receipt end) as "6 - No Receipt is required"
--,count (case when txhd_receipt = 7 then txhd_receipt end) as "7 - official receipt for expense reimbursement"
,count (case when txhd_receipt = 8 then txhd_receipt end) as "8 - Receipt printed on the POS and emailed"
--,count (case when txhd_receipt = 9 then txhd_receipt end) as "9 - Not shown because "
,count (case when txhd_receipt is null  then 1 end)       as "No value in txhd_receipt"
,count ( NVL (txhd_receipt,1))                                   as Total
from txn_header 
where 
txhd_finish_date between '2022080100000000' 
                    and  '2022083199999999'
and TXHD_TXN_TYPE = 3
group by  substr(txhd_finish_date,1,6)
for read only;

--Daily Transaction Rate - PAL
username: reporter
password: pcms
Transactions > POS Numbers and Daily Total Transactions
CDB > 90 > 14

--Get DB Logs size 
Connect to server > df -h

```

### SQL Task Manager/TM

Here are checks to complete for investigating issues with Task Manager on CDB.

Check TM satus = <https://support-ingress.prod1.osuk.gcp.flooidcloudhosting.com/esi-taskmanager/taskmanager/v1/workStatus/SYSC/1024>
Reload TM workers = <https://support-ingress.prod1.osuk.gcp.flooidcloudhosting.com/esi-taskmanager/taskmanager/v1/reloadWork>

```sql
---- CHECKS
--- Task manager tasks (NEW)
 SELECT ou.orgu_name,
       cysc.CYSC_SCRIPT_DESC,
       cysc.CYSC_SCRIPT_CODE,
       cyst.CYST_SCHEDULE_TIME,cyst.CYST_STEP_ID,
       cysc.CYSC_SCHED_PARAM, cyst.cyst_step_params,
       --cysc.VALC_ID_OP_STATUS,
       vc.valc_desc,
       cyta.CYTA_TASK_DESC,
       cyta.cyta_task_function,
       cysc.CYSC_TYPE,
         cysc.cysc_by_time_zone
   FROM CYCLE_SCRIPT cysc
     JOIN CYCLE_STEP cyst ON cysc.CYSC_SCRIPT_ID = cyst.CYSC_SCRIPT_ID
     JOIN VALIDATION_CODE vc ON vc.VALC_ID = cysc.VALC_ID_OP_STATUS
     join CYCLE_TASK cyta on cyst.CYTA_TASK_ID_RUN = cyta.CYTA_TASK_ID 
     join ORG_UNIT OU on OU.ORGU_ID = cyta.ORGU_ID
   WHERE 
      vc.valc_desc = 'Active'  
and (  cyst.cyst_schedule_time is not null or cysc.CYSC_SCHED_PARAM is not null);

--Recently run today.
SELECT CW.CYWK_ID,CWT.CYWT_ID,cysc_script_code,  substr(cywk_created,7,2) || '/' || substr(cywk_created,5,2) ||'/' || substr(cywk_created,1,4) ||' ' || substr(cywk_created,9,2) ||':' || substr(cywk_created,11,2) "cywk_created",
       CASE
          WHEN cywk_status = 0 THEN 'CYCLE_WORK_READY'
          WHEN cywk_status = 1 THEN 'CYCLE_WORK_RUNNING'
          WHEN cywk_status = 2 THEN 'CYCLE_WORK_COMPLETE'
          WHEN cywk_status = 3 THEN 'CYCLE_WORK_FAILED'
          ELSE 'Unknown' 
       END "cywk_status",
       substr(CYWT_CREATED,7,2) || '/' || substr(CYWT_CREATED,5,2) ||'/' || substr(CYWT_CREATED,1,4) ||' ' || substr(CYWT_CREATED,9,2) ||':' || substr(CYWT_CREATED,11,2) "CYWT_CREATED",
       substr(cywt_ended,7,2) || '/' || substr(cywt_ended,5,2) ||'/' || substr(cywt_ended,1,4) ||' ' || substr(cywt_ended,9,2) ||':' || substr(cywt_ended,11,2) "cywt_ended",
       CASE
          WHEN CYWT_STATUS = 0 THEN 'CYCLE_WORK_TASK_READY'
          WHEN CYWT_STATUS = 1 THEN 'CYCLE_WORK_TASK_RUNNING'
          WHEN CYWT_STATUS = 2 THEN 'CYCLE_WORK_TASK_COMPLETE'
          WHEN CYWT_STATUS = 3 THEN 'CYCLE_WORK_TASK_FAILED'
          ELSE 'Unknown' 
       END "CYWT_STATUS"
FROM CYCLE_WORK CW INNER JOIN CYCLE_WORK_TASK CWT ON CW.cywk_id = CWT.cywk_id
WHERE   cywk_created > to_char (sysdate - 0, 'YYYYMMDD')
       --AND cysc_script_code LIKE 'REL%'
       --AND cywk_status =2
ORDER BY cywk_created desc;

--Last COMPLETED status of a job
SELECT CW.CYWK_ID,CWT.CYWT_ID,cysc_script_code,  substr(cywk_created,7,2) || '/' || substr(cywk_created,5,2) ||'/' || substr(cywk_created,1,4) ||' ' || substr(cywk_created,9,2) ||':' || substr(cywk_created,11,2) "cywk_created",
       CASE
          WHEN cywk_status = 0 THEN 'CYCLE_WORK_READY'
          WHEN cywk_status = 1 THEN 'CYCLE_WORK_RUNNING'
          WHEN cywk_status = 2 THEN 'CYCLE_WORK_COMPLETE'
          WHEN cywk_status = 3 THEN 'CYCLE_WORK_FAILED'
          ELSE 'Unknown' 
       END "cywk_status",
       substr(CYWT_CREATED,7,2) || '/' || substr(CYWT_CREATED,5,2) ||'/' || substr(CYWT_CREATED,1,4) ||' ' || substr(CYWT_CREATED,9,2) ||':' || substr(CYWT_CREATED,11,2) "CYWT_CREATED",
       substr(cywt_ended,7,2) || '/' || substr(cywt_ended,5,2) ||'/' || substr(cywt_ended,1,4) ||' ' || substr(cywt_ended,9,2) ||':' || substr(cywt_ended,11,2) "cywt_ended",
       CASE
          WHEN CYWT_STATUS = 0 THEN 'CYCLE_WORK_TASK_READY'
          WHEN CYWT_STATUS = 1 THEN 'CYCLE_WORK_TASK_RUNNING'
          WHEN CYWT_STATUS = 2 THEN 'CYCLE_WORK_TASK_COMPLETE'
          WHEN CYWT_STATUS = 3 THEN 'CYCLE_WORK_TASK_FAILED'
          ELSE 'Unknown' 
       END "CYWT_STATUS"
FROM CYCLE_WORK CW INNER JOIN CYCLE_WORK_TASK CWT ON CW.cywk_id = CWT.cywk_id
WHERE    --cywk_created > to_char (sysdate - 0, 'YYYYMMDD') and
       cysc_script_code LIKE 'RefreshMv%' and
       cywk_status =2
ORDER BY 
    cywk_created DESC;

--count amount of failing tasks
select count(*) from    CYCLE_WORK_TASK  where cywT_status !=2;

-- Check cycle_log for any errors
SELECT    substr (cylg_datetime, 7, 2)|| '/'|| substr (cylg_datetime, 5, 2)|| '/'|| substr (cylg_datetime, 1, 4)|| ' '|| substr (cylg_datetime, 9, 2)|| ':'|| substr (cylg_datetime, 11, 2)"CYLG_DATE",
           cylg_name,
           cysc_script_code,
           cylg_description
    FROM CYCLE_LOG
    WHERE CYLG_DATETIME >=
          (REPLACE (CHAR (CURRENT DATE - 10 DAYS, iso), '-', ''))
    --AND cysc_script_code like 'CDB_TRANS%'
    AND cylg_description not in ('Completed','Started')
    ORDER BY CYLG_DATETIME DESC
FOR READ ONLY;

-- Check DISTINCT exceptions
SELECT 
    cysc_script_code,
    substr(cylg_datetime, 7, 2) || '/' || substr(cylg_datetime, 5, 2) || '/' || substr(cylg_datetime, 1, 4) || ' ' || substr(cylg_datetime, 9, 2) || ':' || substr(cylg_datetime, 11, 2) AS "CYLG_DATE",
    cylg_name,
    cylg_description
FROM (
    SELECT cylg_datetime, cysc_script_code, cylg_name, cylg_description,
           ROW_NUMBER() OVER (PARTITION BY cysc_script_code ORDER BY cylg_datetime DESC) AS rn
    FROM CYCLE_LOG
    WHERE CYLG_DATETIME >= REPLACE(CHAR(CURRENT DATE - 10 DAYS, iso), '-', '')
      AND cylg_description NOT IN ('Completed', 'Started')
) AS subquery
WHERE rn = 1
ORDER BY cysc_script_code
FOR READ ONLY;

---- FIXES

-- Update statuses to complete
update   CYCLE_WORK  set CYWK_STATUS =2 where cywk_status !=2;
update   CYCLE_WORK_TASK  set CYWT_STATUS =2 where cywT_status !=2;

-- Update statuses to complete by date
update  CYCLE_WORK_TASK set  CYWT_STATUS = 2 where  CYWT_STATUS != 2 and cywt_created like '20240131%';
update CYCLE_WORK set cywk_status = 2 where cywk_status != 2 and  cywk_created   like '20240131%';

-- Update statuses to complete by 1 day old.
update   CYCLE_WORK_TASK  set CYWT_STATUS =2 where cywT_status !=2
AND    cywk_created > to_char (sysdate - 1, 'YYYYMMDD');
update   CYCLE_WORK  set CYWK_STATUS =2 where cywk_status !=2
AND    cywk_created > to_char (sysdate - 1, 'YYYYMMDD');

-- Clear TM job by specifying CYSC_SCRIPT_CODE (job name)
UPDATE CYCLE_SCRIPT
    SET VALC_ID_OP_STATUS =
           (SELECT VALC_ID
            FROM VALIDATION_CODE
            WHERE VALC_CODE = 'CYSCSTAT2' AND VALC_DESC = 'Suspended')
    WHERE     
    CYSC_SCRIPT_CODE = 'CDB_TRANS'  AND   --Change CYSC_SCRIPT_CODE to target.
    VALC_ID_OP_STATUS =
              (SELECT VALC_ID
               FROM VALIDATION_CODE
               WHERE VALC_CODE = 'CYSCSTAT1' AND VALC_DESC = 'Active')
```

## SQL DB2 System/Syscat Checks

Review indexes assosiated with a table.

```sql
SELECT ind.INDNAME AS index_name,
       ind.INDSCHEMA AS index_schema,
       ind.TABNAME AS table_name,
       ind.UNIQUERULE AS unique_rule,
       LISTAGG (col.COLNAME, ', ') WITHIN GROUP (ORDER BY col.COLSEQ) AS index_columns
FROM SYSCAT.INDEXES ind
     JOIN SYSCAT.INDEXCOLUSE col
        ON ind.INDSCHEMA = col.INDSCHEMA AND ind.INDNAME = col.INDNAME
WHERE ind.TABNAME = 'TXN_MEDIA' AND ind.TABSCHEMA = 'PCMSDM'
GROUP BY ind.INDNAME,
         ind.INDSCHEMA,
         ind.TABNAME,
         ind.UNIQUERULE
ORDER BY ind.INDNAME;
```

Review indexes with exact column set match (excluding spaces).

```sql
SELECT 
    ind.INDNAME AS index_name,
    LISTAGG(col.COLNAME, ', ') 
        WITHIN GROUP (ORDER BY col.COLSEQ) AS column_list
FROM 
    SYSCAT.INDEXES ind
JOIN 
    SYSCAT.INDEXCOLUSE col
    ON ind.INDSCHEMA = col.INDSCHEMA
    AND ind.INDNAME = col.INDNAME
WHERE 
    ind.TABNAME = 'TXN_MEDIA'
    AND ind.TABSCHEMA = 'PCMSDM'
GROUP BY 
    ind.INDNAME
HAVING 
    REPLACE(LISTAGG(col.COLNAME, ', ') 
        WITHIN GROUP (ORDER BY col.COLSEQ), ' ', '') IN (
        -- Insert your column sets here without spaces
        'TXHD_TXN_NR,TXMD_PARENT_DET_NR,TILL_SHORT_DESC,TXMD_TYPE_CONST,TXMD_VOIDED',
        'TXHD_TXN_NR,ORGU_CODE,TILL_SHORT_DESC,TXMD_TYPE_CONST,TXMD_VOIDED,PAYM_ID'
    );
```

## SQL Housekeeping/HK Checks

Below is the new Housekeeping process checks and useful SQL.

```sql
-- Check if HK is running
SELECT * FROM HK_PROCESS_WORKING WITH UR;

-- Check if the information is being logged and sucessfully ran
SELECT *
FROM hk_process_log
ORDER BY 2 DESC;

-- Any issues, shutdown the session gracefully
UPDATE HK_PROCESS_WORKING
SET HKPL_COMPLETE = 3;

-- Further issues just set the incomplete flag
CALL HK_PROCESS_LOG_INCOMPLETE ();

-- Check next run dates
SELECT HKTC_NAME, HKTG_NEXT_DATE, count (*)
FROM HK_TARGET
GROUP BY HKTC_NAME, HKTG_NEXT_DATE
ORDER BY 2, 1;

-- Check what got deleted
SELECT regexp_replace (HKPL_TARGET, ':.*$', '') target,
       substr (min (HKPL_STARTED), 9, 6) start,
       substr (max (HKPL_AMENDED), 9, 6) end,
       count (*) Shard,
       sum (HKPL_DELETED_COUNT) deleted
FROM (SELECT *
      FROM HK_PROCESS_LOG
      WHERE HKPL_STARTED > left (local_datetime (0), 8)
      UNION ALL
      SELECT * FROM HK_PROCESS_WORKING) x
GROUP BY regexp_replace (HKPL_TARGET, ':.*$', '')
ORDER BY 2 ASC
WITH UR;

-- How to set retention days and commit units
UPDATE pcmsdm.HK_TABLE_CONFIG
SET HKTC_RETENTION_DAYS = 31
WHERE HKTC_NAME = 'PRICE';

-- How to activate groups
UPDATE pcmsdm.HK_GROUP_CONFIG
SET HKGC_ACTIVE = 0
WHERE HKGC_NAME = 'logTable';

-- HK should not affect cycle job so make sure they are ok
SELECT    substr (cylg_datetime, 7, 2)
       || '/'
       || substr (cylg_datetime, 5, 2)
       || '/'
       || substr (cylg_datetime, 1, 4)
       || ' '
       || substr (cylg_datetime, 9, 2)
       || ':'
       || substr (cylg_datetime, 11, 2)"CYLG_DATE",
       cylg_name,
       cysc_script_code,
       cylg_description
FROM CYCLE_LOG
WHERE CYLG_DATETIME >=
      (REPLACE (CHAR (CURRENT DATE - 20 DAYS, iso), '-', ''))
    --AND cysc_script_code like 'CDB_TRANS%'
    --AND cylg_description not in ('Completed','Started')
ORDER BY CYLG_DATETIME DESC
FOR READ ONLY;

SELECT cysc.CYSC_SCRIPT_DESC,
       cysc.CYSC_SCRIPT_CODE,
       cyst.CYST_SCHEDULE_TIME,
       cyst.CYST_STEP_ID,
       cysc.CYSC_SCHED_PARAM,
       cysc.VALC_ID_OP_STATUS,
       vc.valc_desc,
       cyta.CYTA_TASK_DESC,
       cyta.cyta_task_function,
       cysc.CYSC_TYPE
FROM CYCLE_SCRIPT cysc
     JOIN CYCLE_STEP cyst ON cysc.CYSC_SCRIPT_ID = cyst.CYSC_SCRIPT_ID
     JOIN VALIDATION_CODE vc ON vc.VALC_ID = cysc.VALC_ID_OP_STATUS
     JOIN CYCLE_TASK cyta ON cyst.CYTA_TASK_ID_RUN = cyta.CYTA_TASK_ID
WHERE     vc.valc_desc = 'Active'
      AND (   cyst.cyst_schedule_time IS NOT NULL
           OR cysc.CYSC_SCHED_PARAM IS NOT NULL);


UPDATE pcmsdm.HK_GROUP_CONFIG
SET HKGC_ACTIVE = 0
WHERE HKGC_NAME NOT IN ('price');

SELECT HKTC_NAME, HKTG_NEXT_DATE, count (*)
FROM HK_TARGET
GROUP BY HKTC_NAME, HKTG_NEXT_DATE
ORDER BY 2, 1;
```

## SQL Cheat Sheet

```sql
-- SELECT statements
SELECT column1, column2 FROM table;
SELECT * FROM table;

-- DISTINCT
SELECT DISTINCT column FROM table;

-- WHERE clause
SELECT * FROM table WHERE condition;
-- Operators: =, !=, <>, <, >, <=, >=, BETWEEN, IN, LIKE, IS NULL

-- AND, OR, NOT
SELECT * FROM table WHERE column1 = 'value' AND column2 > 5;
SELECT * FROM table WHERE NOT column IS NULL;

-- ORDER BY
SELECT * FROM table ORDER BY column ASC;
SELECT * FROM table ORDER BY column DESC;

-- LIMIT / OFFSET
SELECT * FROM table LIMIT 10 OFFSET 20;

-- INSERT
INSERT INTO table (column1, column2) VALUES (value1, value2);

-- UPDATE
UPDATE table SET column1 = value1 WHERE condition;

-- DELETE
DELETE FROM table WHERE condition;

-- CREATE TABLE
CREATE TABLE table_name (
    id SERIAL PRIMARY KEY,
    column1 datatype,
    column2 datatype
);

-- DROP TABLE
DROP TABLE table_name;

-- ALTER TABLE
ALTER TABLE table_name ADD column_name datatype;
ALTER TABLE table_name DROP COLUMN column_name;
ALTER TABLE table_name RENAME COLUMN old_name TO new_name;

-- JOINS
SELECT * FROM table1
JOIN table2 ON table1.id = table2.fk_id;

SELECT * FROM table1
LEFT JOIN table2 ON table1.id = table2.fk_id;

SELECT * FROM table1
RIGHT JOIN table2 ON table1.id = table2.fk_id;

SELECT * FROM table1
FULL OUTER JOIN table2 ON table1.id = table2.fk_id;

-- GROUP BY + Aggregate Functions
SELECT column, COUNT(*) FROM table GROUP BY column;
SELECT column, SUM(amount) FROM table GROUP BY column;

-- HAVING (filters grouped results)
SELECT column, COUNT(*) FROM table GROUP BY column HAVING COUNT(*) > 1;

-- Subqueries
SELECT * FROM table WHERE column IN (
    SELECT column FROM another_table WHERE condition
);

-- CASE statements
SELECT name,
    CASE
        WHEN score >= 90 THEN 'A'
        WHEN score >= 80 THEN 'B'
        ELSE 'F'
    END AS grade
FROM students;

-- Views
CREATE VIEW view_name AS
SELECT column1, column2 FROM table WHERE condition;

-- Indexes
CREATE INDEX idx_name ON table (column);

-- Transactions
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT; -- or ROLLBACK;

-- Comments
-- Single-line comment
/* Multi-line
   comment */
```

---

## PostgreSQL

- Connection commands
- Backup/restore
- Performance tuning

---

## Docker

- Build/run containers
- Common Dockerfile snippets
- Docker Compose examples

---

## Git

## Git & GitHub Cheat Sheet

### Repository Setup

- **Initialize a local repository**: `$ git init`

- **Clone from remote**: `$ git clone [repository_path]`

- **Clone with a new directory name**: `$ git clone [repository_path] [new_repository_path]`

- **Shallow clone (latest revision only)**: `$ git clone --depth 1 [repository_path]`

### Branching

- **Create a branch**: `$ git branch [branch]`

- **List local branches**: `$ git branch`

- **List all branches (local + remote)**: `$ git branch -a`

- **List remote branches**: `$ git branch -r`

- **Delete a branch**: `$ git branch -d [branch]`

### Checkout

- **Switch to another branch**: `$ git checkout [branch]`

- **Create and switch to a new branch**: `$ git checkout -b [branch]`

### Status & Diff

- **Show changed file diffs**: `$ git diff`

- **Show staged/unstaged changes**: `$ git status`

### Staging (Add)

- **Add a specific file to the index**: `$ git add [filename]`

- **Add updated files to the index**: `$ git add -u`

- **Add all modified files (excluding new files)**: `$ git add -A`

- **Add all files and directories to the index**: `$ git add .`

### Committing

- **Commit staged changes**: `$ git commit`

- **Commit with a message**: `$ git commit -m "[comment]"`

- **Auto-stage & commit tracked files**: `$ git commit -a`

- **Amend the previous commit**: `$ git commit --amend`

### Log & Show

- **View commit history**: `$ git log`

- **View details of the latest commit**: `$ git show`

### Reset

- **Undo last commit (keep changes)**: `$ git reset --soft HEAD^`

- **Undo last commit and discard changes**: `$ git reset --hard HEAD^`

### Push

- **Push to remote branch**: `$ git push [remote] [branch]`

- **Push master to origin**: `$ git push origin master`

### Pull Requests

- **Create a pull request**: `$ git pull-request`

- **Create PR with message and branches**: `$ git pull-request -m "[comment]" -b defunkt:master -h mislav:feature`

### Merging

- **Merge a branch into the current one**: `$ git merge [branch]`

### Fetch & Pull

- **Fetch changes from remote**: `$ git fetch [remote]`

- **Pull (fetch + merge) from remote**: `$ git pull [remote]`

---

## Jenkins

### Ruby jobs

```json
        {
          "name": "cdb_db_check_ruby_memory_usage",
          "scheduled_time": "0 * * * *",
          "scheduled_params": "ENV=prod1; DB_NAME=cdb;",
          "template": "db_check_ruby_memory_usage_ra",
          "disabled" : false
        },
        {
          "name": "mrep_db_check_ruby_memory_usage",
          "scheduled_time": "0 * * * *",
          "scheduled_params": "ENV=prod1; DB_NAME=mrep;",
          "template": "db_check_ruby_memory_usage_ra",
          "disabled" : false
        },
        {
          "name": "esm_db_check_ruby_memory_usage",
          "scheduled_time": "0 * * * *",
          "scheduled_params": "ENV=prod1; DB_NAME=esm;",
          "template": "db_check_ruby_memory_usage_ra",
          "disabled" : false
        },
        {
          "name": "txn_db_check_ruby_memory_usage",
          "scheduled_time": "0 * * * *",
          "scheduled_params": "ENV=prod1; DB_NAME=txn;",
          "template": "db_check_ruby_memory_usage_ra",
          "disabled" : false
        },
        {
          "name": "mongo_db_check_ruby_memory_usage",
          "scheduled_time": "0 * * * *",
          "scheduled_params": "ENV=prod1; DB_NAME=mongodb;",
          "template": "db_check_ruby_memory_usage_ra",
          "disabled" : false
        },
        {
          "name": "app_mq_check_ruby_memory_usage",
          "scheduled_time": "0 * * * *",
          "scheduled_params": "ENV=prod1; APP_NAME=mq;",
          "template": "app_check_ruby_memory_usage_ra",
          "disabled" : false
        },
      {
          "name": "app_etl_check_ruby_memory_usage",
          "scheduled_time": "0 * * * *",
          "scheduled_params": "ENV=prod1; APP_NAME=etl;",
          "template": "app_check_ruby_memory_usage_ra",
          "disabled" : false
        },
```

---

## Common Tasks

- Daily setup
- Useful scripts/commands

---

## Troubleshooting

- Common errors & fixes
- Logs & debugging tools
- Incident response steps

---

## References & Links

### Flooid

### Cheat sheets

[Original Git & GitHub Cheat Sheet Cheat Sheet Reference](https://gist.github.com/mignonstyle/4b437a4060646f55964b85cd6edb4ee3)

---
