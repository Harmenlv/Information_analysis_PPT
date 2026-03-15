# 实验 4：主理想 ⟨n⟩（对应：主理想、商环 = 模运算）
def principal_ideal(n, limit=20):
    """主理想 ⟨n⟩ = {kn | k∈Z}"""
    return [i*n for i in range(-limit, limit+1)]

n = 6
I = principal_ideal(n)
print(f"主理想 ⟨{n}⟩ =", I[:10], "...")
print("商环 Z/⟨6⟩ 就是 Z6 👇")
print("等价类：0+6Z,1+6Z,2+6Z,3+6Z,4+6Z,5+6Z")