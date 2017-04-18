#!/usr/bin/env python3
import tarfile
#import gzip
import datetime
import os
import subprocess
from shlex import quote

BACKUP_PATH = r'/root/backups/'



def pack(paths, archname):
	arcfname = gen_pack_fname(archname) + ".tar.gz"
	tar = tarfile.open(arcfname, "w:gz")
	for path in paths:
		tar.add(path)
	tar.close()

def pg_pack(dbname):
	arcpgname = gen_pack_fname(dbname) + ".backup"
	pgpack = subprocess.run(['pg_dump', '-Upostgres', '-Fc', '-Z9', '-f', arcpgname, dbname ])

def mysql_pack(dbname):
	arcmysqlname = gen_pack_fname(dbname) + ".sql.gz"
	#packcmd = 'mysqldump ' + dbname + ' | ' + 'gzip ' + '> ' + arcmysqlname
	#mysqlpack0 = subprocess.run(['mysqldump', dbname], stdout=subprocess.PIPE)
	mysqlpack = subprocess.run('mysqldump ' + dbname + " | gzip > " + arcmysqlname, shell=True)

def gen_pack_dir(archname):
	return os.path.join(BACKUP_PATH,archname)

def gen_pack_fname(archname):
	curtime = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
	filename = archname + "_" + curtime
	return os.path.join(gen_pack_dir(archname), filename)

def cleanup(archname):
	curdir=gen_pack_dir(archname)
	#print "Cleaning %s" % curdir
	# Delete files  curtime-file ctime > 30 days
	#print os.listdir(gen_pack_dir(archname))
	#print "Now %s" % datetime.datetime.today()
	if len([name for name in os.listdir(curdir) if os.path.isfile( os.path.join(curdir,name) )])>9:
		for f in os.listdir(curdir):
			if os.path.isfile(os.path.join(curdir,f)):
				file_mtime=datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(curdir,f)))
				if file_mtime+datetime.timedelta(days=90)<datetime.datetime.today():
					os.remove(os.path.join(curdir,f))
					print (os.path.join(curdir,f), "deleted")

def main():
	etc_dirs=["/etc"]

	pack(etc_dirs, "etc")

	#print datetime.datetime.today()+datetime.timedelta(days=30)
	cleanup("etc")


if __name__ == "__main__":
	main()


