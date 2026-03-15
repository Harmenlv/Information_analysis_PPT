# 主理想整环中理想和的计算
import math
from sympy import gcd, Poly, symbols

x = symbols('x')

def ideal_sum_pid(a, b, ring_type='Z'):
    """
    计算PID中两个主理想(a)+(b)=(d)，d为a,b的gcd
    :param a: 生成元1
    :param b: 生成元2
    :param ring_type: 环类型（'Z'整数环 / 'F[x]'域上多项式环）
    :return: 理想和的生成元d
    """
    if ring_type == 'Z':
        # 整数环：gcd(a,b)
        return math.gcd(a, b)
    elif ring_type == 'F[x]':
        # 域上多项式环（以Q[x]为例）
        return gcd(a, b)
    else:
        raise ValueError("仅支持Z和F[x]环")

# 实验验证
if __name__ == "__main__":
    # 测试1：整数环Z
    a, b = 12, 18
    d = ideal_sum_pid(a, b, 'Z')
    print(f"整数环中：({a})+({b})=({d})")  # (6)
    # 验证：6Z包含12Z+18Z，且6是最小生成元
    print(f"12是否属于{d}Z: {12 % d == 0}")  # True
    print(f"18是否属于{d}Z: {18 % d == 0}")  # True
    
    # 测试2：多项式环Q[x]
    f = Poly(x**2 - 4, x, domain='Q')  # (x-2)(x+2)
    g = Poly(x**2 + 5x + 6, x, domain='Q')  # (x+2)(x+3)
    d_poly = ideal_sum_pid(f, g, 'F[x]')
    print(f"\n多项式环中：({f})+({g})=({d_poly})")  # (x+2)
    # 验证吸收性
    fg_sum = expand(f + g)
    print(f"f+g={fg_sum} 是否属于({d_poly}): {fg_sum % d_poly == 0}")  # True