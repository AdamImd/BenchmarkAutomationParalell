m4 -Ulen -Uindex /home/adam/BenchmarkAutomation/benchmarks//pthread_macros/pthread.m4.stougie box.H > box.h
m4 -Ulen -Uindex /home/adam/BenchmarkAutomation/benchmarks//pthread_macros/pthread.m4.stougie box.C > box.c
m4 -Ulen -Uindex /home/adam/BenchmarkAutomation/benchmarks//pthread_macros/pthread.m4.stougie defs.H > defs.h
m4 -Ulen -Uindex /home/adam/BenchmarkAutomation/benchmarks//pthread_macros/pthread.m4.stougie particle.H > particle.h
m4 -Ulen -Uindex /home/adam/BenchmarkAutomation/benchmarks//pthread_macros/pthread.m4.stougie memory.H > memory.h
gcc -c -O2  box.c
m4 -Ulen -Uindex /home/adam/BenchmarkAutomation/benchmarks//pthread_macros/pthread.m4.stougie construct_grid.H > construct_grid.h
m4 -Ulen -Uindex /home/adam/BenchmarkAutomation/benchmarks//pthread_macros/pthread.m4.stougie construct_grid.C > construct_grid.c
m4 -Ulen -Uindex /home/adam/BenchmarkAutomation/benchmarks//pthread_macros/pthread.m4.stougie partition_grid.H > partition_grid.h
gcc -c -O2  construct_grid.c
m4 -Ulen -Uindex /home/adam/BenchmarkAutomation/benchmarks//pthread_macros/pthread.m4.stougie cost_zones.H > cost_zones.h
m4 -Ulen -Uindex /home/adam/BenchmarkAutomation/benchmarks//pthread_macros/pthread.m4.stougie cost_zones.C > cost_zones.c
gcc -c -O2  cost_zones.c
m4 -Ulen -Uindex /home/adam/BenchmarkAutomation/benchmarks//pthread_macros/pthread.m4.stougie defs.C > defs.c
gcc -c -O2  defs.c
m4 -Ulen -Uindex /home/adam/BenchmarkAutomation/benchmarks//pthread_macros/pthread.m4.stougie interactions.H > interactions.h
m4 -Ulen -Uindex /home/adam/BenchmarkAutomation/benchmarks//pthread_macros/pthread.m4.stougie fmm.C > fmm.c
gcc -c -O2  fmm.c
m4 -Ulen -Uindex /home/adam/BenchmarkAutomation/benchmarks//pthread_macros/pthread.m4.stougie interactions.C > interactions.c
gcc -c -O2  interactions.c
m4 -Ulen -Uindex /home/adam/BenchmarkAutomation/benchmarks//pthread_macros/pthread.m4.stougie memory.C > memory.c
gcc -c -O2  memory.c
m4 -Ulen -Uindex /home/adam/BenchmarkAutomation/benchmarks//pthread_macros/pthread.m4.stougie particle.C > particle.c
gcc -c -O2  particle.c
m4 -Ulen -Uindex /home/adam/BenchmarkAutomation/benchmarks//pthread_macros/pthread.m4.stougie partition_grid.C > partition_grid.c
gcc -c -O2  partition_grid.c
gcc box.o construct_grid.o cost_zones.o defs.o fmm.o interactions.o memory.o particle.o partition_grid.o -O2  -o FMM -lm
