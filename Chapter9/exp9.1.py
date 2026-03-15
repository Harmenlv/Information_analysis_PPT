# 实验1：素域Fp与二进制域F2^m运算效率对比
import time
import random

# ===================== 素域Fp运算实现 =====================
def fp_add(a, b, p):
    """素域加法：大整数模加（带进位）"""
    return (a + b) % p

def fp_mult(a, b, p):
    """素域乘法：大整数模乘（带约简）"""
    return (a * b) % p

# ===================== 二进制域F2^m运算实现 =====================
def f2m_add(a, b):
    """二进制域加法：无进位XOR"""
    return a ^ b

def f2m_mult(a, b, m, irreducible_poly):
    """二进制域乘法：移位+XOR（模不可约多项式）"""
    result = 0
    while b > 0:
        if b & 1:
            result ^= a
        a <<= 1
        # 模不可约多项式截断（仅保留低m位）
        if (a >> m) & 1:
            a ^= irreducible_poly
        b >>= 1
    return result & ((1 << m) - 1)

# ===================== 效率对比测试 =====================
def test_performance():
    # 测试参数：256位素域 vs 256位二进制域
    # 256位素数（示例，实际用NIST标准素数）
    p_256 = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
    # 256位二进制域不可约多项式（SM2标准：x^256 + x^128 + x^9 + x + 1）
    m_256 = 256
    irr_poly_256 = (1 << 256) | (1 << 128) | (1 << 9) | (1 << 1) | 1
    
    # 生成测试数据
    test_count = 1000
    fp_data = [(random.randint(1, p_256-1), random.randint(1, p_256-1)) for _ in range(test_count)]
    f2m_data = [(random.randint(1, (1<<m_256)-1), random.randint(1, (1<<m_256)-1)) for _ in range(test_count)]
    
    # 素域加法耗时
    start = time.time()
    for a, b in fp_data:
        fp_add(a, b, p_256)
    fp_add_time = time.time() - start
    
    # 素域乘法耗时
    start = time.time()
    for a, b in fp_data:
        fp_mult(a, b, p_256)
    fp_mult_time = time.time() - start
    
    # 二进制域加法耗时
    start = time.time()
    for a, b in f2m_data:
        f2m_add(a, b)
    f2m_add_time = time.time() - start
    
    # 二进制域乘法耗时
    start = time.time()
    for a, b in f2m_data:
        f2m_mult(a, b, m_256, irr_poly_256)
    f2m_mult_time = time.time() - start
    
    # 输出结果
    print("=== 256位有限域运算效率对比（{}次运算）===".format(test_count))
    print("素域Fp加法耗时：{:.6f}秒".format(fp_add_time))
    print("二进制域F2^m加法耗时：{:.6f}秒（提速{:.2f}倍）".format(f2m_add_time, fp_add_time/f2m_add_time))
    print("素域Fp乘法耗时：{:.6f}秒".format(fp_mult_time))
    print("二进制域F2^m乘法耗时：{:.6f}秒（提速{:.2f}倍）".format(f2m_mult_time, fp_mult_time/f2m_mult_time))

if __name__ == "__main__":
    test_performance()