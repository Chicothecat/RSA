#include <iostream>
#include <fstream>
#include <gmp.h>

using namespace std;

mpz_t g_d, g_n, g_c_target;
int g_blocked = 0;

void oracle_init(const mpz_t d, const mpz_t n, const mpz_t c_target) {
    mpz_inits(g_d, g_n, g_c_target, NULL);
    mpz_set(g_d, d);
    mpz_set(g_n, n);
    mpz_set(g_c_target, c_target);
}

int oracle_decrypt(mpz_t m_out, const mpz_t c_in) {
    if (mpz_cmp(c_in, g_c_target) == 0) {
        g_blocked++;
        return 0;
    }
    mpz_powm(m_out, c_in, g_d, g_n);
    return 1;
}

int main() {
    // Mở file CSV
    ofstream csv("results/cca_result.csv");
    csv << "step,param,value\n";

    // ===== SETUP =====
    mpz_t p, q, n, phi, e, d;
    mpz_inits(p, q, n, phi, e, d, NULL);

    mpz_set_ui(p, 10007);
    mpz_set_ui(q, 10009);
    mpz_mul(n, p, q);

    mpz_t p1, q1;
    mpz_inits(p1, q1, NULL);
    mpz_sub_ui(p1, p, 1);
    mpz_sub_ui(q1, q, 1);
    mpz_mul(phi, p1, q1);

    mpz_set_ui(e, 65537);
    mpz_invert(d, e, phi);

    cout << "===== SETUP =====" << endl;
    gmp_printf("n = %Zd\n", n);
    gmp_printf("e = %Zd\n", e);
    gmp_printf("d = %Zd (BIMAT)\n\n", d);

    csv << "setup,n," << mpz_get_str(NULL, 10, n) << "\n";
    csv << "setup,e," << mpz_get_str(NULL, 10, e) << "\n";
    csv << "setup,d," << mpz_get_str(NULL, 10, d) << "\n";

    // ===== MỤC TIÊU =====
    unsigned long msg = 12345;
    mpz_t m_target, c_target;
    mpz_inits(m_target, c_target, NULL);
    mpz_set_ui(m_target, msg);
    mpz_powm(c_target, m_target, e, n);

    cout << "===== MUC TIEU =====" << endl;
    gmp_printf("m* = %Zd (BIMAT)\n", m_target);
    gmp_printf("c* = %Zd\n\n", c_target);

    csv << "target,m_star," << mpz_get_str(NULL, 10, m_target) << "\n";
    csv << "target,c_star," << mpz_get_str(NULL, 10, c_target) << "\n";

    oracle_init(d, n, c_target);

    // ===== TẤN CÔNG =====
    cout << "===== TAN CONG CCA =====" << endl;

    mpz_t s, c_prime, s_pow_e;
    mpz_inits(s, c_prime, s_pow_e, NULL);
    mpz_set_ui(s, 2);

    mpz_powm(s_pow_e, s, e, n);
    mpz_mul(c_prime, c_target, s_pow_e);
    mpz_mod(c_prime, c_prime, n);

    cout << "Buoc 1: Blinding" << endl;
    gmp_printf("  s   = %Zd\n", s);
    gmp_printf("  c'  = %Zd\n\n", c_prime);

    csv << "step1,s," << mpz_get_str(NULL, 10, s) << "\n";
    csv << "step1,c_prime," << mpz_get_str(NULL, 10, c_prime) << "\n";

    mpz_t m_prime;
    mpz_init(m_prime);

    cout << "Buoc 2: Gui c' cho oracle..." << endl;
    if (!oracle_decrypt(m_prime, c_prime)) {
        cout << "  [X] Oracle tu choi!" << endl;
        csv << "step2,status,BLOCKED\n";
        csv.close();
        return 1;
    }
    cout << "  [OK] Oracle da tra loi" << endl;
    gmp_printf("  m'  = %Zd\n\n", m_prime);

    csv << "step2,m_prime," << mpz_get_str(NULL, 10, m_prime) << "\n";

    mpz_t s_inv, m_recovered;
    mpz_inits(s_inv, m_recovered, NULL);
    mpz_invert(s_inv, s, n);
    mpz_mul(m_recovered, m_prime, s_inv);
    mpz_mod(m_recovered, m_recovered, n);

    cout << "Buoc 3: Khoi phuc m*" << endl;
    gmp_printf("  s^-1 = %Zd\n", s_inv);
    gmp_printf("  m*   = %Zd\n\n", m_recovered);

    csv << "step3,s_inv," << mpz_get_str(NULL, 10, s_inv) << "\n";
    csv << "step3,m_recovered," << mpz_get_str(NULL, 10, m_recovered) << "\n";

    // ===== KẾT QUẢ =====
    cout << "===== KET QUA =====" << endl;
    if (mpz_cmp(m_recovered, m_target) == 0) {
        cout << "[SUCCESS] m* = 12345 (dung!)" << endl;
        csv << "result,status,SUCCESS\n";
    } else {
        cout << "[FAIL]" << endl;
        csv << "result,status,FAIL\n";
    }

    cout << "\nOracle blocked: " << g_blocked << endl;
    csv << "oracle,blocked," << g_blocked << "\n";

    csv.close();
    cout << "\n[+] Da ghi: results/cca_result.csv" << endl;

    mpz_clears(p, q, n, phi, e, d, p1, q1, m_target, c_target,
               s, c_prime, s_pow_e, m_prime, s_inv, m_recovered, NULL);
    return 0;
}
