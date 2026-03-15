# 实验2：模素数原根数量计算与枚举
import math

# 复用实验1的工具函数：fast_pow, prime_factorization, is_primitive_root

def euler_phi(n):
    """计算欧拉函数φ(n)：返回1~n中与n互素的数的个数"""
    if n == 0:
        return 0
    result = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n = n // i
            result -= result // i
        i += 1
    if n > 1:
        result -= result // n
    return result

def count_primitive_roots(p):
    """计算模素数p的原根数量（φ(p-1)）"""
    if p <= 2:
        return 0 if p == 2 else 1
    return euler_phi(p-1)

def enumerate_primitive_roots(p):
    """枚举模素数p的所有原根"""
    roots = []
    for g in range(2, p-1):
        is_root, _ = is_primitive_root(g, p)
        if is_root:
            roots.append(g)
    return roots

# 测试用例（对应课件例题）
if __name__ == "__main__":
    # 例1：模7的原根数量与枚举
    p1 = 7
    count1 = count_primitive_roots(p1)
    roots1 = enumerate_primitive_roots(p1)
    print(f"模{p1}的原根数量：{count1}（φ({p1-1})={euler_phi(p1-1)}）")
    print(f"模{p1}的所有原根：{roots1}")
    
    # 例2：模11的原根数量与枚举
    p2 = 11
    count2 = count_primitive_roots(p2)
    roots2 = enumerate_primitive_roots(p2)
    print(f"\n模{p2}的原根数量：{count2}（φ({p2-1})={euler_phi(p2-1)}）")
    print(f"模{p2}的所有原根：{roots2}")