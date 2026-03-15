"""
实验1：验证模n加法群/乘法群的群公理（封闭性、单位元、逆元、结合律）
对应讲义：群的四大公理、阿贝尔群
"""
def is_add_group(n):
    """验证模n加法群(Z_n, +)是否满足群公理"""
    print(f"=== 模{n}加法群(Z_{n}, +) 验证 ===")
    # 1. 封闭性验证
    closed = True
    for a in range(n):
        for b in range(n):
            if (a + b) % n not in range(n):
                closed = False
                break
    print(f"1. 封闭性：{'满足' if closed else '不满足'}")
    
    # 2. 单位元验证（加法单位元为0）
    unit = 0
    unit_valid = True
    for a in range(n):
        if (a + unit) % n != a or (unit + a) % n != a:
            unit_valid = False
            break
    print(f"2. 单位元({unit})：{'满足' if unit_valid else '不满足'}")
    
    # 3. 逆元验证（a的逆元为n-a）
    inverse_valid = True
    for a in range(n):
        inv = (-a) % n
        if (a + inv) % n != unit:
            inverse_valid = False
            break
    print(f"3. 逆元存在性：{'满足' if inverse_valid else '不满足'}")
    
    # 4. 结合律验证
    assoc_valid = True
    for a in range(n):
        for b in range(n):
            for c in range(n):
                left = (a + b) % n + c % n
                right = a + (b + c) % n % n
                if left % n != right % n:
                    assoc_valid = False
                    break
    print(f"4. 结合律：{'满足' if assoc_valid else '不满足'}")
    print(f"结论：Z_{n}加法群{'是' if all([closed, unit_valid, inverse_valid, assoc_valid]) else '不是'}合法群\n")

def is_mul_group(n):
    """验证模n乘法群(Z_n*, ×)是否满足群公理（仅含与n互质的元素）"""
    # 筛选与n互质的元素
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    elements = [x for x in range(n) if gcd(x, n) == 1]
    print(f"=== 模{n}乘法群(Z_{n}*, ×) 验证（元素：{elements}）===")
    
    # 1. 封闭性
    closed = True
    for a in elements:
        for b in elements:
            if (a * b) % n not in elements:
                closed = False
                break
    print(f"1. 封闭性：{'满足' if closed else '不满足'}")
    
    # 2. 单位元（乘法单位元为1）
    unit = 1
    unit_valid = unit in elements
    if unit_valid:
        for a in elements:
            if (a * unit) % n != a or (unit * a) % n != a:
                unit_valid = False
                break
    print(f"2. 单位元({unit})：{'满足' if unit_valid else '不满足'}")
    
    # 3. 逆元验证（扩展欧几里得算法）
    def extended_gcd(a, b):
        if b == 0:
            return (a, 1, 0)
        else:
            g, x, y = extended_gcd(b, a % b)
            return (g, y, x - (a // b) * y)
    
    inverse_valid = True
    for a in elements:
        g, x, _ = extended_gcd(a, n)
        inv = x % n
        if (a * inv) % n != 1:
            inverse_valid = False
            break
    print(f"3. 逆元存在性：{'满足' if inverse_valid else '不满足'}")
    
    # 4. 结合律
    assoc_valid = True
    for a in elements:
        for b in elements:
            for c in elements:
                left = (a * b) % n * c % n
                right = a * (b * c) % n % n
                if left % n != right % n:
                    assoc_valid = False
                    break
    print(f"4. 结合律：{'满足' if assoc_valid else '不满足'}")
    print(f"结论：Z_{n}乘法群{'是' if all([closed, unit_valid, inverse_valid, assoc_valid]) else '不是'}合法群\n")

# 测试案例（对应讲义例题）
is_add_group(5)   # 模5加法群（讲义例题2）
is_mul_group(7)   # 模7乘法群（讲义例题4）
is_mul_group(12)  # 模12乘法群（讲义例题5）