all: m1.xlarge-data720iops/log.out \
	m1.xlarge-data720iops-work4000iops/log.out \
	m1.xlarge-normal/log.out \
	m2.xlarge/log.out \
	rackspace-15gb-200GB+100GB-data/log.out \
	numa/hpc.txt

clean:
	find . -name log.out -exec rm {} \;
	-rm -f numa/hpc.txt

m1.xlarge-data720iops/log.out:
	cd m1.xlarge-data720iops && python ../extract.py

m1.xlarge-data720iops-work4000iops/log.out:
	cd m1.xlarge-data720iops-work4000iops && python ../extract.py

m1.xlarge-normal/log.out:
	cd m1.xlarge-normal && python ../extract.py

m2.xlarge/log.out:
	cd m2.xlarge && python ../extract.py

rackspace-15gb-200GB+100GB-data/log.out: 
	cd rackspace-15gb-200GB+100GB-data && python ../extract.py

numa/hpc.txt:
	cd numa && python extract-times.py hpc/benchtimes.out > hpc.txt
