''' Author: Tapti Palit '''

import sys
import os

syscallfns = ['syscall.Syscall', 'syscall.Syscall6', 'syscall.RawSyscall',
        'syscall.rawVforkSyscall',
        'syscall.rawSyscallNoError'];

runtimeSyscalls = [
        '0',
        '1',
        '3',
        '9',
        '11',
        '12',
        '13',
        '14',
        '15',
        '24',
        '27',
        '28',
        '35',
        '38',
        '39',
        '41',
        '42',
        '56',
        '60',
        '62',
        '72',
        '131',
        '158',
        '186',
        '202',
        '204',
        '213',
        '231',
        '233',
        '234',
        '257',
        '269',
        '281',
        '291'
];

#runtimeSyscallMap = {
#        'runtime.exit': ['231'],
#        'runtime.exitThread': ['60'],
#        'runtime.open': ['257'],
#        'runtime.closefd': ['3'],
#        'runtime.write': ['1'],
#        'runtime.read': ['0'],
#        'runtime.usleep': ['35'],
#        'runtime.gettid': ['186'],
#        'runtime.raise': ['186', '234'],
#        'runtime.raiseproc': ['62'],
#        'runtime.setitimer': ['38'],
#        'runtime.mincore': ['27'],
#        'runtime.rtsigprocmask': ['14'],
#        'runtime.rt_sigaction': [13],
#        'runtime.rt_sigreturn': [15],
#        'runtime.sysMmap': [9],
#        'runtime.sysMunmap' : [11],
#        'runtime.madvise' : [28],
#        'runtime.futex' : [202],
#        'runtime.clone' : [56, 186, 60],
#        'runtime.sigaltstack' : [131],
#        'runtime.settls' : [158],
#        'runtime.osyield' : [24],
#        'runtime.sched_getaffinity' : [204],
#        'runtime.epollcreate' : [213],
#        'runtime.epollcreate1' : [291],
#        'runtime.epollctl' : [233],
#        'runtime.epollwait' : [281],
#        'runtime.closeonexec' : [72],
#        'runtime.access' : [269],
#        'runtime.connect' : [42],
#        'runtime.socket' : [41],
#        'runtime.sbrk0' : [12]
#        }



syscallSet = set()

def sanitize(instr):
    outstr = ""
    for s in instr:
        if s == "<":
            continue
        if s == ">":
            continue
        if s == ":":
            continue
        if s == "'":
            continue
        if s == ";":
            continue
        if s == "(":
            continue
        if s == ")":
            continue
        if s == ",":
            continue
        if s == "\\":
            continue
        if s == '\n':
            continue
        if s == '"':
            continue
        if s == ' ':
            continue
        outstr += s
    return outstr

def parseGoCallGraph(inputdir):
    for fname in os.listdir(inputdir):
        f = open(inputdir + fname)
        for line in f:
            splitted = line.split('->')
            if len(splitted) < 2:
                continue
            caller = sanitize(splitted[0])
            callee = sanitize(splitted[1])
            arg0 = splitted[2] # don't remove the : in this

            #print caller, ' calls ', callee
            for syscallfn in syscallfns:
                #print syscallfn
                if syscallfn == callee:
                    #print 'syscall found'
                    if 'nil' in arg0:
                        sys.stderr.write('Cannot reason about system call in ' +
                                caller + ' to ' + callee);
                        continue
                    arg0splitted = arg0.split(':')
                    syscallNo = sanitize(arg0splitted[0])
                    #print arg0
                    #print arg0splitted
                    #print syscallNo
                    try:
                        syscallSet.add(int(syscallNo))
                    except ValueError:
                        print 'This was not an integer', syscallNo, caller, callee
            
        f.close()
    for syscall in runtimeSyscalls:
        syscallSet.add(int(syscall))

if __name__ == "__main__":
    parseGoCallGraph(sys.argv[1])
    for syscall in sorted(syscallSet):
        print syscall

