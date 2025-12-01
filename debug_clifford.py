# debug_clifford.py (PHIÊN BẢN SỬA LỖI IMPORT NUMPY)

import clifford as cf
from clifford.g3 import *
import math
import numpy as np  # <<<< ĐÃ THÊM

# 1. Tạo một vector và một Rotor
v_e1 = 1*e1
b_xy = e1 ^ e2
R_90 = np.cos(math.pi / 4) - b_xy.normal() * np.sin(math.pi / 4)

# 2. Thực hiện phép quay
rotated_mv = R_90 * v_e1 * (~R_90)

print("--- CLIFFORD DEBUG OUTPUT ---")
print(f"Type of rotated_mv: {type(rotated_mv)}")
print(f"Rotated Multivector (Full): {rotated_mv}")
print("-" * 30)

# 3. Kiểm tra các thuộc tính để trích xuất grade 1

print("Attempting to extract components:")

# A. Grades (Sử dụng để lấy dictionary/mapping)
print(f"Check .grades(): {hasattr(rotated_mv, 'grades')}")
if hasattr(rotated_mv, 'grades'):
    print(f"rotated_mv.grades(): {rotated_mv.grades()}")

# B. Coefficients (.value)
print(f"Check .value (coefficients array): {hasattr(rotated_mv, 'value')}")
if hasattr(rotated_mv, 'value'):
    print(f"rotated_mv.value[:]: {rotated_mv.value}")

# C. Accessing components by index (grade 1)
try:
    # Cảnh báo: Phương pháp này bị Deprecated, nhưng giúp ta thấy cấu trúc
    grade_1_part = rotated_mv[1] 
    print(f"rotated_mv[1] (Grade 1): {grade_1_part} (Type: {type(grade_1_part)})")
except Exception as e:
    print(f"rotated_mv[1] FAILED: {e}")

# D. Accessing components by basis (e1, e2, e3)
print(f"rotated_mv[e1] coeff: {rotated_mv[e1]}")
print(f"rotated_mv[e2] coeff: {rotated_mv[e2]}")
print(f"rotated_mv[e3] coeff: {rotated_mv[e3]}")

print("-" * 30)
