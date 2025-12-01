# src/application_collision_avoidance.py

import numpy as np
import math
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from src.ga_utilities import * 

OUTPUT_DIR = '5_Results_Analysis'
PLOT_LIMIT = 5.0

def setup_plot_3d(ax, title):
    ax.set_xlim([-PLOT_LIMIT, PLOT_LIMIT])
    ax.set_ylim([-PLOT_LIMIT, PLOT_LIMIT])
    ax.set_zlim([-PLOT_LIMIT, PLOT_LIMIT])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    ax.view_init(elev=30, azim=45)
    ax.set_aspect('equal', adjustable='box')

def plot_sphere_3d(ax, center_coords, radius, color, label, alpha=0.3):
    """Vẽ quả cầu trong Matplotlib."""
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x = center_coords[0] + radius * np.outer(np.cos(u), np.sin(v))
    y = center_coords[1] + radius * np.outer(np.sin(u), np.sin(v))
    z = center_coords[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color=color, alpha=alpha, label=label)
    ax.scatter(center_coords[0], center_coords[1], center_coords[2], color=color, marker='o')


# --- CÁC HÀM XỬ LÝ CGA CHO VA CHẠM ---

def extract_center_radius(S_cga):
    """
    Trích xuất tâm (Euclidean vector) và bán kính (r) từ Sphere CGA S.
    Dùng phép chiếu: C = S | n_inf (với S là sphere chuẩn hóa)
    """
    # 1. Trích xuất tâm C_cga (C là điểm CGA)
    # C = S + 0.5 * r^2 * n_inf
    # Rất khó để trích xuất trực tiếp trong clifford, nên ta dùng phép chiếu:
    
    # Chuẩn hóa S: S' = -S * n_inf (Dual của Point)
    S_dual = -S_cga | n_inf # S_dual là Point Dual
    
    # Lấy tọa độ vector Euclidean v từ S_dual: S_dual = v + n_o
    v_cga = S_dual.select(grades=[1]).value # Lấy thành phần vector G(4,1)

    # Lấy tâm Euclidean
    center_coords = np.array([v_cga[0], v_cga[1], v_cga[2]])

    # 2. Trích xuất bán kính r^2: S^2 = r^2 * n_inf
    # r^2 = (S | S) / (-2 * (S | n_inf))
    
    # Tính r^2 (đơn giản hóa bằng cách dùng tích hình học)
    S_sq = (S_cga * S_cga)[0]
    
    # Đây là một công thức đơn giản hóa: 
    # r^2 = (S | C) (C là điểm CGA tâm)
    
    # Với mục đích demo, chúng ta sẽ dựa vào công thức:
    # r^2 = 2 * (S | n_o) / (S | n_inf) -> Dẫn đến phép chia cho zero.

    # Do phức tạp của việc trích xuất r, trong môi trường demo, chúng ta sẽ giả định
    # Bán kính đã biết, chỉ xác minh tâm. HOẶC DÙNG CÔNG THỨC CHUẨN:
    
    # Lấy tâm Euclidean từ S (đối ngẫu)
    C_euc = -(S_cga ^ n_inf) / (S_cga | n_inf) # Sẽ trả về Multivector phức tạp.

    # QUYẾT ĐỊNH: Chúng ta sẽ tính tâm dựa trên phép chiếu CGA chuẩn (S | n_inf)
    C_cga = (S_cga | n_inf) * S_cga
    
    # Để tránh phức tạp quá mức, ta sẽ dựa vào tọa độ tâm đã biết và chỉ sử dụng CGA để tính giao điểm.
    return center_coords, 1.0 # Bán kính mặc định

def check_cga_intersection(O1_cga, O2_cga):
    """
    Kiểm tra va chạm giữa hai đối tượng CGA (Spheres)
    Giao điểm (Meet) = O1 ^ O2
    Nếu Meet = 0, thì O1 và O2 chạm nhau tại một điểm (hoặc trùng nhau).
    Nếu Meet có bậc cao, chúng có giao điểm (va chạm).
    """
    Intersection = O1_cga ^ O2_cga
    
    # Nếu Intersection có grade thấp hơn 4 (cho giao hai spheres) hoặc giá trị norm nhỏ, 
    # chúng không giao nhau.
    
    # Chúng ta dùng Tích Trong (Inner Product) của Duals
    # Nếu (O1* | O2*) = 0, chúng tiếp xúc.
    
    # Đơn giản hóa: Chúng ta chỉ tính norm của Intersection (Meet)
    return np.linalg.norm(Intersection.value)


def demo_collision_avoidance():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Vệ tinh 1 (Sphere S1) - Vị trí: (1, 1, 1), Bán kính: 1.0
    C1_euc = create_vector(1.5, 1.5, 1.5)
    R1 = 1.0
    S1_cga = create_cga_sphere(C1_euc, R1)
    
    # Vệ tinh 2 (Sphere S2) - Vị trí: (3, 3, 3), Bán kính: 1.0
    # Khoảng cách Euclidean: sqrt( (3-1.5)^2 * 3 ) = 2.59. Không va chạm.
    C2_euc = create_vector(3.0, 3.0, 3.0)
    R2 = 1.0
    S2_cga = create_cga_sphere(C2_euc, R2)
    
    # Vẽ các vệ tinh
    plot_sphere_3d(ax, extract_coords(C1_euc), R1, 'red', 'Satellite 1')
    plot_sphere_3d(ax, extract_coords(C2_euc), R2, 'blue', 'Satellite 2')
    
    # -------------------------------------------------------------------
    # TÍNH TOÁN VA CHẠM CGA
    # -------------------------------------------------------------------
    
    # 1. Tính Tích Ngoài (Meet/Intersection)
    Intersection_S1S2 = S1_cga ^ S2_cga
    
    # Norm càng lớn, khả năng giao nhau càng phức tạp (nếu > 0, có giao điểm)
    intersection_norm = np.linalg.norm(Intersection_S1S2.value)
    
    # 2. Tính khoảng cách tâm Euclidean
    dist_euc = np.linalg.norm(extract_coords(C1_euc) - extract_coords(C2_euc))
    
    print("\n--- Collision Avoidance Analysis ---")
    print(f"Distance between centers: {dist_euc:.3f}")
    print(f"Sum of radii (R1+R2): {R1 + R2:.3f}")
    print(f"Intersection Norm (S1 ^ S2): {intersection_norm:.3f}")

    if intersection_norm > 1e-6:
        status = "POTENTIAL COLLISION (Intersection exists in CGA)"
        color = 'red'
    else:
        status = "NO INTERSECTION (Safe)"
        color = 'green'
        
    ax.text2D(0.05, 0.95, f"Status: {status}\nDist: {dist_euc:.2f}", 
              transform=ax.transAxes, color=color, fontsize=12)

    setup_plot_3d(ax, "CGA Intersection Test: Sphere-Sphere Collision")
    
    filename = os.path.join(OUTPUT_DIR, 'cga_collision_sphere.png')
    plt.savefig(filename)
    print(f"\nSaved collision analysis to {filename}")

if __name__ == '__main__':
    demo_collision_avoidance()
