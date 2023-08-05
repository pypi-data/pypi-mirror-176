// Stephen Lawrence, 2022

/*
to build:
cc -fPIC -shared -o bayes.o bayes.c
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>

// buffer definitions
#define CSV_ROWS    4096
#define CSV_COLS    256

int square(int i) {
	return i * i;
}

int solve(char file[]){
    char buffer[1024];
    int row = 0;
    int col = 0;
    char* value;
    char* header[CSV_COLS];
    double data[CSV_COLS][CSV_ROWS];
    FILE* fp = fopen(file,"r");
    if (!fp) printf("Can't open file\n");
    else {
        while (fgets(buffer,1024,fp)) {
            col = 0;
            value = strtok(buffer, ",");
            if (row == 0) {
                while (value) {
                    header[col] = value;
                    printf("%s",header[col]);
                    value = strtok(NULL,",");
                    if (value != NULL) printf("\t");
                    col++;
                }
            }
            else {
                while (value) {
                    data[col][row] = atof(value);
                    printf("%.4f",data[col][row]);
                    value = strtok(NULL,",");
                    if (value != NULL) printf("\t");
                    col++;
                }
            }
            printf("\n");
            row++;
        }
        close(fp);
    }
    return 0;
}
