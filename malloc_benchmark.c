#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Name of the compiler this program was built with, as written in the CSV file
#if defined(__clang__)
#define COMPILER "Clang"
#elif defined(_MSC_VER)
#define COMPILER "MSVC"
#elif defined(__GNUC__) && defined(__linux__)
#define COMPILER "GCC (WSL2)"
#elif defined(__GNUC__) && defined(_UCRT)
#define COMPILER "GCC (MSYS2 UCRT64)"
#elif defined(__GNUC__)
#define COMPILER "GCC (MSYS2)"
#else
#define COMPILER "Unknown"
#endif

#define CSV_FILE "performance_results.csv"
#define GIB 1073741824ULL

// memset called through a volatile pointer, so that the compiler cannot remove the writes
void *(*volatile fill)(void *, int, size_t) = memset;

// Append one result line to the CSV file
void save_result(const char *test_name, unsigned long long size, double seconds)
{
    FILE *file = fopen(CSV_FILE, "a");
    if (file == NULL)
        return;
    fprintf(file, "%s, %s, %llu, %f\n", test_name, COMPILER, size, seconds);
    fclose(file);
}

double elapsed(clock_t t1, clock_t t2)
{
    return (double)(t2 - t1) / CLOCKS_PER_SEC;
}

int main(int argc, char *argv[])
{
    // Write a header to the CSV file if it is empty
    FILE *file = fopen(CSV_FILE, "a+");
    if (file == NULL)
    {
        printf("Cannot open %s\n", CSV_FILE);
        return 1;
    }
    fseek(file, 0, SEEK_END);
    if (ftell(file) == 0)
        fprintf(file, "Test Name,Compiler,Size of Data,Speed\n");
    fclose(file);

    // Largest size (in GiB), number of repetitions and size step (in bytes) from program arguments
    unsigned long long max_size = 20, repetitions = 10, step = GIB;
    if (argc > 1)
        max_size = strtoull(argv[1], NULL, 10);
    if (argc > 2)
        repetitions = strtoull(argv[2], NULL, 10);
    if (argc > 3)
        step = strtoull(argv[3], NULL, 10);

    printf("Compiler: %s\n", COMPILER);

    for (unsigned long long i = 1; i <= max_size; i++)
    {
        unsigned long long size = i * step;

        for (unsigned long long r = 0; r < repetitions; r++)
        {
            // Allocation: allocate the buffer and write to all of it
            clock_t t1 = clock();
            char *buffer = (char *)malloc(size);
            if (buffer == NULL)
            {
                printf("Allocation of %llu bytes failed\n", size);
                return 1;
            }
            fill(buffer, 1, size);
            clock_t t2 = clock();
            save_result("Allocation", size, elapsed(t1, t2));
            printf("Allocation, %llu bytes: %f s\n", size, elapsed(t1, t2));

            // Reallocation: grow the buffer to twice its size and write to all of it
            t1 = clock();
            char *bigger = (char *)realloc(buffer, size * 2);
            if (bigger == NULL)
            {
                printf("Reallocation to %llu bytes failed\n", size * 2);
                free(buffer);
                return 1;
            }
            buffer = bigger;
            fill(buffer, 2, size * 2);
            t2 = clock();
            save_result("Reallocation", size, elapsed(t1, t2));
            printf("Reallocation, %llu bytes: %f s\n", size, elapsed(t1, t2));

            // Free: release the buffer
            t1 = clock();
            free(buffer);
            t2 = clock();
            save_result("Free", size, elapsed(t1, t2));
            printf("Free, %llu bytes: %f s\n", size, elapsed(t1, t2));
        }
    }

    return 0;
}
