"""
实验3：循环群生成元（原根）求解
对应讲义：循环群、DH密钥交换、安全素数选择
"""
def factorize(n):
    """质因数分解（简单版，适配小整数）"""
    factors = {}
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n = n // 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n = n // i
        i += 2
    if n > 2:
        factors[n] = 1
    return factors

def is_primitive_root(g, p):
    """
    判断g是否是模p乘法群Z_p*的生成元（原根）
    条件：g^((p-1)/q) ≢ 1 mod p 对p-1的所有素因子q成立
    """
    if gcd(g, p) != 1:
        return False
    
    # 分解p-1的素因子
    n = p - 1
    factors = factorize(n)
    prime_factors = list(factors.keys())
    
    # 验证生成元条件
    for q in prime_factors:
        exponent = n // q
        if pow(g, exponent, p) == 1:
            return False
    return True

def find_all_primitive_roots(p):
    """找出模p乘法群的所有生成元"""
    if not is_prime(p):  # 仅素数模的乘法群是循环群
        return "仅素数模的乘法群是循环群，无生成元"
    
    roots = []
    for g in range(2, p):
        if is_primitive_root(g, p):
            roots.append(g)
    return roots

# 辅助函数：素数判断（米勒-拉宾）
def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0:
        return False
    # 米勒-拉宾测试
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    # 测试用例（小整数足够）
    for a in [2, 3, 5, 7, 11]:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# 测试案例：讲义例题4（模7乘法群生成元）
p = 7
roots = find_all_primitive_roots(p)
print(f"=== 模{p}乘法群的生成元 ===")
print(f"所有生成元：{roots}")
print(f"验证生成元3：{pow(3, 6, 7)} = 1（群阶6）")
print(f"验证生成元5：{pow(5, 6, 7)} = 1（群阶6）")