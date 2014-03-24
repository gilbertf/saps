all: start

clean:
	-rm -r jobs
	-rm -r logs
	-mkdir -p jobs/waiting
	-mkdir -p jobs/running
	-mkdir -p jobs/finished
	-mkdir -p logs/out
	-mkdir -p logs/err
	find ../../results -size 0 -delete

status:
	echo -n "Waiting: "
	ls -1 jobs/waiting | grep -c .
	echo -n "Running: "
	ls -1 jobs/running | grep -c .
	echo -n "Finished: "
	ls -1 jobs/finished | grep -c .

start:
	./cluster.py
