# 实验 3：理想验证（对应：理想、吸收性、子环≠理想）
def is_ideal(R, I, add, mul):
    """
    验证 I 是 R 的理想
    1. I 是加法子群
    2. 吸收性：∀r∈R, ∀i∈I → r*i ∈ I
    """
    # 子群：封闭 + 逆元
    for i1 in I:
        for i2 in I:
            if add(i1,i2) not in I:
                return False, "I 加法不封闭"

    for i in I:
        has_inv = any(add(i, inv)==0 for inv in I)
        if not has_inv:
            return False, "I 无逆元"

    # 吸收性（关键！子环 vs 理想）
    for r in R:
        for i in I:
            if mul(r,i) not in I:
                return False, "不满足吸收性，不是理想"
    return True, "是理想"

# ========== 学生实验：2Z 是 Z 的理想 ==========
R = range(-10, 11)
I = [i for i in R if i%2==0]
add = lambda a,b:a+b
mul = lambda a,b:a*b

print("2Z 是 Z 的理想？", is_ideal(R, I, add, mul))