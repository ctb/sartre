for i in $(cat /root/targets)
do
   echo $i start `date` >> /root/kmertimes.log
   make $i
   echo $i stop `date` >> /root/kmertimes.log
done 
