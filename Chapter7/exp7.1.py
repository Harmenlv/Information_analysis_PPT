# 实验1：有限循环群与离散对数基础验证
import math

def extended_gcd(a, b):
    """扩展欧几里得算法，用于求模逆"""
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def mod_inverse(a, m):
    """计算a在模m下的逆元"""
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise Exception('模逆不存在')
    else:
        return x % m

def euler_phi(n):
    """计算欧拉函数φ(n)"""
    result = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            result -= result // i
        i += 1
    if n > 1:
        result -= result // n
    return result

def is_primitive_root(g, n):
    """验证g是否是模n乘法群的生成元（原根）"""
    if math.gcd(g, n) != 1:
        return False
    phi = euler_phi(n)
    factors = set()
    temp = phi
    i = 2
    while i * i <= temp:
        if temp % i == 0:
            factors.add(i)
            while temp % i == 0:
                temp //= i
        i += 1
    if temp > 1:
        factors.add(temp)
    
    for p in factors:
        if pow(g, phi // p, n) == 1:
            return False
    return True

def discrete_log_brute_force(g, h, mod):
    """暴力枚举求解离散对数log_g h mod mod"""
    phi = euler_phi(mod)
    current = 1
    for k in range(phi):
        if current == h % mod:
            return k
        current = (current * g) % mod
    return None

# 实验步骤1：验证模18乘法群的基本性质
mod = 18
phi_18 = euler_phi(mod)
print(f"1. 模{mod}的欧拉函数φ({mod}) = {phi_18}")

# 实验步骤2：验证5是模18的生成元
g = 5
is_gen = is_primitive_root(g, mod)
print(f"2. {g}是否是模{mod}的生成元：{is_gen}")

# 实验步骤3：生成模18乘法群的离散对数表
print("\n3. 模18乘法群（生成元5）的离散对数表：")
log_table = {}
for k in range(phi_18):
    val = pow(g, k, mod)
    log_table[val] = k
    print(f"   log_5({val}) = {k}")

# 实验步骤4：验证离散对数的加法性质
h1, h2 = 7, 13
k1 = log_table[h1]
k2 = log_table[h2]
product = (h1 * h2) % mod
k_product = log_table[product]
sum_k = (k1 + k2) % phi_18
print(f"\n4. 验证加法性质：log_5({h1}*{h2}) = log_5({h1}) + log_5({h2}) mod {phi_18}")
print(f"   log_5({h1}) = {k1}, log_5({h2}) = {k2}, 和 = {sum_k}")
print(f"   {h1}*{h2} mod {mod} = {product}, log_5({product}) = {k_product}")
print(f"   验证结果：{sum_k == k_product}")

# 实验步骤5：暴力求解离散对数示例
target = 11
k = discrete_log_brute_force(g, target, mod)
print(f"\n5. 求解log_5({target}) mod {mod} = {k}")
print(f"   验证：5^{k} mod {mod} = {pow(g, k, mod)}")