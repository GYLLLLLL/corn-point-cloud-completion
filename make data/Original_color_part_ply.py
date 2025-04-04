import open3d as o3d
import numpy as np

# 读取玉米点云
input_ply = r"D:\point cloud 6D pose\down_data\pcn_corn\train\complete\06666666\0000004.pcd"
out_path=r"D:\point cloud 6D pose\down_data\pcn_corn\train\patrial\06666666\0000004\09.pcd"



corn_pcd = o3d.io.read_point_cloud(input_ply)

# 确保点云包含颜色信息
if not corn_pcd.has_colors():
    print("警告：点云没有颜色信息，生成的点云将仅包含几何数据！")

# 计算玉米的最小包围盒 (OBB)
obb = corn_pcd.get_oriented_bounding_box()
obb_center = obb.get_center()
obb_extent = obb.extent  # 获取 OBB 的尺寸（长宽高）
obb_rotation = obb.R  # OBB 旋转矩阵
obb_axes = np.eye(3) @ obb_rotation.T  # 计算 OBB 旋转后的坐标轴

# **确定最大平面 (最大尺寸对应的轴)**
max_dim_index = np.argmax(obb_extent)  # 找到最大尺寸的轴索引
normal_vector = obb_axes[:, max_dim_index]  # 获取该轴的法向量

# **在最大平面上生成遮挡区域**
# 随机选择遮挡区域的中心（沿最大平面分布）
leaf_center = obb_center + np.random.uniform(-0.3, 0.3, size=3) * obb_extent
leaf_center[max_dim_index] = obb_center[max_dim_index]  # 确保叶片遮挡在最大平面上

# 设定遮挡区域的大小（矩形）
leaf_size = np.array([obb_extent[0] * 0.8, obb_extent[1] * 0.8, obb_extent[2]])  # 遮挡区域覆盖最大法向量方向

# 计算遮挡区域的边界
leaf_min_bound = leaf_center - leaf_size / 2
leaf_max_bound = leaf_center + leaf_size / 2

# **移除被遮挡区域的所有点**
points = np.asarray(corn_pcd.points)
colors = np.asarray(corn_pcd.colors) if corn_pcd.has_colors() else None  # 读取颜色

# 找到在遮挡区域内的点（包括整个法向量方向）
mask = np.all((points >= leaf_min_bound) & (points <= leaf_max_bound), axis=1)

# **删除被遮挡区域的点，并保留原始颜色**
filtered_points = points[~mask]
filtered_colors = colors[~mask] if colors is not None else None

filtered_pcd = o3d.geometry.PointCloud()
filtered_pcd.points = o3d.utility.Vector3dVector(filtered_points)
if filtered_colors is not None:
    filtered_pcd.colors = o3d.utility.Vector3dVector(filtered_colors)  # 重新赋值颜色

# **创建遮挡区域的点云 (可视化)**
leaf_pcd = o3d.geometry.PointCloud()
num_leaf_points = 4000  # 生成的遮挡区域点数
x_leaf = np.random.uniform(leaf_min_bound[0], leaf_max_bound[0], num_leaf_points)
y_leaf = np.random.uniform(leaf_min_bound[1], leaf_max_bound[1], num_leaf_points)
z_leaf = np.random.uniform(leaf_min_bound[2], leaf_max_bound[2], num_leaf_points)
leaf_pcd.points = o3d.utility.Vector3dVector(np.vstack((x_leaf, y_leaf, z_leaf)).T)

# **可视化遮挡区域**
leaf_pcd.paint_uniform_color([0, 1, 0])  # 绿色：叶片（遮挡区域）

# **可视化最终结果**
o3d.visualization.draw_geometries([filtered_pcd])
o3d.io.write_point_cloud(out_path, filtered_pcd)