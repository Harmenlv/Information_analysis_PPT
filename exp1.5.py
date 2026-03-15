"""
实验5：循环群同构性验证（模乘法群 → 模加法群）
对应讲义：有限循环群同构定理、密码运算化简
"""
def cyclic_group_isomorphism(p, g):
    """
    验证模p乘法群（生成元g）与模(p-1)加法群的同构性
    映射：f(g^k) = k mod (p-1)
    """
    # 1. 确认模p乘法群是循环群（p为素数）
    if not is_prime(p):
        return "p必须是素数，模p乘法群才是循环群"
    
    # 2. 确认g是生成元
    def is_primitive_root(g, p):
        n = p - 1
        factors = factorize(n)
        for q in factors:
            if pow(g, n//q, p) == 1:
                return False
        return True
    
    if not is_primitive_root(g, p):
        return f"{g}不是模{p}乘法群的生成元"
    
    # 3. 构建映射表（g^k mod p ↔ k mod (p-1)）
    n = p - 1  # 循环群阶
    mul_to_add = {}  # 乘法群元素 → 加法群元素
    add_to_mul = {}  # 加法群元素 → 乘法群元素
    
    current = 1  # g^0 mod p
    for k in range(n):
        mul_to_add[current] = k
        add_to_mul[k] = current
        current = (current * g) % p
    
    # 4. 验证同构性（运算保持）
    # 随机选两个元素测试
    import random
    k1 = random.randint(0, n-1)
    k2 = random.randint(0, n-1)
    
    # 乘法群运算：g^k1 * g^k2 mod p = g^(k1+k2) mod p
    mul_result = (add_to_mul[k1] * add_to_mul[k2]) % p
    # 加法群运算：k1 + k2 mod n
    add_result = (k1 + k2) % n
    # 验证映射保持：f(mul_result) = add_result
    is_isomorphic = mul_to_add[mul_result] == add_result
    
    return {
        "循环群阶": n,
        "生成元": g,
        "映射表（乘法→加法）": mul_to_add,
        "测试用例": {
            "k1": k1, "k2": k2,
            "乘法群运算": f"{add_to_mul[k1]} * {add_to_mul[k2]} mod {p} = {mul_result}",
            "加法群运算": f"{k1} + {k2} mod {n} = {add_result}",
            "映射保持": is_isomorphic
        },
        "结论": "同构性成立，乘法运算可化简为加法运算" if is_isomorphic else "同构性不成立"
    }

# 辅助函数（复用实验3）
def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0:
        return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in [2, 3, 5]:
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

def factorize(n):
    factors = set()
    while n % 2 == 0:
        factors.add(2)
        n = n // 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.add(i)
            n = n // i
        i += 2
    if n > 2:
        factors.add(n)
    return factors

# 测试案例：模7乘法群（生成元3）与模6加法群同构
result = cyclic_group_isomorphism(7, 3)
print("=== 循环群同构性验证 ===")
for k, v in result.items():
    if isinstance(v, dict):
        print(f"{k}：")
        for k2, v2 in v.items():
            print(f"  {k2}：{v2}")
    else:
        print(f"{k}：{v2}")