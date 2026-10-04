#include <iostream>
#include <gmp.h>

using namespace std;

void compute_phi(mpz_t phi, const mpz_t p, const mpz_t q) {
    mpz_t p1, q1;
    mpz_inits(p1, q1, NULL);
    mpz_sub_ui(p1, p, 1);
    mpz_sub_ui(q1, q, 1);
    mpz_mul(phi, p1, q1);
    mpz_clears(p1, q1, NULL);
}

int main() {
    mpz_t p, q, n, phi, e, d;
    mpz_inits(p, q, n, phi, e, d, NULL);

    mpz_set_ui(p, 10007);
    mpz_set_ui(q, 10009);

    mpz_mul(n, p, q);
    gmp_printf("p = %Zd\n", p);
    gmp_printf("q = %Zd\n", q);
    gmp_printf("n = p*q = %Zd\n\n", n);

    compute_phi(phi, p, q);
    gmp_printf("phi(n) = %Zd\n", phi);

    mpz_set_ui(e, 65537);
    gmp_printf("e = %Zd\n", e);

    mpz_invert(d, e, phi);
    gmp_printf("d = %Zd\n\n", d);

    unsigned long msg = 12345;
    mpz_t m, c;
    mpz_inits(m, c, NULL);
    mpz_set_ui(m, msg);
    mpz_powm(c, m, e, n);

    gmp_printf("Message (m)   = %Zd\n", m);
    gmp_printf("Ciphertext(c) = %Zd\n\n", c);

    cout << "===== PUBLIC KEY (attacker biet) =====" << endl;
    gmp_printf("n = %Zd\n", n);
    gmp_printf("e = %Zd\n", e);
    gmp_printf("c = %Zd\n\n", c);

    cout << "===== SECRET (attacker KHONG biet) =====" << endl;
    gmp_printf("p = %Zd\n", p);
    gmp_printf("q = %Zd\n", q);
    gmp_printf("d = %Zd\n", d);

    mpz_clears(p, q, n, phi, e, d, m, c, NULL);
    return 0;
}

