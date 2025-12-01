# src/demo_ga_3d_rotation.py (PHIÊN BẢN SỬA LỖI HOÀN CHỈNH)

import numpy as np
import matplotlib.pyplot as plt
import math
import os
from src.ga_utilities import * # Import các hàm trợ giúp GA

# --- CẤU HÌNH TRỰC QUAN HÓA ---
OUTPUT_DIR = '5_Results_Analysis'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Định nghĩa 'limit' ở phạm vi toàn cục hoặc truyền vào hàm
PLOT_LIMIT = 1.2 # <<<< SỬA TẠI ĐÂY

def plot_vector(ax, vector_coords, color, label):
    """Hàm trợ giúp để vẽ một vector trong không gian 3D."""
    ax.quiver(0, 0, 0, 
              vector_coords[0], vector_coords[1], vector_coords[2], 
              color=color, length=1, normalize=True, arrow_length_ratio=0.1, label=label)

def setup_3d_plot(ax, title):
    """Thiết lập giới hạn và nhãn cho plot 3D."""
    ax.set_xlim([-PLOT_LIMIT, PLOT_LIMIT]) # <<<< SỬA TẠI ĐÂY
    ax.set_ylim([-PLOT_LIMIT, PLOT_LIMIT]) # <<<< SỬA TẠY ĐÂY
    ax.set_zlim([-PLOT_LIMIT, PLOT_LIMIT]) # <<<< SỬA TẠI ĐÂY
    ax.set_xlabel('X (e1)')
    ax.set_ylabel('Y (e2)')
    ax.set_zlabel('Z (e3)')
    ax.set_title(title)
    ax.view_init(elev=20, azim=45)
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')

def compare_rotation_ga_vs_matrix(vector_in_np, angle_deg=60):
    """
    Thực hiện và so sánh phép quay bằng Rotor (GA) và Ma trận quay (truyền thống).
    """
    angle_rad = math.radians(angle_deg)
    
    # ------------------------------------------------------
    # 1. PHƯƠNG PHÁP GA (ROTOR)
    # Trục quay là trục X (mặt phẳng YZ)
    # ------------------------------------------------------
    
    v_in_ga = create_vector(*vector_in_np)
    
    # Trục quay X (Bivector e2^e3)
    axis_bivector = create_bivector_from_plane(e2, e3)
    R = create_rotor(axis_bivector, angle_rad)
    
    v_out_ga_mv = apply_rotor(R, v_in_ga)
    v_out_ga_np = extract_coords(v_out_ga_mv)

    print(f"\n--- GA Rotor Results ---")
    print(f"Input Vector (GA): {v_in_ga}")
    print(f"Output Vector (GA): {v_out_ga_mv}")
    print(f"Coordinates (NP): {v_out_ga_np}")

    # ------------------------------------------------------
    # 2. PHƯƠNG PHÁP MA TRẬN TRUYỀN THỐNG (Quay quanh trục X)
    # ------------------------------------------------------
    
    cos_a = np.cos(angle_rad)
    sin_a = np.sin(angle_rad)
    
    # Ma trận quay quanh trục X
    R_matrix = np.array([
        [1, 0, 0],
        [0, cos_a, -sin_a],
        [0, sin_a, cos_a]
    ])
    
    v_out_matrix = R_matrix @ vector_in_np
    
    print(f"\n--- Matrix Rotation Results ---")
    print(f"Output Vector (Matrix): {v_out_matrix}")
    
    # ------------------------------------------------------
    # 3. TRỰC QUAN HÓA
    # ------------------------------------------------------
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Vẽ vector gốc
    plot_vector(ax, vector_in_np, 'blue', 'Input Vector (v)')
    
    # Vẽ vector GA (kết quả Rotor)
    plot_vector(ax, v_out_ga_np, 'red', 'GA Rotated (v\')')
    
    # Vẽ vector Ma trận (kết quả Ma trận)
    plot_vector(ax, v_out_matrix, 'green', 'Matrix Rotated (v\')')

    # Trục quay (ví dụ, trục X)
    ax.plot([0, PLOT_LIMIT], [0, 0], [0, 0], 'k--', alpha=0.5, label='Rotation Axis (X)') # <<<< SỬA TẠI ĐÂY
    
    setup_3d_plot(ax, f'3D Rotation Comparison ({angle_deg} deg around X)')
    
    # Kiểm tra sự khác biệt (đảm bảo hai phương pháp cho cùng kết quả)
    diff = np.linalg.norm(v_out_ga_np - v_out_matrix)
    print(f"\nDifference (Norm): {diff:.6f}")

    # Xuất file hình ảnh
    plt.legend()
    filename = os.path.join(OUTPUT_DIR, 'rotation_comparison_g3.png')
    plt.savefig(filename)
    print(f"\nSaved visualization to {filename}")
    # plt.show() # Chỉ bật nếu chạy local

if __name__ == '__main__':
    # Vector đầu vào (ví dụ: tư thế ăng-ten vệ tinh)
    initial_vector = np.array([0.5, 0.8, 0.2]) 
    
    compare_rotation_ga_vs_matrix(initial_vector, angle_deg=120)
