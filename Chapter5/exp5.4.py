# 实验4：安全素数下的原根快速判定
import math

# 复用实验1的fast_pow函数
def fast_pow(base, exponent, mod):
    result = 1
    base = base % mod
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        exponent = exponent >> 1
        base = (base * base) % mod
    return result

def is_safe_prime(p):
    """判定p是否为安全素数（p=2q+1，q为素数）"""
    if p <= 2 or (p-1) % 2 != 0:
        return False, 0
    q = (p - 1) // 2
    # 简单素性检测（仅用于演示，工程中需用Miller-Rabin）
    if q < 2:
        return False, 0
    for i in range(2, int(math.sqrt(q)) + 1):
        if q % i == 0:
            return False, 0
    return True, q

def fast_primitive_root_check(g, p):
    """
    安全素数下的原根快速判定（仅需2次模幂）
    :param g: 候选原根
    :param p: 安全素数
    :return: True/False
    """
    is_safe, q = is_safe_prime(p)
    if not is_safe:
        raise ValueError(f"{p}不是安全素数，无法使用快速判定")
    
    # 安全素数p=2q+1，仅需验证：g^2 ≢1 mod p 且 g^q ≢1 mod p
    if fast_pow(g, 2, p) == 1:
        return False
    if fast_pow(g, q, p) == 1:
        return False
    return True

# 测试用例（对应课件安全素数例题：p=23=2×11+1）
if __name__ == "__main__":
    # 例1：验证p=23是否为安全素数
    p = 23
    is_safe, q = is_safe_prime(p)
    print(f"p={p}是否为安全素数：{'是' if is_safe else '否'}，q={q}")
    
    # 例2：快速判定g=5是否为模23的原根
    g = 5
    is_root = fast_primitive_root_check(g, p)
    print(f"\n快速判定g={g}是否为模{p}的原根：{'是' if is_root else '否'}")
    
    # 例3：对比标准判定与快速判定的效率（大数场景）
    import time
    # 模拟2048位安全素数（简化演示，实际需生成大数）
    p_large = 2 * 1000003 + 1  # 模拟安全素数
    g_large = 3
    
    # 快速判定耗时
    start = time.time()
    res_fast = fast_primitive_root_check(g_large, p_large)
    fast_time = time.time() - start
    
    # 标准判定耗时（复用实验1的is_primitive_root）
    from 实验1 import is_primitive_root
    start = time.time()
    res_standard, _ = is_primitive_root(g_large, p_large)
    standard_time = time.time() - start
    
    print(f"\n大数场景效率对比（p={p_large}）：")
    print(f"快速判定耗时：{fast_time:.6f}秒，结果：{res_fast}")
    print(f"标准判定耗时：{standard_time:.6f}秒，结果：{res_standard}")
    print(f"效率提升：{standard_time/fast_time:.2f}倍")