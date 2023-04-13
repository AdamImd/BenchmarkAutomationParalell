#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
#include <sys/time.h>
#include "./config.h"
#include "./kernels.h"

// gcc -fopenmp -o shared ./sharedMemoryParallel.c ./kernels.c

int main() {
    int integerDimension = DIMENSION;
    double precision = PRECISION;

    // Initialize random seed
    srand(SEED);
    
    double (*array)[integerDimension] = malloc(integerDimension * sizeof(*array));
    double (*copy)[integerDimension]  = malloc(integerDimension * sizeof(*copy));
    printf("Dimension: %d \n", integerDimension);
    printf("Precision: %f \n", precision);

    for (int i = 0; i < integerDimension; i++) {
        for (int j = 0; j < integerDimension; j++) {
            // Random value between 0 and 100
            copy[i][j] = (double)rand() / (double)RAND_MAX * MAX_VALUE;
        }
    }
    
    double(*kernels[])(double array[][integerDimension], int integerDimension, double precision, int precisionCount) = {
        single,
        naive_parallel,
        };
    char* kernel_names[] = {
        "single",
        "naive_parallel",
        };


    FILE* kernel_files = fopen("/tmp/parallel-kernels.txt", "w");
    printf("Kernel: %s \n", kernel_names[KERNEL]);
    int iteration = 0;
    int precisionCount = 0;

    char* kernel_file = malloc(100);
    sprintf(kernel_file, "/tmp/%s-names.txt", kernel_names[KERNEL]);
    fprintf(kernel_files, "%s, %s, %i\n", kernel_file, kernel_names[KERNEL], MAX_VALUE);
    FILE *names = fopen(kernel_file, "w");


    memcpy(array, copy, integerDimension * integerDimension * sizeof(double));
    while (1) {
        struct timeval tv;
        gettimeofday(&tv, NULL);
        unsigned long wall_micros = 1000000 * tv.tv_sec + tv.tv_usec;
        clock_t cycles = clock();

        precisionCount = kernels[KERNEL](array, integerDimension, precision, precisionCount);

        cycles = clock() - cycles;
        gettimeofday(&tv, NULL);
        wall_micros = 1000000 * tv.tv_sec + tv.tv_usec - wall_micros;


        // Filename format: /tmp/parallel-<dimension>-<precision>_<iteration>.csv
        char* file_name = malloc(100);
        sprintf(file_name, "/tmp/data_%s-%d-%f_%d.csv", kernel_names[KERNEL], integerDimension, precision, iteration);
        FILE *fp = fopen(file_name, "w");
        for (int i = 0; i < integerDimension; i+=LOG_STEP) {
            for (int j = 0; j < integerDimension; j+=LOG_STEP) {
                fprintf(fp, "%f,", array[i][j]);
            }
            fprintf(fp, "\n");
        }
        // Print the time
        fclose(fp);
        fprintf(names, "%s, %ld, %ld, %i\n", file_name, cycles, wall_micros, precisionCount);

        // Check if the result is within the precision
        printf("Precision count: %d/%d \n", precisionCount, (integerDimension - 2) * (integerDimension - 2));
        if (precisionCount == (integerDimension - 2) * (integerDimension - 2)) {
            break;
        }
        precisionCount = 0;
        iteration++;
        if(iteration > 20) {
            break;
        }
        

        fclose(names);
    }
    
}
