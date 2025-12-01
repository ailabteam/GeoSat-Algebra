# src/ga_utilities.py (HỢP NHẤT G3 và CGA)

import numpy as np
import math
import clifford as cf
from clifford.g3 import *

# ----------------------------------------------------
# 1. SETUP: EUCLIDEAN GEOMETRIC ALGEBRA G(3)
# ----------------------------------------------------

def create_vector(x, y, z):
    """Tạo một vector 3D trong không gian G(3)."""
    # Sử dụng basis e1, e2, e3 của G3
    return x*e1 + y*e2 + z*e3

def create_bivector_from_plane(v1, v2):
    return v1 ^ v2

def create_rotor(axis_bivector, angle_rad):
    B = axis_bivector.normal()
    half_angle = angle_rad / 2
    R = np.cos(half_angle) - B * np.sin(half_angle)
    return R

def extract_coords(multivector):
    """Trích xuất tọa độ 3D (x, y, z) từ một Multivector (grade 1)."""
    if not isinstance(multivector, cf.MultiVector):
        return np.zeros(3)

    coords = [
        multivector[e1],
        multivector[e2],
        multivector[e3]
    ]
    return np.array(coords)

def apply_rotor(R, vector):
    """Áp dụng Rotor R lên Vector v để quay nó."""
    R_reverse = ~R
    rotated_vector_full = R * vector * R_reverse
    coords = extract_coords(rotated_vector_full)
    return create_vector(*coords)

# ----------------------------------------------------
# 2. SETUP: CONFORMAL GEOMETRIC ALGEBRA G(4,1)
# ----------------------------------------------------
# (4, 1) signature: 4 basis^2 = +1, 1 basis^2 = -1
layout_cga, blades_cga = cf.Cl(4, 1)

e1_cga, e2_cga, e3_cga, ep, em = (
    blades_cga['e1'], blades_cga['e2'], blades_cga['e3'], blades_cga['e4'], blades_cga['e5']
)

# Null Basis
n_inf = ep + em          # Vector vô cực (e_infinity)
n_o = 0.5 * (em - ep)    # Vector gốc (e_origin)

# ----------------------------------------------------
# 3. HÀM TẠO ĐỐI TƯỢNG CGA VÀ PHÉP BIẾN ĐỔI
# ----------------------------------------------------

def create_vector_cga(x, y, z):
    """Tạo một vector Euclidean trong không gian CGA."""
    return x*e1_cga + y*e2_cga + z*e3_cga

def point_to_cga(P_euclidean):
    """
    Chuyển đổi một vector Euclidean 3D sang Point trong CGA 5D.
    P = v + 0.5 * ||v||^2 * n_inf + n_o
    """
    # P_euclidean là G3 Multivector. Lấy tọa độ từ G3.
    x, y, z = extract_coords(P_euclidean)

    # Tạo vector v (G3)
    v = P_euclidean

    # Tính ||v||^2. Lưu ý: P_euclidean là G3, nên phép nhân vẫn là G3
    v_sq = (v * v).select(grades=[0]).value[0] if hasattr(v * v, 'select') else (v * v)[0]

    # Tạo vector v_cga
    v_cga = create_vector_cga(x, y, z)

    # Multivector đại diện cho Điểm (Point)
    P_cga = v_cga + 0.5 * v_sq * n_inf + n_o

    return P_cga

def create_cga_line(P1_cga, P2_cga):
    """
    Tạo một Đường thẳng (Line) đi qua hai điểm CGA.
    Công thức: L = P1 ^ P2 ^ n_inf
    """
    return P1_cga ^ P2_cga ^ n_inf

def create_cga_sphere(center_euc, radius):
    """
    Tạo một Quả cầu (Sphere) từ vector tâm (G3 Multivector) và bán kính.
    Công thức: S = C - 0.5 * r^2 * n_inf (C là điểm CGA tâm)
    """
    C_cga = point_to_cga(center_euc)
    # Tích trong (Inner Product) của quả cầu với chính nó là r^2
    S_cga = C_cga - 0.5 * radius**2 * n_inf
    return S_cga

def get_closest_distance(O1, O2):
    """
    Tính khoảng cách ngắn nhất giữa hai đối tượng CGA O1 và O2
    (ví dụ: Sphere-Sphere, Sphere-Line).
    Sử dụng Tích đối ngẫu (Dual) và Tích Trong (Inner Product).
    Khoảng cách D = || (O1 ^ O2) / I5 ||
    Tuy nhiên, cách đơn giản nhất là dựa vào công thức:
    D = sqrt(|(O1 | O2) / (O1 | O1 | O2 | O2)|) cho các đối tượng chuẩn hóa.
    
    Cách dễ nhất: Trích xuất tọa độ từ giao điểm hoặc dùng công thức đơn giản cho đối tượng dual.
    
    Chúng ta sẽ dùng công thức chuẩn hóa CGA cho khoảng cách giữa hai mặt phẳng:
    Nếu O1* và O2* là đối ngẫu (Dual), D = ||(O1* | O2*) - 1||
    
    Cho hai quả cầu (Sphere) S1, S2: Khoảng cách = ||v1 - v2|| - (r1 + r2)
    Vì CGA không tính khoảng cách Euclidean trực tiếp mà chỉ tính giao điểm/tiếp xúc, 
    chúng ta cần chiếu đối tượng tâm về Euclidean trước.
    
    Nhưng để "show up" CGA, ta sẽ tính giao điểm (Meet) và khoảng cách tâm (Euclidean).
    """
    # Quay lại mục tiêu ban đầu: Trích xuất tọa độ tâm từ quả cầu.
    # 1. Trích xuất tâm (C) và bán kính (r) từ quả cầu S
    
    # S = C - 0.5 * r^2 * n_inf
    # Tâm C = S - 0.5 * (S | S) * n_inf (C là điểm CGA)
    
    # Do phức tạp, chúng ta sẽ chỉ tính khoảng cách Euclidean giữa hai tâm
    # và sau đó dùng CGA để kiểm tra xem có giao nhau không (Meet).
    
    # Hàm này sẽ chỉ trích xuất tâm Euclidean từ Sphere CGA
    
    # S* = S / I5  (Dual)
    # S* | n_inf = -C/I + n_inf... (quá phức tạp cho demo)
    
    # HÀM NÀY SẼ ĐƯỢC ĐƠN GIẢN HÓA TRONG SCRIPT DEMO
    pass



# ... (Hàm point_to_cga giữ nguyên)

def create_translator(translation_vector_euclidean):
    """
    Tạo một Translator (Tịnh tiến) từ vector Euclidean t.
    Công thức: T = 1 - 0.5 * n_inf * t_cga
    Chúng ta sẽ dùng tích ngoài (wedge) cho sự rõ ràng: T = 1 - 0.5 * t_cga ^ n_inf
    """
    # Chuyển vector Euclidean (G3) sang vector t_cga (G4,1)
    x, y, z = extract_coords(translation_vector_euclidean)
    t_cga = create_vector_cga(x, y, z)

    # SỬA TẠI ĐÂY: Dùng tích ngoài thay vì tích hình học cho phần bivector
    # T = 1 - 0.5 * (t_cga * n_inf)
    T = 1 - 0.5 * (t_cga ^ n_inf)  # <-- Translator dựa trên Wedge Product
    return T
# ----------------------------------------------------
# 4. SELF TEST (Cập nhật)
# ----------------------------------------------------
if __name__ == '__main__':
    # ... (G3 Test giữ nguyên)
    print("\n--- CGA Utilities Test (G(4,1)) ---")

    # 1. Tạo điểm gốc (Origin)
    P_origin_euc = create_vector(0, 0, 0)
    P_origin_cga = point_to_cga(P_origin_euc)
    # Kết quả kỳ vọng: (1^e5) - (0.5^e4) * n_o
    print(f"P_o (CGA): {P_origin_cga}")

    # 2. Tạo điểm P1 (1, 0, 0)
    P1_euc = create_vector(1, 0, 0)
    P1_cga = point_to_cga(P1_euc)
    # Kết quả kỳ vọng: (1^e1) + 0.5 * 1^2 * n_inf + n_o
    print(f"P1 (CGA): {P1_cga}")

    # 3. Test Translator tịnh tiến
    t_euc = create_vector(2, 0, 0)
    T = create_translator(t_euc)
    print(f"Translator T (x=2): {T}")

    # 4. Áp dụng Translator lên P_origin: P_o' = T * P_o * ~T
    P_prime_cga = T * P_origin_cga * (~T)
    print(f"P_o' (Tịnh tiến P_o): {P_prime_cga}")

    print("---------------------------------")
