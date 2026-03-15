# 实验 1：验证一个集合是不是环（对应：环的公理化定义）
def is_ring(elements, add, mul):
    """
    验证 (elements, add, mul) 是否是环
    对应 PPT：环的三大公理
    1. (R,+) 阿贝尔群
    2. 乘法封闭
    3. 分配律
    """
    # ========== 1. 加法是阿贝尔群 ==========
    # 封闭
    for a in elements:
        for b in elements:
            if add(a, b) not in elements:
                return False, "加法不封闭"

    # 结合律
    for a in elements:
        for b in elements:
            for c in elements:
                if add(add(a,b),c) != add(a,add(b,c)):
                    return False, "加法不结合"

    # 零元
    zero = None
    for e in elements:
        if all(add(a,e)==a for a in elements):
            zero = e
            break
    if zero is None:
        return False, "无零元"

    # 逆元
    for a in elements:
        has_inv = any(add(a,b)==zero for b in elements)
        if not has_inv:
            return False, f"{a}无加法逆元"

    # 交换
    for a in elements:
        for b in elements:
            if add(a,b) != add(b,a):
                return False, "加法不交换"

    # ========== 2. 乘法封闭 ==========
    for a in elements:
        for b in elements:
            if mul(a,b) not in elements:
                return False, "乘法不封闭"

    # ========== 3. 分配律 ==========
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(a, add(b,c)) != add(mul(a,b), mul(a,c)):
                    return False, "左分配律失败"
                if mul(add(b,c), a) != add(mul(b,a), mul(c,a)):
                    return False, "右分配律失败"

    return True, "满足环公理"

# ========== 学生实验：验证 Z4 是环 ==========
elements = [0,1,2,3]
add = lambda a,b: (a+b)%4
mul = lambda a,b: (a*b)%4

ok, msg = is_ring(elements, add, mul)
print("Z4 是环吗？", ok, "｜", msg)