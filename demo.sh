for file in demo/*; do
	echo -e "\npython ./main.py $file"
	cat $file
	sleep 1
	./main.py $file
	sleep 1
	echo ''
done
