from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import sys

textfile = sys.argv[1]
outdir   = sys.argv[2]
src_lang = sys.argv[3]

tgtfile = outdir + '/' + textfile.split("/")[-1].replace(".vtt.txt",".sents")

punkt_param = PunktParameters()
#if add'l lang-specific abbrevations need to be added to nltk punkt models:
if src_lang == "es":
    punkt_param.abbrev_types = set(["uds"])
    #note: no trailing punctuation is to be added to abbrev, and they must be all lowercase
sentence_splitter = PunktSentenceTokenizer(punkt_param)

f = open(textfile, "r")
full  = f.read()
sents = sentence_splitter.tokenize(full)
f.close()

f = open(tgtfile, "w")
for l in sents:
    f.write(l + '\n')
f.close()
