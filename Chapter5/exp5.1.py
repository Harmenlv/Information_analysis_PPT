# 实验1：原根判定（标准算法实现）
import math

def fast_pow(base, exponent, mod):
    """快速幂算法：计算 (base^exponent) mod mod，时间复杂度O(log exponent)"""
    result = 1
    base = base % mod
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        exponent = exponent >> 1
        base = (base * base) % mod
    return result

def prime_factorization(n):
    """素因子分解：返回n的所有不同素因子列表（用于原根判定）"""
    factors = set()
    if n % 2 == 0:
        factors.add(2)
        while n % 2 == 0:
            n = n // 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            factors.add(i)
            while n % i == 0:
                n = n // i
        i += 2
    if n > 2:
        factors.add(n)
    return list(factors)

def is_primitive_root(g, p):
    """
    判定g是否为模p的原根（p为素数）
    :param g: 候选原根
    :param p: 模数（素数）
    :return: True/False + 判定过程信息
    """
    if p <= 2 or g <= 1 or g >= p-1:
        return False, "候选元需满足 2 ≤ g ≤ p-2"
    
    phi_p = p - 1  # 素数p的欧拉函数φ(p)=p-1
    prime_factors = prime_factorization(phi_p)
    
    # 核心判定逻辑：对所有素因子q，验证g^(φ(p)/q) ≢ 1 mod p
    for q in prime_factors:
        exponent = phi_p // q
        res = fast_pow(g, exponent, p)
        if res == 1:
            return False, f"g^({phi_p}/{q}) ≡ 1 mod {p}，阶<{phi_p}，非原根"
    
    return True, f"所有素因子验证通过，{g}是模{p}的原根"

# 测试用例（对应课件例题）
if __name__ == "__main__":
    # 例1：验证3是否为模7的原根
    g1, p1 = 3, 7
    is_root1, info1 = is_primitive_root(g1, p1)
    print(f"测试1：g={g1}, p={p1} → {'是原根' if is_root1 else '非原根'}，{info1}")
    
    # 例2：验证2是否为模7的原根（反例）
    g2, p2 = 2, 7
    is_root2, info2 = is_primitive_root(g2, p2)
    print(f"测试2：g={g2}, p={p2} → {'是原根' if is_root2 else '非原根'}，{info2}")
    
    # 例3：验证5是否为模23的原根（课件例题）
    g3, p3 = 5, 23
    is_root3, info3 = is_primitive_root(g3, p3)
    print(f"测试3：g={g3}, p={p3} → {'是原根' if is_root3 else '非原根'}，{info3}")