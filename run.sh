frameworks="apistar bottle falcon flask hug pyramid qt sanic tornado"
#frameworks="tornado"
#frameworks=$1

for fw in $frameworks; do {
	file=$fw"-hello"
	echo $file
	if [ "$fw" = "sanic" ]; then
		gunicorn $file:app --bind 127.0.0.1:8000 --worker-class sanic.worker.GunicornWorker & ./benchmark.sh $fw
	elif [ "$fw" = "qt" ]; then
		gunicorn $file:app --bind 127.0.0.1:8000 --worker-class quart.worker.GunicornWorker & ./benchmark.sh $fw
	elif [ "$fw" = "tornado" ]; then
		gunicorn -k tornado $file:app & ./benchmark.sh $fw
	else
		gunicorn $file:app & ./benchmark.sh $fw
	fi
	#parallel ::: "gunicorn $file:app" "./benchmark.sh $fw"
} done
