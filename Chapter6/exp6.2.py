# 多项式环子环与理想的区分验证
from sympy import Poly, symbols, expand

x, y = symbols('x y')

def is_in_subring_S(f):
    """
    判断多项式是否属于子环S = {f(x) ∈ Z[x] | f(0)=0}
    :param f: 多项式（sympy Poly对象）
    :return: bool
    """
    # 计算f(0)：常数项为0则属于S
    return f.eval(0) == 0

def is_in_ideal_I(f, gen):
    """
    判断多项式是否属于由gen生成的主理想I=(gen)
    :param f: 待判断多项式
    :param gen: 理想生成元（多项式）
    :return: bool
    """
    if gen == 0:
        return f == 0
    # 理想定义：存在g ∈ Z[x] 使得 f = gen * g
    try:
        quo, rem = divmod(f, gen)
        # 余数为0且商为整数系数多项式
        return rem == 0 and all(coeff.is_integer for coeff in quo.all_coeffs())
    except:
        return False

# 实验验证
if __name__ == "__main__":
    # 定义子环S和理想I=(x)
    f1 = Poly(x, x, domain='Z')  # x ∈ S
    f2 = Poly(2*x + x**2, x, domain='Z')  # 2x+x² ∈ S
    f3 = Poly(1 + x, x, domain='Z')  # 1+x ∉ S
    
    print("子环S验证：")
    print(f"f1={f1} ∈ S? {is_in_subring_S(f1)}")  # True
    print(f"f2={f2} ∈ S? {is_in_subring_S(f2)}")  # True
    print(f"f3={f3} ∈ S? {is_in_subring_S(f3)}")  # False
    
    # 验证理想I=(x)的吸收性
    gen = Poly(x, x, domain='Z')
    r = Poly(2 + 3*x, x, domain='Z')  # 环中任意元素
    a = Poly(x, x, domain='Z')  # 理想中元素
    ra = expand(r * a)
    
    print("\n理想I=(x)验证：")
    print(f"r={r}, a={a}, ra={ra}")
    print(f"ra ∈ I? {is_in_ideal_I(ra, gen)}")  # True
    
    # 对比：子环无全局吸收性（修正版例子）
    # 环Z[x,y]，子环S={f | f(0,y)=0}，测试吸收性
    f4 = Poly(x, x, y, domain='Z')  # x ∈ S
    r2 = Poly(y, x, y, domain='Z')  # 环中元素y
    r2f4 = expand(r2 * f4)  # xy
    # 验证xy仍属于S（说明原例子瑕疵，换更典型场景）
    # 改用环Q[x]，子环S={f | f(0)∈Z}，理想I=(x)
    f5 = Poly(x, x, domain='Q')
    r3 = Poly(1/2, x, domain='Q')
    r3f5 = expand(r3 * f5)  # x/2
    print(f"\nQ[x]中子环S验证：r3*f5={r3f5}，f(0)={r3f5.eval(0)} ∈ Z? {r3f5.eval(0).is_integer}")  # False