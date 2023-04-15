#include "config.h"
#include "kernels.h"
#include <math.h>
#include <omp.h>



double single(double array[][DIMENSION], int integerDimension, double precision, int precisionCount){
    double result = 0.0;
    for (int i = 1; i < integerDimension - 1; i++) {
        for (int j = 1; j < integerDimension - 1; j++) {
            result = (array[i-1][j] + array[i+1][j] + array[i][j-1] + array[i][j+1]) / 4;
            if (fabs(result - array[i][j]) < precision)
                precisionCount++;
            array[i][j] = result;
        }
    }
    return precisionCount;
}


double single_interchange(double array[][DIMENSION], int integerDimension, double precision, int precisionCount){
    double result = 0.0;
    for (int j = 1; j < integerDimension - 1; j++) {
        for (int i = 1; i < integerDimension - 1; i++) {
            result = (array[i-1][j] + array[i+1][j] + array[i][j-1] + array[i][j+1]) / 4;
            if (fabs(result - array[i][j]) < precision)
                precisionCount++;
            array[i][j] = result;
        }
    }
    return precisionCount;
}

double single_tiling(double array[][DIMENSION], int integerDimension, double precision, int precisionCount) {
    double result = 0.0;
    const int tile_size = 32;
    int i, j, ii, jj;
    for (i = 1; i < integerDimension - 1; i += tile_size) {
        for (j = 1; j < integerDimension - 1; j += tile_size) {
            int max_i = i + tile_size < integerDimension - 1 ? i + tile_size : integerDimension - 1;
            int max_j = j + tile_size < integerDimension - 1 ? j + tile_size : integerDimension - 1;
            for (ii = i; ii < max_i; ii++) {
                for (jj = j; jj < max_j; jj++) {
                    result = (array[ii-1][jj] + array[ii+1][jj] + array[ii][jj-1] + array[ii][jj+1]) / 4;
                    if (fabs(result - array[ii][jj]) < precision)
                        precisionCount++;
                    array[ii][jj] = result;
                }
            }
        }
    }
    return precisionCount;
}


double parallel(double array[][DIMENSION], int integerDimension, double precision, int precisionCount){
    double result = 0.0;
    #pragma omp parallel for reduction(+:precisionCount)
    for (int i = 1; i < integerDimension - 1; i++) {
        for (int j = 1; j < integerDimension - 1; j++) {
            result = (array[i-1][j] + array[i+1][j] + array[i][j-1] + array[i][j+1]) / 4;
            if (fabs(result - array[i][j]) < precision)
                precisionCount++;
            array[i][j] = result;
        }
    }
    return precisionCount;
}

double parallel_interchange(double array[][DIMENSION], int integerDimension, double precision, int precisionCount){
    double result = 0.0;
    #pragma omp parallel for reduction(+:precisionCount)
    for (int j = 1; j < integerDimension - 1; j++) {
        for (int i = 1; i < integerDimension - 1; i++) {
            result = (array[i-1][j] + array[i+1][j] + array[i][j-1] + array[i][j+1]) / 4;
            if (fabs(result - array[i][j]) < precision)
                precisionCount++;
            array[i][j] = result;
        }
    }
    return precisionCount;
}

double parallel_tiling(double array[][DIMENSION], int integerDimension, double precision, int precisionCount) {
    double result = 0.0;
    const int tile_size = 32;
    int i, j, ii, jj;
    #pragma omp parallel for private(j, ii, jj, result) reduction(+:precisionCount)
    for (i = 1; i < integerDimension - 1; i += tile_size) {
        for (j = 1; j < integerDimension - 1; j += tile_size) {
            int max_i = i + tile_size < integerDimension - 1 ? i + tile_size : integerDimension - 1;
            int max_j = j + tile_size < integerDimension - 1 ? j + tile_size : integerDimension - 1;
            for (ii = i; ii < max_i; ii++) {
                for (jj = j; jj < max_j; jj++) {
                    result = (array[ii-1][jj] + array[ii+1][jj] + array[ii][jj-1] + array[ii][jj+1]) / 4;
                    if (fabs(result - array[ii][jj]) < precision)
                        precisionCount++;
                    array[ii][jj] = result;
                }
            }
        }
    }
    return precisionCount;
}