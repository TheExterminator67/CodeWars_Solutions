MOD = 998244353

def height(n, m):
    if n <= 0 or m <= 0:
        return 0

    
    m0 = m % MOD
    if m0 == 0:
        return 0

    kmax = n if n < m0 else m0 

   
    if n >= m0:
        return (pow(2, m0, MOD) - 1) % MOD

    
    inv = [0] * (kmax + 1)
    inv[1] = 1
    for i in range(2, kmax + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    
    c = 1
    s = 0
    for k in range(1, kmax + 1):
        c = (c * (m0 - k + 1)) % MOD
        c = (c * inv[k]) % MOD
        s += c
    return s % MOD