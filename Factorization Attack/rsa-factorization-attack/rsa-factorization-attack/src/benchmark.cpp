#include <iostream>
#include <fstream>
#include <gmp.h>
#include <chrono>
#include <cstdlib>

using namespace std;

// Trial Division: tìm ước nhỏ nhất của n
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

// Sinh số nguyên tố ngẫu nhiên gần đúng với số bit cho trước (dùng cho test)
// KHÔNG cần primality test chính xác — chỉ cần số lẻ đủ lớn
void gen_odd(mpz_t out, int bits) {
    mpz_t low, high;
    mpz_inits(low, high, NULL);

    // low = 2^(bits-1), high = 2^bits
    mpz_ui_pow_ui(low, 2, bits - 1);
    mpz_ui_pow_ui(high, 2, bits);

    gmp_randstate_t state;
    gmp_randinit_mt(state);
    gmp_randseed_ui(state, time(NULL) + bits);

    mpz_urandomm(out, state, high);
    mpz_add(out, out, low);

    // Đảm bảo là số lẻ
    if (mpz_even_p(out)) {
        mpz_add_ui(out, out, 1);
    }

    gmp_randclear(state);
    mpz_clears(low, high, NULL);
}

int main() {
    ofstream csv("results/benchmark.csv");
    csv << "bits_p,bits_q,bits_n,steps,time_us,status\n";

    cout << "===== BENCHMARK FACTORIZATION =====" << endl;
    cout << "bits_n\tsteps\ttime_us" << endl;

    // Test từ 8 bit đến 24 bit (có thể tăng nếu muốn)
    int sizes[] = {8, 10, 12, 14, 16, 18, 20, 22, 24};

    for (int bits : sizes) {
        mpz_t p, q, n;
        mpz_inits(p, q, n, NULL);

        gen_odd(p, bits);
        gen_odd(q, bits);
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

        csv << bits << "," << bits << "," << bits_n << ","
            << steps << "," << duration << ","
            << (ok ? "ok" : "fail") << "\n";

        mpz_clears(p, q, n, p_found, q_found, NULL);
    }

    csv.close();
    cout << "\n[+] Da ghi ket qua vao: results/benchmark.csv" << endl;

    return 0;
}

