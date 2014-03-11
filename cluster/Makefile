all: start

clean:
	-rm -r ~/Dissertation/cluster/jobs
	-rm -r ~/Dissertation/cluster/logs
	-mkdir -p ~/Dissertation/cluster/jobs/waiting
	-mkdir -p ~/Dissertation/cluster/jobs/running
	-mkdir -p ~/Dissertation/cluster/jobs/finished
	-mkdir -p ~/Dissertation/cluster/logs/out
	-mkdir -p ~/Dissertation/cluster/logs/err
	find ~/Dissertation/results -size 0 -delete

status:
	echo -n "Waiting: "
	ls -1 ~/Dissertation/cluster/jobs/waiting | grep -c .
	echo -n "Running: "
	ls -1 ~/Dissertation/cluster/jobs/running | grep -c .
	echo -n "Finished: "
	ls -1 ~/Dissertation/cluster/jobs/finished | grep -c .

start:
	./cluster.py
