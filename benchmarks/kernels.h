#ifndef KERNLES_H
#define KERNLES_H

#include "config.h"

double single(double array[][DIMENSION], int integerDimension, double precision, int precisionCount);
double single_interchange(double array[][DIMENSION], int integerDimension, double precision, int precisionCount);
double single_tiling(double array[][DIMENSION], int integerDimension, double precision, int precisionCount);
double parallel(double array[][DIMENSION], int integerDimension, double precision, int precisionCount);
double parallel_interchange(double array[][DIMENSION], int integerDimension, double precision, int precisionCount);
double parallel_tiling(double array[][DIMENSION], int integerDimension, double precision, int precisionCount);

#endif