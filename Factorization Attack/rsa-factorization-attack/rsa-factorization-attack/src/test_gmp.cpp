#include <iostream>
#include <gmp.h>

using namespace std;

int main() {
    mpz_t a;
    mpz_init(a);
    mpz_set_str(a, "12345678901234567890", 10);

    cout << "GMP is working." << endl;
    cout << "Number: ";
    mpz_out_str(stdout, 10, a);
    cout << endl;

    mpz_clear(a);
    return 0;
}
