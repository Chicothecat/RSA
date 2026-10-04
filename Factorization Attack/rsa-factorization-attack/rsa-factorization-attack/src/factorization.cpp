#include <iostream>
#include <gmp.h>
#include <chrono>

using namespace std;

// Trial Division: thử chia n cho 2, 3, 5, 7, ... đến sqrt(n)
int trial_division(mpz_t p, mpz_t q, const mpz_t n) {
    mpz_t i, rem, limit;
    mpz_inits(i, rem, limit, NULL);

    // limit = sqrt(n)
    mpz_sqrt(limit, n);

    // Thử từ 2 trở đi
    mpz_set_ui(i, 2);

    while (mpz_cmp(i, limit) <= 0) {
        mpz_mod(rem, n, i);
        if (mpz_cmp_ui(rem, 0) == 0) {
            // Tìm thấy ước!
            mpz_set(p, i);
            mpz_divexact(q, n, i);  // q = n / i
            mpz_clears(i, rem, limit, NULL);
            return 1;  // success
        }
        mpz_add_ui(i, i, 1);
    }

    mpz_clears(i, rem, limit, NULL);
    return 0;  // fail
}

int main() {
    // ========== CHỈ BIẾT PUBLIC INFO ==========
    mpz_t n, e, c;
    mpz_inits(n, e, c, NULL);

    mpz_set_str(n, "100160063", 10);
    mpz_set_ui(e, 65537);
    mpz_set_str(c, "85109818", 10);

    cout << "===== ATTACKER CHI BIET =====" << endl;
    gmp_printf("n = %Zd\n", n);
    gmp_printf("e = %Zd\n", e);
    gmp_printf("c = %Zd\n\n", c);

    // ========== BƯỚC 1: FACTOR n ==========
    cout << "[*] Dang factor n..." << endl;

    auto start = chrono::high_resolution_clock::now();

    mpz_t p, q;
    mpz_inits(p, q, NULL);

    if (!trial_division(p, q, n)) {
        cout << "[-] That bai!" << endl;
        return 1;
    }

    auto end = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::microseconds>(end - start).count();

    cout << "[+] Tim thay uoc!" << endl;
    gmp_printf("    p = %Zd\n", p);
    gmp_printf("    q = %Zd\n", q);
    cout << "    Thoi gian: " << duration << " microseconds\n\n";

    // ========== BƯỚC 2: Tinh phi(n) ==========
    mpz_t phi, p1, q1;
    mpz_inits(phi, p1, q1, NULL);
    mpz_sub_ui(p1, p, 1);
    mpz_sub_ui(q1, q, 1);
    mpz_mul(phi, p1, q1);
    gmp_printf("[*] phi(n) = %Zd\n", phi);

    // ========== BƯỚC 3: Tinh d = e^(-1) mod phi(n) ==========
    mpz_t d;
    mpz_init(d);
    mpz_invert(d, e, phi);
    gmp_printf("[*] d = %Zd\n\n", d);

    // ========== BƯỚC 4: Decrypt m = c^d mod n ==========
    mpz_t m;
    mpz_init(m);
    mpz_powm(m, c, d, n);
    gmp_printf("[+] Decrypted message = %Zd\n", m);

    if (mpz_cmp_ui(m, 12345) == 0) {
        cout << "\n[SUCCESS] Attack thanh cong! m = 12345 (dung)" << endl;
    } else {
        cout << "\n[FAIL] m khong dung!" << endl;
    }

    mpz_clears(n, e, c, p, q, phi, p1, q1, d, m, NULL);
    return 0;
}

