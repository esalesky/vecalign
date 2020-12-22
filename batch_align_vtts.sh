#!/usr/bin/env bash
#$ -cwd
#$ -N vec
#$ -j y -o $JOB_NAME-$JOB_ID.out
#$ -m e
#$ -l ram_free=20G,mem_free=20G,gpu=1,hostname=b1[123456789]|c0*|c1[123456789]
# Submit to GPU queue
#$ -q g.q
#---------------------------------------------

hostname
source /home/gqin2/scripts/acquire-gpu
conda deactivate; conda activate laser

SRC=$1
TGT=$2

# -- get data --
datadir=$SRC-${TGT}
mkdir -p $datadir
cd $datadir
cp /export/b14/salesky/tedx/${SRC}/*/*.${SRC}.vtt.txt .
cp /export/b14/salesky/tedx/${SRC}/*/*.${TGT}.vtt .
for X in *.${TGT}.vtt; do echo ${X%.${TGT}.vtt} >> ${SRC}-${TGT}.ids; done
cd -

outdir=${SRC}-${TGT}.ali
tmpdir=tmp.${SRC}-${TGT}
mkdir -p $outdir
mkdir -p $tmpdir

TALKS=`cat ${datadir}/${SRC}-${TGT}.ids`
for TALK in $TALKS; do
    echo $TALK
    
    # -- prep txt files -- 
    python prep_src.py $datadir/$TALK.$SRC.vtt.txt $tmpdir $SRC
    python prep_vtt.py $datadir/$TALK.$TGT.vtt $tmpdir
    
    # -- prep & do vecalign -- 
    ./overlap.py -i $tmpdir/$TALK.$SRC.sents -o $tmpdir/overlaps.$SRC -n 2
    ./overlap.py -i $tmpdir/$TALK.$TGT.vtt.prepped -o $tmpdir/overlaps.$TGT -n 15

    $LASER/tasks/embed/embed.sh $tmpdir/overlaps.$SRC $SRC $tmpdir/overlaps.$SRC.emb
    $LASER/tasks/embed/embed.sh $tmpdir/overlaps.$TGT $TGT $tmpdir/overlaps.$TGT.emb

    ./vecalign.py --alignment_max_size 15 \
                  --src $tmpdir/$TALK.$SRC.sents \
                  --tgt $tmpdir/$TALK.$TGT.vtt.prepped \
                  --del_percentile_frac 0.9 \
                  --costs_sample_size 100 \
                  --src_embed $tmpdir/overlaps.$SRC $tmpdir/overlaps.$SRC.emb \
                  --tgt_embed $tmpdir/overlaps.$TGT $tmpdir/overlaps.$TGT.emb \
                  >> $tmpdir/alis
    
    python apply_alis.py $tmpdir/alis $tmpdir/$TALK.$SRC.sents $tmpdir/$TALK.$TGT.vtt.prepped $outdir $SRC $TGT

    # -- cleanup
    rm $tmpdir/*
    echo "-- next --"
done

echo '-- done! -- '
