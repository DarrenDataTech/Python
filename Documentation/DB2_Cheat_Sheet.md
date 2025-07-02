# DB2 DUMP

## Database Connection and Session Management

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

## Database Management

- **List all databases**: `db2 list database directory`
- **List all nodes**: `db2 list node directory`
- **Display current connection**: `db2 get connection`
- **Create a database**: `db2 create database <database_name>`
- **Drop a database**: `db2 drop database <database_name>`
- **Catalog a database**: `db2 catalog db <database_name> on /db`
- **Uncatalog a database**: `db2 uncatalog database <database_name>`
- **Upgrade database**: `db2 upgrade db <database_name>`

## Tables and Schemas

- **List all tables**: `db2 list tables for all`
- **Describe table structure**: `db2 describe table table_name`
- **Describe indexes**: `db2 describe indexes for table schema_name.table`
- **List all schemas**: `db2 "select schemaname from syscat.schemata"`
- **Check current schema**: `db2 "select current schema from sysibm.sysdummy1"`

## Configuration and Environment

- **Check DB config**: `db2 get db cfg`
- **Check DBM config**: `db2 get dbm cfg`
- **Check db2set**: `db2set -all`
- **Set db2set parameter**: `db2set <param>=<value>`
- **Update DB config**: `db2 update db cfg for cdb using LOGARCHMETH1 OFF`

## Backup and Recovery

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

## Performance and Monitoring

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

## High Availability and Disaster Recovery (HADR)

- **Check HADR status**: `db2pd -d <database_name> -hadr`
- **Start HADR**: `db2 start hadr on database <database_name> as standby`
- **Stop HADR**: `db2 stop hadr on db <database_name>`
- **Take over HADR**: `db2 takeover hadr on db <database_name>`

## Storage and Logs

- **Find archive log path**: `db2 get db cfg for <database_name> | grep -i "Archive" && db2 get db cfg for <database_name> | findstr /i "Archive"`
- **Find online log path**: `db2 get db cfg for <database_name> | grep -i "Path to log files"`
- **Switch/archive logs**: `db2 archive log for database <database_name>`
- **Check bufferpool**: `db2pd -db <database_name> -bufferpool`
- **Review bufferpools**: `db2pd -db <db> -bufferpools`
- **Check tablespaces**: `db2 list tablespaces show detail`

## Tools and Diagnostics

- **DB2 diagnostic log**: `db2diag -f`
- **Archive diag logs**: `db2diag -A`
- **Find DIAGPATH**: `db2 get dbm cfg | grep DIAGPATH`
- **SQL advisor**: `db2advis -d mrep -n pcmsdm -i advis.sql >advis.txt`
- **Check error code**: `db2 "? SQL1639N"`
- **Get DDL from DB**: `db2look -d sample -createdb -f -m -l -a -e -printdbcfg -o db2look.out`

## Installation and Version Checks

- **Check DB2 version**: `db2level`
- **Check DB2 is running**: `ps -ef | grep -i db2`
- **Check instance owner**: `find . -name sqllib`
- **Check prerequisites**: `./db2prereqcheck -l -I && ./db2prereqcheck -v 11.5.7.0 -i`

## Network

- **Find DB port**: `db2 get dbm cfg | grep SVCENAME && cat /etc/services | grep [service_name]`
- **Check if port is listening**: `netstat -a -n -o | find /i "60002" && netstat -a -n -o | grep "60002"`

## Licensing

- **Check license**: `db2licm -l`
- **Apply license**: `db2licm -A`

## Maintenance

- **Force end DB instance**: `db2nkill 0`
- **Force stop/start**: `db2_kill`
