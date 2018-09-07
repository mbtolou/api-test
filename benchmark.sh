sleep 2

TIME=60s

OUT="results"
if [ ! -f "$OUT" ]; then
	mkdir -p "`dirname \"$OUT\"`" 2>/dev/null
fi

REQUESTS=$(wrk -d$TIME -t2 -c200 http://127.0.0.1:8000 \
	| grep "requests in" \
	| cut -dr -f1 \
	| tr -dc '0-9')

printf "%-8s: %8s requests in %5s\n" "$1" "$REQUESTS" "$TIME" >> $OUT

pkill -f hello
