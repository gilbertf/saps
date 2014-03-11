#!/usr/bin/python
import os, time, socket
import shlex, subprocess

cores = 1
SleepTime = 1

hostname = socket.gethostname()
if hostname == "wik":
    cores = 24
elif hostname == "pries":
    cores = 24
elif hostname == "gaarden":
    cores = 8
elif hostname == "mettenhof":
    cores = 15
elif hostname == "bonnie":
    cores = 6
elif hostname == "clyde":
    cores = 6
elif hostname == "ictibmt42":
    cores = 1
elif hostname == "lilalaptop":
    cores = 1
elif hostname == "megatron":
    cores = 5
elif hostname == "ictnb":
    cores = 4
elif hostname == "asterix":
    cores = 1
else:
    print "No valid host: " + hostname
    exit()

fn = "jobs/waiting/"

core = list()
p = [None]*cores

for c in range(cores):
    core.append("")

s = list('x' for a in range(cores))
j = list("No job" for a in range(cores))

while 1:
    for c in range(cores):
        #print hostname + "> checking core: " + str(c)
        if core[c] == "":
            jobs = os.listdir("jobs/waiting")
            if len(jobs) > 0:
                move_failed = 0
                job = jobs[0]
                fn_alt = fn + job
                fn_neu = "jobs/running/" + job + "." + hostname
                try:
                    os.rename(fn_alt,fn_neu)
                except:
                    move_failed = 1
                if move_failed == 0:
                    #print "Reserved by move: " + job
                    fn_neu_f = open(fn_neu)
                    cmd = fn_neu_f.read()
                    #print "Starting job " + job + ": " + cmd
                    args = shlex.split(cmd)
                    try:
                        p[c] = subprocess.Popen(args, stdout=subprocess.PIPE,stderr=subprocess.PIPE, preexec_fn=lambda : os.nice(10))
                    except:
                        print "Not able to execute: " + str(args)
                        exit()
                    j[c] = job
                    core[c] = job
                    s[c] = 's'
                else:
                    print "Job already taken, could not move"
            #else:
                #print "No waiting jobs"
        else:
            if p[c].poll() == None:
                    print "Waiting process to end"
                    s[c] = 'r'
            else:
               fn_fini = "jobs/finished/" + core[c] + "." + hostname
               fn_neu = "jobs/running/" + core[c] + "." + hostname
               fn_log_out = "logs/out/" + core[c] + "." + hostname
               fn_log_out_f = open(fn_log_out, 'w')
               msgs_out = str(p[c].stdout.read())
               fn_log_out_f.write(msgs_out)
               fn_log_out_f.close()
               fn_log_err = "logs/err/" + core[c] + "." + hostname
               fn_log_err_f = open(fn_log_err, 'w')
               msgs_err = str(p[c].stderr.read())
               fn_log_err_f.write(msgs_err)
               fn_log_err_f.close()
               print "Finished"
               print fn_neu
               print fn_fini
               os.rename(fn_neu,fn_fini)
               core[c] = ""
               s[c] = 'f'
               j[c] = "No job"
        os.system('clear')
        print "Hostname: " + hostname
        print '\r' + " ".join(s)
        s2 = ""
        for i in range(c):
            s2 = s2 + "  "
        print s2 + "+"
        for jj in j:
            print jj
        time.sleep(SleepTime)
