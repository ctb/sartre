Code and data for my 2014 PyCon talk:

   Instrument ALL the things: Studying data-intensive workflows in the
   clowd

See http://ivory.idyll.org/blog/2014-pycon.html

Run: 'make clean all'

To run resource tracing::

   sar -u -r -d -o times.dat 1

To extract information::

   sar -d -p -f times.dat > disk.txt
   sar -u -f times.dat > cpu.txt
   sar -r -f times.dat > ram.txt
   gzip *.txt

--titus

ctb@msu.edu
