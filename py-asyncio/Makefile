


profile:
	timeout -s INT 5s python -m cProfile -o $(target).cprof $(target)


profiler:
	pyprof2calltree -k -i $(target).cprof