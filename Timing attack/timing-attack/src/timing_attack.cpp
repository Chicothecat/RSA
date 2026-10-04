#include <iostream>
#include <fstream>
#include <chrono>
#include <string>

using namespace std;
using namespace chrono;

const string SECRET = "secret123";

// Hàm KHÔNG an toàn: thoát sớm khi gặp ký tự sai
// Thêm vòng lặp busy để kéo dài thời gian mỗi nhánh
__attribute__((noinline))
bool check_unsafe(const string& input) {
    for (size_t i = 0; i < SECRET.size(); i++) {
        // busy work cố định mỗi vòng
        volatile int dummy = 0;
        for (int k = 0; k < 10000; k++) dummy += k;

        if (i >= input.size() || input[i] != SECRET[i])
            return false;
    }
    return input.size() == SECRET.size();
}

// Hàm AN TOÀN: luôn chạy hết
__attribute__((noinline))
bool check_safe(const string& input) {
    bool len_ok = (input.size() == SECRET.size());
    int diff = 0;
    for (size_t i = 0; i < SECRET.size(); i++) {
        volatile int dummy = 0;
        for (int k = 0; k < 10000; k++) dummy += k;

        char a = (i < input.size()) ? input[i] : 0;
        char b = SECRET[i];
        diff |= (a ^ b);
    }
    return len_ok && (diff == 0);
}

long long measure(bool (*fn)(const string&), const string& input, int reps) {
    auto start = high_resolution_clock::now();
    for (int r = 0; r < reps; r++) {
        volatile bool res = fn(input);
        (void)res;
    }
    auto end = high_resolution_clock::now();
    return duration_cast<nanoseconds>(end - start).count() / reps;
}

int main() {
    ofstream csv("results/timing_result.csv");
    csv << "input,prefix_correct,time_unsafe_ns,time_safe_ns\n";

    int reps = 1000;

    string inputs[] = {
        "x", "s", "se", "sec", "secr", "secre", "secret",
        "secret1", "secret12", "secret123"
    };

    cout << "input\t\tprefix\ttime_unsafe\ttime_safe" << endl;

    for (const string& inp : inputs) {
        long long t_unsafe = measure(check_unsafe, inp, reps);
        long long t_safe = measure(check_safe, inp, reps);

        int prefix = 0;
        for (size_t i = 0; i < inp.size() && i < SECRET.size(); i++) {
            if (inp[i] == SECRET[i]) prefix++;
            else break;
        }

        cout << inp << "\t\t" << prefix << "\t"
             << t_unsafe << "\t\t" << t_safe << endl;

        csv << inp << "," << prefix << ","
            << t_unsafe << "," << t_safe << "\n";
    }

    csv.close();
    cout << "\nDa ghi: results/timing_result.csv" << endl;
    return 0;
}
