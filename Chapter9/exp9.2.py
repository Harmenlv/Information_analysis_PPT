# 实验2：不可约多项式验证与零因子检测
def is_irreducible_f2(poly, m):
    """
    验证F2[x]中m次多项式是否不可约（低次多项式专用）
    :param poly: 多项式的二进制表示（如x^2+x+1 → 0b111=7）
    :param m: 多项式次数
    :return: True=不可约，False=可约
    """
    # 1. 检查是否有根（二次/三次多项式：无根=不可约）
    if m <= 3:
        # 代入F2的所有元素（0和1）验证
        def eval_poly(x):
            res = 0
            bit = 0
            temp_poly = poly
            while temp_poly > 0:
                if temp_poly & 1:
                    res ^= (x ** bit)
                temp_poly >>= 1
                bit += 1
            return res % 2
        
        if eval_poly(0) == 0 or eval_poly(1) == 0:
            return False
        return True
    
    # 2. 更高次多项式（简化版：仅验证是否能被低次不可约多项式整除）
    # 生成所有次数≤m/2的不可约多项式（示例仅实现基础逻辑）
    irreducible_candidates = []
    for d in range(1, m//2 + 1):
        for p in range(2**d, 2**(d+1)):
            if bin(p).count('1') >= 2 and is_irreducible_f2(p, d):
                irreducible_candidates.append(p)
    
    # 多项式除法验证是否可约
    def poly_divide(a, b):
        """F2[x]多项式除法：a / b，返回商和余数"""
        q = 0
        while a >= b:
            shift = a.bit_length() - b.bit_length()
            q ^= (1 << shift)
            a ^= (b << shift)
        return q, a
    
    for p in irreducible_candidates:
        _, rem = poly_divide(poly, p)
        if rem == 0:
            return False
    return True

def detect_zero_divisor(irreducible_poly, m):
    """
    检测模多项式后的集合是否存在零因子
    :param irreducible_poly: 模多项式（二进制表示）
    :param m: 多项式次数
    :return: 零因子列表（空列表=无零因子）
    """
    zero_divisors = []
    # 遍历所有非零元素（次数<m的多项式）
    for a in range(1, 2**m):
        for b in range(1, 2**m):
            # 计算a*b mod irreducible_poly
            def poly_mult_mod(a_p, b_p, mod_p):
                res = 0
                temp_b = b_p
                shift = 0
                while temp_b > 0:
                    if temp_b & 1:
                        res ^= (a_p << shift)
                    temp_b >>= 1
                    shift += 1
                # 模约简
                while res.bit_length() > m:
                    highest_bit = res.bit_length() - 1
                    res ^= (mod_p << (highest_bit - m))
                return res
            
            product = poly_mult_mod(a, b, irreducible_poly)
            if product == 0:
                zero_divisors.append((a, b))
                break  # 找到一个即可退出
    return zero_divisors

# ===================== 测试用例 =====================
def test_irreducible_and_zero_divisor():
    # 测试用例1：不可约多项式（x^2+x+1=7）
    poly_irre = 0b111  # x^2+x+1
    m_irre = 2
    print("=== 测试用例1：不可约多项式 x^2+x+1 ===")
    print("是否不可约：", is_irreducible_f2(poly_irre, m_irre))
    print("零因子检测：", detect_zero_divisor(poly_irre, m_irre))  # 空列表=无零因子
    
    # 测试用例2：可约多项式（x^2+1=5）
    poly_reducible = 0b101  # x^2+1=(x+1)^2
    m_reducible = 2
    print("\n=== 测试用例2：可约多项式 x^2+1 ===")
    print("是否不可约：", is_irreducible_f2(poly_reducible, m_reducible))
    print("零因子检测：", detect_zero_divisor(poly_reducible, m_reducible))  # 存在零因子(3,3)
    
    # 测试用例3：SM2标准不可约多项式（x^256+x^128+x^9+x+1）
    poly_sm2 = (1 << 256) | (1 << 128) | (1 << 9) | (1 << 1) | 1
    m_sm2 = 256
    print("\n=== 测试用例3：SM2标准不可约多项式 ===")
    print("是否不可约（简化验证）：", is_irreducible_f2(poly_sm2, m_sm2))

if __name__ == "__main__":
    test_irreducible_and_zero_divisor()