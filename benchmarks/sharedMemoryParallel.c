#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>
#include "./config.h"
#include <omp.h>
#include "kernels.h"

// gcc -fopenmp -o shared ./sharedMemoryParallel.c 

int main() {
    int integerDimension = DIMENSION;
    double precision = PRECISION;

    // Initialize random seed
    srand(time(NULL));
    
    double (*array)[integerDimension] = malloc(integerDimension * sizeof(*array));
    double (*copy)[integerDimension]  = malloc(integerDimension * sizeof(*copy));
    printf("Dimension: %d \n", integerDimension);
    printf("Precision: %f \n", precision);

    for (int i = 0; i < integerDimension; i++) {
        for (int j = 0; j < integerDimension; j++) {
            // Random value between 0 and 100
            copy[i][j] = (double)rand() / (double)RAND_MAX * MAX_VAL;
        }
    }
    
    const int len_kernel = 1;
    double(*kernels[])(double array[][integerDimension], int integerDimension, double precision, int precisionCount) = {
        single,
        };
    char* kernel_names[] = {
        "single"
        };


    FILE* kernel_files = fopen("/tmp/parallel-kernels.txt", "w");
    for (int i = 0; i < len_kernel; i++) {
        printf("Kernel: %s \n", kernel_names[i]);
        int iteration = 0;
        int precisionCount = 0;

        char* kernel_file = malloc(100);
        sprintf(kernel_file, "/tmp/%s-names.txt", kernel_names[i]);
        fprintf(kernel_files, "%s, %s, %i\n", kernel_file, kernel_names[i], MAX_VAL);
        FILE *names = fopen(kernel_file, "w");

        memcpy(array, copy, integerDimension * integerDimension * sizeof(double));
        while (1) {
            // Run the kernel
            // Get the microsecond time:
            clock_t start = clock();
            precisionCount = kernels[i](array, integerDimension, precision, precisionCount);
            time_t end = clock();

            // Filename format: /tmp/parallel-<dimension>-<precision>_<iteration>.csv
            char* file_name = malloc(100);
            sprintf(file_name, "/tmp/%s-%d-%f_%d.csv", kernel_names[i], integerDimension, precision, iteration);
            FILE *fp = fopen(file_name, "w");
            for (int i = 0; i < integerDimension; i++) {
                for (int j = 0; j < integerDimension; j++) {
                    fprintf(fp, "%f,", array[i][j]);
                }
                fprintf(fp, "\n");
            }
            // Print the time
            fclose(fp);
            fprintf(names, "%s, %ld\n", file_name, end - start);

            // Check if the result is within the precision
            printf("Precision count: %d/%d \n", precisionCount, (integerDimension - 2) * (integerDimension - 2));
            if (precisionCount == (integerDimension - 2) * (integerDimension - 2)) {
                break;
            }
            precisionCount = 0;
            iteration++;
        }

        fclose(names);
        printf("Result: %f \n", array[integerDimension/2][integerDimension/2]);
    }
    
}
