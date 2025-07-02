# Linux Cheat Sheet

## File Commands

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

## Process Management

- **List active processes**: `ps`
- **Display all running processes**: `top`
- **Kill process by ID**: `kill pid`
- **Kill all processes named `proc`**: `killall proc`
- **List stopped/background jobs; resume in background**: `bg`
- **Bring most recent job to foreground**: `fg`
- **Bring job `n` to foreground**: `fg n`

## File Permissions

- **Change file permissions to octal**: `chmod octal file`
  - `4` – read (r)
  - `2` – write (w)
  - `1` – execute (x)

### Examples

- `chmod 777` – read, write, execute for all
- `chmod 755` – rwx for owner, rx for group and others

## SSH

- **Connect to host as user**: `ssh user@host`
- **Connect on port `port` as user**: `ssh -p port user@host`
- **Add your key to host for passwordless login**: `ssh-copy-id user@host`

## Searching

- **Search for pattern in files**: `grep pattern files`
- **Recursively search in directory**: `grep -r pattern dir`
- **Search output of a command**: `command | grep pattern`
- **Find all instances of a file**: `locate file`

## System Info

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

## Compression

- **Create tar file**: `tar cf file.tar files`
- **Extract tar file**: `tar xf file.tar`
- **Create gzip-compressed tar**: `tar czf file.tar.gz files`
- **Extract gzip-compressed tar**: `tar xzf file.tar.gz`
- **Create bzip2-compressed tar**: `tar cjf file.tar.bz2 files`
- **Extract bzip2-compressed tar**: `tar xjf file.tar.bz2`
- **Compress file to .gz**: `gzip file`
- **Decompress .gz file**: `gzip -d file.gz`

## Network

- **Ping host**: `ping host`
- **Get domain whois info**: `whois domain`
- **Get DNS info**: `dig domain`
- **Reverse lookup host**: `dig -x host`
- **Download file**: `wget file`
- **Resume stopped download**: `wget -c file`

## Installation

- **Install .deb package**: `dpkg -i pkg.deb`
- **Install .rpm package**: `rpm -Uvh pkg.rpm`

## Install from Source

- `./configure`
- `make`
- `make install`

## Shortcuts

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
