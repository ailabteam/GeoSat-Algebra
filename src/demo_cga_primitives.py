# src/demo_cga_primitives.py (PHIÊN BẢN SỬA LỖI NAMEERROR)

import numpy as np
import math
import os
import matplotlib.pyplot as plt
from src.ga_utilities import *
# Lưu ý: Các hàm CGA và G3 đã được import từ ga_utilities

# --- CẤU HÌNH TRỰC QUAN HÓA ---
OUTPUT_DIR = '5_Results_Analysis'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
PLOT_LIMIT = 3.0

# (Hàm setup_3d_plot_cga giữ nguyên)
def setup_3d_plot_cga(ax, title):
    """Thiết lập giới hạn và nhãn cho plot 3D."""
    ax.set_xlim([-PLOT_LIMIT, PLOT_LIMIT])
    ax.set_ylim([-PLOT_LIMIT, PLOT_LIMIT])
    ax.set_zlim([-PLOT_LIMIT, PLOT_LIMIT])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    ax.view_init(elev=30, azim=60)
    ax.set_aspect('equal', adjustable='box')


# src/demo_cga_primitives.py (SỬA LỖI AS_SCALAR)

# ... (các import và hàm setup giữ nguyên)

def plot_point_cga(ax, P_cga, color, label):
    """
    Trích xuất tọa độ 3D Euclidean từ Point CGA và vẽ điểm đó.
    Phương pháp: Chuẩn hóa P_cga, sau đó chiếu P_norm - n_o.
    """
    try:
        # 1. Chuẩn hóa điểm CGA: P_norm = P / (-P | n_inf)
        inner_prod_mv = -(P_cga | n_inf)
        
        # Trích xuất scalar bằng index [0]
        norm_factor = inner_prod_mv[0]
        
        if np.isclose(norm_factor, 0): # Dùng np.isclose cho số float
             print("Warning: Point is at infinity.")
             return np.zeros(3)

        P_norm = P_cga / norm_factor
        
        # 2. Chiếu về vector Euclidean: v = P_norm - n_o
        v_euclidean_cga = P_norm - n_o
        
        # 3. Lấy hệ số v
        # Lấy hệ số theo basis CGA Euclidean
        x = v_euclidean_cga[e1_cga]
        y = v_euclidean_cga[e2_cga]
        z = v_euclidean_cga[e3_cga]

        ax.scatter(x, y, z, color=color, s=50, label=label)
        
        return np.array([x, y, z])
    
    except Exception as e:
        print(f"Error plotting CGA point: {e}")
        return np.zeros(3)

# ... (Hàm demo_translation và main giữ nguyên)


def demo_translation():
    """Minh họa phép tịnh tiến của vệ tinh bằng Translator CGA."""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # 1. Điểm bắt đầu (vị trí vệ tinh) - Dùng hàm G3 create_vector
    P_start_euc = create_vector(1.0, 1.0, 0.5)
    P_start_cga = point_to_cga(P_start_euc)

    coords_start = plot_point_cga(ax, P_start_cga, 'blue', 'Start Point $P_{start}$')

    # 2. Vector Tịnh tiến (Move 1.5 units in X and 1.0 unit in Y)
    t_euc = create_vector(1.5, -1.0, 0.0) # Dùng hàm G3 create_vector
    T = create_translator(t_euc)

    # 3. Tịnh tiến điểm: P' = T * P * ~T
    P_end_cga = T * P_start_cga * (~T)
    coords_end = plot_point_cga(ax, P_end_cga, 'red', 'End Point $P_{end}$')

    # Vẽ vector tịnh tiến
    t_coords = extract_coords(t_euc)
    ax.quiver(coords_start[0], coords_start[1], coords_start[2],
              t_coords[0], t_coords[1], t_coords[2],
              color='gray', linestyle='--', label='Translation Vector (t)')

    setup_3d_plot_cga(ax, "CGA Translator: Satellite Position Update")

    # Kiểm tra tính chính xác của phép tịnh tiến
    expected_end = coords_start + t_coords
    actual_end = coords_end
    print(f"\nExpected End Coords: {expected_end}")
    print(f"Actual End Coords (CGA): {actual_end}")
    print(f"Error Norm: {np.linalg.norm(expected_end - actual_end):.6f}")

    # Xuất file hình ảnh
    filename = os.path.join(OUTPUT_DIR, 'cga_translation_demo.png')
    plt.legend()
    plt.savefig(filename)
    print(f"\nSaved CGA translation demo to {filename}")

if __name__ == '__main__':
    demo_translation()
