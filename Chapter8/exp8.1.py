# 实验1：椭圆曲线判别式计算与非奇异性判定
def is_non_singular(a, b, p):
    """
    判断有限域F_p上的椭圆曲线y²=x³+ax+b是否非奇异
    核心判定条件：4a³ + 27b² ≢ 0 (mod p)
    """
    # 分步计算模p值，避免大数运算
    term1 = (4 * pow(a, 3, p)) % p
    term2 = (27 * pow(b, 2, p)) % p
    total = (term1 + term2) % p
    
    # 输出判定结果
    if total != 0:
        print(f"曲线非奇异（4a³+27b² mod p = {total} ≠ 0），可用于密码学")
        print(f"判别式Δ = {-16 * total % p} (mod {p}) ≠ 0")
        return True
    else:
        print(f"曲线奇异（4a³+27b² mod p = 0），禁止用于密码学")
        print(f"判别式Δ = 0")
        return False

# 测试用例1：F_11上的曲线y²=x³+2x+3（奇异曲线）
print("=== 测试用例1：F_11上的y²=x³+2x+3 ===")
is_non_singular(a=2, b=3, p=11)

# 测试用例2：F_11上的曲线y²=x³+2x+4（非奇异曲线）
print("\n=== 测试用例2：F_11上的y²=x³+2x+4 ===")
is_non_singular(a=2, b=4, p=11)

# 测试用例3：F_7上的曲线y²=x³+2x+3（非奇异曲线）
print("\n=== 测试用例3：F_7上的y²=x³+2x+3 ===")
is_non_singular(a=2, b=3, p=7)