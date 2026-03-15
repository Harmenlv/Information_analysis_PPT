"""
实验4：GCD/LCM 计算（辗转相除法+质因数分解法）
对应讲义：整除、GCD/LCM、几何直观
"""
def gcd_euclidean(a, b):
    """辗转相除法求GCD"""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """通过GCD求LCM：lcm(a,b) = |a*b| / gcd(a,b)"""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd_euclidean(a, b)

def gcd_lcm_prime(a, b):
    """质因数分解法求GCD/LCM（验证用）"""
    def prime_factorize(n):
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
    
    # 分解a和b
    fa = prime_factorize(a)
    fb = prime_factorize(b)
    
    # 计算GCD（取最小指数）
    gcd_factors = {}
    for p in fa:
        if p in fb:
            gcd_factors[p] = min(fa[p], fb[p])
    gcd_val = 1
    for p, exp in gcd_factors.items():
        gcd_val *= p ** exp
    
    # 计算LCM（取最大指数）
    lcm_factors = fa.copy()
    for p in fb:
        if p in lcm_factors:
            lcm_factors[p] = max(lcm_factors[p], fb[p])
        else:
            lcm_factors[p] = fb[p]
    lcm_val = 1
    for p, exp in lcm_factors.items():
        lcm_val *= p ** exp
    
    return {
        "a的质因数分解": fa,
        "b的质因数分解": fb,
        "GCD（质因数法）": gcd_val,
        "LCM（质因数法）": lcm_val,
        "验证GCD×LCM=|a×b|": gcd_val * lcm_val == abs(a * b)
    }

# 测试案例：讲义示例（a=12, b=18）
a, b = 12, 18
print(f"=== GCD/LCM 计算（a={a}, b={b}）===")
print(f"辗转相除法GCD：{gcd_euclidean(a, b)}")
print(f"LCM（通过GCD）：{lcm(a, b)}")
print(f"质因数分解法验证：")
result = gcd_lcm_prime(a, b)
for k, v in result.items():
    print(f"  {k}：{v}")

# 几何直观验证（GCD是能铺满矩形的最大正方形边长）
def gcd_geometric_verify(a, b):
    g = gcd_euclidean(a, b)
    width = a // g
    height = b // g
    print(f"\n=== GCD几何直观验证（{a}×{b}矩形）===")
    print(f"最大正方形边长：{g}")
    print(f"横向铺{width}个，纵向铺{height}个，总计{width×height}个正方形")
    print(f"验证：{g}×{width} = {a}, {g}×{height} = {b}")

gcd_geometric_verify(12, 18)