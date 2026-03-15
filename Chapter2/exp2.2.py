# 实验 2：模 m 剩余类环 Zₘ（对应：Zₘ 零因子、密码安全）
def zero_divisors(elements, mul):
    """找零因子：a≠0,b≠0 但 a*b=0"""
    zeros = []
    for a in elements:
        if a == 0:
            continue
        for b in elements:
            if b == 0:
                continue
            if mul(a, b) == 0:
                zeros.append((a,b))
    return zeros

def is_field(elements, add, mul):
    """是否是域：交换幺环 + 非零元都可逆"""
    ok, _ = is_ring(elements, add, mul)
    if not ok:
        return False

    # 单位元
    one = None
    for e in elements:
        if e == 0:
            continue
        if all(mul(a,e)==a for a in elements if a!=0):
            one = e
            break
    if one is None:
        return False

    # 逆元
    for a in elements:
        if a == 0:
            continue
        has_inv = any(mul(a,b)==one for b in elements)
        if not has_inv:
            return False
    return True

# ========== 学生实验：对比 Z6 和 Z7 ==========
m = 6
elements = list(range(m))
add = lambda a,b:(a+b)%m
mul = lambda a,b:(a*b)%m

print(f"Z{m} 零因子：", zero_divisors(elements, mul))
print(f"Z{m} 是域吗？", is_field(elements, add, mul))