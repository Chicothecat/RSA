#include <iostream>
#include <fstream>
#include <gmp.h>
#include <chrono>

using namespace std;

int trial_division(mpz_t p, mpz_t q, const mpz_t n, unsigned long &steps) {
    mpz_t i, rem, limit;
    mpz_inits(i, rem, limit, NULL);
    mpz_sqrt(limit, n);
    mpz_set_ui(i, 2);
    steps = 0;

    while (mpz_cmp(i, limit) <= 0) {
        steps++;
        mpz_mod(rem, n, i);
        if (mpz_cmp_ui(rem, 0) == 0) {
            mpz_set(p, i);
            mpz_divexact(q, n, i);
            mpz_clears(i, rem, limit, NULL);
            return 1;
        }
        mpz_add_ui(i, i, 1);
    }
    mpz_clears(i, rem, limit, NULL);
    return 0;
}

int main() {
    ofstream csv("results/benchmark.csv");
    csv << "bits_n,steps,time_us\n";

    cout << "===== BENCHMARK (TRUE PRIMES) =====" << endl;
    cout << "bits_n\tsteps\ttime_us" << endl;

    // p, q là SỐ NGUYÊN TỐ THẬT, gần nhau
    // bits của n ≈ bits(p) + bits(q)
    const char* p_str[] = {
        "251",       // 8 bit  SNT
        "1009",      // 10 bit SNT
        "4003",      // 12 bit SNT
        "16001",     // 14 bit SNT
        "65003",     // 16 bit SNT (đã check)
        "262139",    // 18 bit SNT
        "1048573",   // 20 bit SNT
        "4194301",   // 22 bit SNT
        "16777213",  // 24 bit SNT
        "67108859",  // 26 bit SNT
        "268435399", // 28 bit SNT
    };

    const char* q_str[] = {
        "257",       // SNT
        "1013",      // SNT
        "4007",      // SNT
        "16007",     // SNT
        "65011",     // SNT
        "262147",    // SNT
        "1048583",   // SNT
        "4194319",   // SNT
        "16777259",  // SNT
        "67108879",  // SNT
        "268435459", // SNT
    };

    int N = 11;  // chạy 11 dòng

    for (int idx = 0; idx < N; idx++) {
        mpz_t p, q, n;
        mpz_inits(p, q, n, NULL);

        mpz_set_str(p, p_str[idx], 10);
        mpz_set_str(q, q_str[idx], 10);
        mpz_mul(n, p, q);

        int bits_n = mpz_sizeinbase(n, 2);
        unsigned long steps = 0;

        auto start = chrono::high_resolution_clock::now();

        mpz_t p_found, q_found;
        mpz_inits(p_found, q_found, NULL);
        int ok = trial_division(p_found, q_found, n, steps);

        auto end = chrono::high_resolution_clock::now();
        auto duration = chrono::duration_cast<chrono::microseconds>(end - start).count();

        cout << bits_n << "\t" << steps << "\t" << duration << endl;
        csv << bits_n << "," << steps << "," << duration << "\n";

        mpz_clears(p, q, n, p_found, q_found, NULL);

        // Nếu quá 10 giây thì dừng
        if (duration > 10000000) {
            cout << "[!] Qua lau, dung tai " << bits_n << " bit" << endl;
            break;
        }
    }

    csv.close();
    cout << "\n[+] Da ghi: results/benchmark.csv" << endl;
    return 0;
}
