sar -d -p -f benchtimes.dat > disk.txt
sar -u -f benchtimes.dat > cpu.txt
sar -r -f benchtimes.dat > ram.txt
gzip *.txt
