# malloc Compiler Benchmark

This project benchmarks the performance (execution time) of the standard C memory allocation functions on Windows when the same program is built with different compilers: Clang, MSVC, GCC (MSYS2), GCC (MSYS2 UCRT64) and GCC (WSL2). Three operations are measured: allocation (`malloc`), reallocation (`realloc`) and deallocation (`free`), on buffers from 1 GiB to 20 GiB in 1 GiB steps, with each measurement repeated (usually 10 times). The results are stored in CSV files (`performance_results.csv`) and then visualized using a Python script (`plot.py`).

## Files

- `performance_results.csv`: The raw benchmark data used for the figures (Clang, MSVC, GCC (MSYS2) and GCC (WSL2)), with the columns `Test Name` (Allocation, Reallocation or Free), `Compiler`, `Size of Data` (bytes) and `Speed` (time in seconds).
- Result sets for each combination of compilers, in the same format:
  - [`clang_msvc/`](clang_msvc): Clang and MSVC.
  - [`clang_msvc_gcc(msys2)/`](clang_msvc_gcc(msys2)): adds GCC (MSYS2).
  - [`clang_msvc_gcc(msys2)_gcc(msys2_ucrt)/`](clang_msvc_gcc(msys2)_gcc(msys2_ucrt)): adds GCC (MSYS2) and GCC (MSYS2 UCRT64).
  - [`clang_msvc_gcc(msys2)_gcc(wsl2)/`](clang_msvc_gcc(msys2)_gcc(wsl2)): adds GCC (MSYS2) and GCC (WSL2); identical to the top-level `performance_results.csv`.
  - [`clang_msvc_gcc(msys2)_gcc(wsl2)_gcc(msys2_ucrt)/`](clang_msvc_gcc(msys2)_gcc(wsl2)_gcc(msys2_ucrt)): all five compilers.
- `plot.py`: A Python script to process `performance_results.csv` and generate performance plots.
- `plots/`: The generated figures (`Allocation`, `Reallocation` and `Free`), as PDF and SVG.

## Usage

### 1. Running Benchmarks

The CSV files were produced by running the same benchmark program built with each compiler.

*Note: The source code of the benchmark program is not included in this repository; only its results are.*

### 2. Generating Plots

To generate the plots from the `performance_results.csv` data:

1.  **Install Dependencies:** Ensure you have the required Python libraries installed.
    ```bash
    pip install pandas matplotlib
    ```
2.  **Run the Plotting Script:**
    ```bash
    python plot.py
    ```

To plot another set of compilers, copy its `performance_results.csv` from one of the folders above to the top level first.

## Output

The `plot.py` script will create a directory named `plots/` (if it doesn't already exist) and save one figure per operation as PDF and SVG files within this directory. Each figure shows the mean time per compiler for each memory size as a bar chart (the two largest sizes are left out), with a table of the minimum, mean and maximum time per compiler underneath.

## Publication
- Y. Hadjadj, C. M. A. Zouaoui and N. Taleb, “Benchmarking Memory Allocation Performance in Windows: A Comparative Analysis of malloc Across Different Compilers,” *4th Journées Doctorales en Génie Électrique (JDGE 2023)*, Sidi Bel Abbès, Algeria, 28–29 Nov. 2023. [Event page](https://www.univ-sba.dz/ge/fr/les-quatriemes-journees-doctorales-en-genie-electrique28-29-novembre-2023/) · [Abstract book](https://www.univ-sba.dz/ge/wp-content/uploads/2026/03/4%C2%B0-Journees-doctorales-en-genie-electrique-2023.pdf) (p. 95)
