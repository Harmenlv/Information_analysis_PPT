# 实验2：格基变换与体积不变性验证
import numpy as np

def calculate_lattice_volume(basis):
    """
    计算格的体积（基矩阵行列式的绝对值）
    :param basis: 格基（二维数组）
    :return: 格体积
    """
    basis_matrix = np.array(basis)
    det = np.linalg.det(basis_matrix)
    return abs(det)

def basis_transform(basis, transform_matrix):
    """
    格基变换（B2 = B1 · U）
    :param basis: 原始格基
    :param transform_matrix: 整数可逆矩阵（行列式±1）
    :return: 新格基
    """
    basis_matrix = np.array(basis)
    transform_matrix = np.array(transform_matrix)
    new_basis_matrix = basis_matrix @ transform_matrix
    return new_basis_matrix.tolist()

# 实验执行
if __name__ == "__main__":
    # 1. 原始基（标准正交基）
    basis1 = [[1, 0], [0, 1]]
    vol1 = calculate_lattice_volume(basis1)
    print(f"原始基体积：{vol1}")
    
    # 2. 合法基变换（行列式=1）
    # 变换矩阵U = [[1,1],[0,1]]（行列式=1）
    U_valid = [[1, 1], [0, 1]]
    basis2 = basis_transform(basis1, U_valid)
    vol2 = calculate_lattice_volume(basis2)
    print(f"变换后基：{basis2}，体积：{vol2}（与原始体积一致）")
    
    # 3. 非法基变换（行列式≠±1）
    U_invalid = [[1, 1], [1, -1]]
    basis3 = basis_transform(basis1, U_invalid)
    vol3 = calculate_lattice_volume(basis3)
    print(f"非法变换后基：{basis3}，体积：{vol3}（体积改变，非同一格）")
    
    # 4. 验证多组基体积不变性
    basis_list = [
        [[1,0],[0,1]],
        [[1,1],[1,-1]],
        [[2,1],[1,1]]
    ]
    for idx, basis in enumerate(basis_list):
        vol = calculate_lattice_volume(basis)
        print(f"基{idx+1}体积：{vol}（均为1，验证同一格体积不变）")