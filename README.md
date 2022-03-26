The script `plot.py` is run with the following arguments:
```
./plot.py /path/to/benchmark/results delay_time
```
where:
- `/path/to/benchmark/results` path to the file obtained as a result of running `strace -tt`
- `delay_time` is the delay time to differentiate between the setup time of the application and the actual benchmarking

Example 1:
Obtaining `strace -tt` output file for default `redis-benchmark`:
```
strace -tt redis-server --port 1234 2>>/tmp/redis-benchmark & \
sleep 0.1; \
redis-benchmark -p 1234 && \
kill -9 $(lsof -t -i:1234);
```

First we attach `strace -tt` to `redis-server` and redirect `stderr` (`strace`'s default output file descriptor) to our desired output file. We insert our delay of `0.1` to make sure `redis-server` is ready and then we run the benchmark, after which we kill `redis-server` to make it stop outputting information to our output file.

Then we simply run:
```
./plot.py /tmp/redis-benchmark 0.1
```
And the plot is produced.

Example 2:
Obtaining `strace -tt` output file for default `nginx`:
```
sudo service nginx start
```
First we make sure that nginx is started, then we need to find Nginx's master process PID (You can find it through `ps aux | grep nginx`) and use the additional `-f` option of `strace` to also follow whatever `nginx` may fork.
``` 
strace -ftt -p ${NGINX_MASTER_PID} 2>>/tmp/nginx-wrk & \
sudo service nginx reload; \
sleep 0.2; \
wrk -t12 -c400 -d30s http://127.0.0.1:80/index.html && \
sudo pkill nginx
```
Then we reload the service to make sure that we strace from the very beginning and catch the worker processes. Finally, we run the default benchmark of [wrk](https://github.com/wg/wrk).
Then, for our plot:
```
sed '/[pid  [0-9]*] //` && ./plot.py /tmp/nginx-wrk 0.2
```
Due to the `-f` option, additional string may be appended at the beginning of lines to indicate which child called which syscall - we want to avoid it.

