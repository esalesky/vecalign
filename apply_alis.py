import sys
import json

alifile = sys.argv[1]
srcfile = sys.argv[2]
tgtfile = sys.argv[3]
outdir  = sys.argv[4]
src  = sys.argv[5]
tgt  = sys.argv[6]

mistakes = "summary."+src+"-"+tgt
talk = srcfile.split('/')[1].split('.')[0]
srcs = []
tgts = []

with open(srcfile,'r') as f:
    line = f.readline().strip()
    while line:
        srcs.append(line)
        line = f.readline().strip()
    
with open(tgtfile,'r') as f:
    line = f.readline().strip()
    while line:
        tgts.append(line)
        line = f.readline().strip()
    
with open(alifile,'r') as f, open(outdir + "/" + talk + '.' + src,'w') as srcout, open(outdir + "/" + talk + '.' + tgt,'w') as tgtout, open(mistakes,'a') as errfile:
    line = f.readline().strip()
    while line:
        s,t,c = line.split(":")
        ss = json.loads(s)
        tt = json.loads(t)
        if len(ss) > 1:
            print("-- WARN: src in %s has more than 1 sent -- " % srcfile)
            print("-- WARN: src in %s has more than 1 sent -- " % srcfile, file=errfile)
        if len(ss) == 0:
            print("%s : src was null-aligned -- " % talk)
            print("%s : src was null-aligned -- " % talk, file=errfile)
        if len(tt) == 0:
            print("%s: tgt was null-aligned -- " % talk)
            print("%s: tgt was null-aligned -- " % talk, file=errfile)
            
        srctmp = ' '.join([srcs[x] for x in ss])
        tgttmp = ' '.join([tgts[x] for x in tt])

        srcout.write(srctmp+'\n')
        tgtout.write(tgttmp+'\n')
        
        line = f.readline().strip()
