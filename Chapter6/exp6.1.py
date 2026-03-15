# 整数环理想的生成与验证
def generate_ideal_Z(m):
    """
    生成整数环Z中由m生成的主理想mZ
    :param m: 生成元（非负整数）
    :return: 理想的特征描述与验证函数
    """
    # 理想定义：所有m的整数倍
    def is_in_ideal(a):
        return a % m == 0 if m != 0 else a == 0
    
    ideal_desc = f"理想 {m}Z = {{ {m}*k | k ∈ Z }}"
    return ideal_desc, is_in_ideal

# 实验验证
if __name__ == "__main__":
    # 测试用例1：平凡理想0Z
    desc0, check0 = generate_ideal_Z(0)
    print(desc0)
    print("0是否属于理想：", check0(0))  # True
    print("5是否属于理想：", check0(5))  # False
    
    # 测试用例2：主理想2Z
    desc2, check2 = generate_ideal_Z(2)
    print("\n" + desc2)
    print("4是否属于理想：", check2(4))  # True
    print("5是否属于理想：", check2(5))  # False
    
    # 验证理想的核心性质：减法封闭+吸收性
    m = 3
    _, check = generate_ideal_Z(m)
    a, b = 6, 9
    # 减法封闭：a-b ∈ I
    print(f"\n验证{m}Z的减法封闭性：{a}-{b}={a-b}，是否属于理想：", check(a-b))  # True
    # 吸收性：任意整数r * 理想元素a ∈ I
    r = 7
    print(f"验证{m}Z的吸收性：{r}*{a}={r*a}，是否属于理想：", check(r*a))  # True