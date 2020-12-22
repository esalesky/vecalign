import sys

vttfile = sys.argv[1]
outdir  = sys.argv[2]

tgtfile = outdir + '/' + vttfile.split("/")[-1] + ".prepped"

f = open(vttfile, "r")
vtt = f.read()
vtt = vtt.strip().split('\n')
vtt = [item for item in vtt if item]
vtt = vtt[6:]
vtt = [x for x in vtt if '-->' not in x]
f.close()

f = open(tgtfile, "w")
for l in vtt:
    f.write(l + '\n')
f.close()
