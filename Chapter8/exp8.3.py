# 实验3：有限域椭圆曲线点加法与倍点运算
def mod_inverse(x, p):
    """计算模p逆元（扩展欧几里得算法），x与p互质"""
    try:
        return pow(x, -1, p)
    except ValueError:
        return None  # 无逆元（x≡0 mod p）

def ec_point_add(p1, p2, a, p):
    """
    有限域F_p上椭圆曲线点加法：P1⊕P2
    :param p1: 点1 (x1,y1)，"O"表示无穷远点
    :param p2: 点2 (x2,y2)，"O"表示无穷远点
    :param a: 椭圆曲线参数y²=x³+ax+b
    :param p: 有限域素数
    :return: 相加结果 (x3,y3) 或 "O"
    """
    # 处理无穷远点
    if p1 == "O":
        return p2
    if p2 == "O":
        return p1
    
    x1, y1 = p1
    x2, y2 = p2
    
    # 处理逆元情况：P2=-P1 → 结果为无穷远点
    if x1 == x2 and y2 == (p - y1) % p:
        return "O"
    
    # 计算斜率λ
    if p1 != p2:
        # 点加法（P≠Q）
        dx = (x2 - x1) % p
        dy = (y2 - y1) % p
        inv_dx = mod_inverse(dx, p)
        if inv_dx is None:
            return "O"  # 理论上不会出现（已处理逆元情况）
        lam = (dy * inv_dx) % p
    else:
        # 倍点运算（P=Q）
        if y1 == 0:
            return "O"  # 切线垂直x轴，结果为无穷远点
        numerator = (3 * pow(x1, 2, p) + a) % p
        denominator = (2 * y1) % p
        inv_den = mod_inverse(denominator, p)
        if inv_den is None:
            return "O"
        lam = (numerator * inv_den) % p
    
    # 计算x3, y3
    x3 = (pow(lam, 2, p) - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    
    return (x3, y3)

# 测试用例：F_7上y²=x³+2x+3的点运算
a, p = 2, 7
P = (2, 1)
Q = (3, 1)

# 测试1：点加法 P⊕Q
print("=== 测试1：点加法 (2,1)⊕(3,1) ===")
R = ec_point_add(P, Q, a, p)
print(f"结果：{R}（预期：(2,6)）")

# 测试2：倍点运算 2P = P⊕P
print("\n=== 测试2：倍点运算 2*(2,1) ===")
double_P = ec_point_add(P, P, a, p)
print(f"结果：{double_P}（预期：(3,6)）")

# 测试3：逆元验证 P⊕(-P)
print("\n=== 测试3：逆元验证 (2,1)⊕(2,6) ===")
neg_P = (2, 6)
inv_test = ec_point_add(P, neg_P, a, p)
print(f"结果：{inv_test}（预期：O）")