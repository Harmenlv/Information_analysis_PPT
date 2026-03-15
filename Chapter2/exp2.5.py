# 实验 5：二元多项式环 Z₂[x] + 构造 GF (2⁸)（AES 核心，完全匹配你 PPT）
def poly_add(p1, p2):
    """Z2[x] 加法 = 异或"""
    return [a^b for a,b in zip(p1+[0]*len(p2), p2+[0]*len(p1))]

def poly_mul(p1, p2):
    """Z2[x] 乘法"""
    deg1 = len(p1)-1
    deg2 = len(p2)-1
    res = [0]*(deg1+deg2+1)
    for i in range(len(p1)):
        for j in range(len(p2)):
            res[i+j] ^= p1[i] & p2[j]
    return res

# AES 不可约多项式：x^8+x^4+x^3+x+1 → [1,1,0,1,1,0,0,0,1]
f = [1,1,0,1,1,0,0,0,1]

print("=== 二元多项式环 Z2[x] ===")
p1 = [1,0,1,1]   # x^3 + x + 1
p2 = [1,1]       # x + 1
print("p1 =", p1)
print("p2 =", p2)
print("p1+p2 =", poly_add(p1,p2))
print("p1*p2 =", poly_mul(p1,p2))
print("\nAES 用理想 ⟨x^8+x^4+x^3+x+1⟩ 构造 GF(2^8)")
print("商环 Z2[x]/⟨f⟩ ≅ GF(2^8)（256字节，无零因子）")