for file in demo/*; do
	echo -e "\npython ./main.py $file"
	cat $file
	sleep 1
	python ./main.py $file 2>/dev/null
	sleep 1
	echo ''
done
