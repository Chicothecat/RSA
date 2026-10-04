**Input bài toán: **
RSA bảo mật dựa trên độ phức tạp của bài toán phân tích thừa số nguyên
- Chiều xuôi: Khởi tạo n = p.q với p và q là hai số nguyên tố
- Chiều ngược: từ n giải mã ra p và q 

**Procedure:**

<img width="122" height="692" alt="FAT" src="https://github.com/user-attachments/assets/72e698aa-7f8b-44cf-a29d-c39df0f08bd9" />

- Lấy tham số: Thu thập $(n, e)$ từ khóa công khai
- Factor $n$: Tìm $p, q$ sao cho $p \times q = n$
- Tính Euler's totient: $\varphi(n) = (p - 1)(q - 1)$.
- Tìm số mũ bí mật $d$: Giải phương trình nghịch đảo modulo $d \equiv e^{-1} \pmod{\varphi(n)}$
- Khai thác:Giải mã ciphertext: $m = c^d \pmod n$
- Signature forgery: $\sigma = H(m)^d \pmod n$. 
