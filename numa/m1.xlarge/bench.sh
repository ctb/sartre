for TABLESIZE in 1e7 2e7 3e7 4e7 5e7 6e7 7e7 8e7 9e7 1e8 2e8 3e8 4e8 5e8 6e8 7e8 8e8 9e8 1e9 2e9 3e9
do
   mkdir bench-$TABLESIZE
   cd bench-$TABLESIZE
   echo bench starting `date` >> ../benchtimes.out
   normalize-by-median.py -p -k 20 -C 20 -N 4 -x $TABLESIZE /data/*.pe.qc.fq.gz
   echo bench-$TABLESIZE ending `date` >> ../benchtimes.out
   cd ../

done
