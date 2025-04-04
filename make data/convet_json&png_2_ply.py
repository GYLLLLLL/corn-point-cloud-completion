import numpy as np
import cv2
import json
import open3d as o3d
import os
root_p=r"D:\point cloud 6D pose\All_data\data3\1719297351.9629416"
json_path = os.path.join(root_p,'left.json')
img_path = os.path.join(root_p,'left.png')
depth_path = os.path.join(root_p,'depth.npy')
out_path=os.path.join(root_p,'output.pcd')
print(out_path)
#out_path=r"D:\point cloud 6D pose\All_data\data2\pcd\output.pcd"

# 读取 JSON 文件
with open(json_path, "r") as f:
    data = json.load(f)

# 读取 RGB 图像
image = cv2.imread(img_path)  # 读取 RGB 图像
#image = cv2.imread(r"D:\point cloud 6D pose\make data\3773\left.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # OpenCV 默认 BGR，转换为 RGB

# 读取深度图
depth = np.load(depth_path)  # 读取深度数据（单位：米）

# 获取图像尺寸
height, width, _ = image.shape

# 创建掩码
mask = np.zeros((height, width), dtype=np.uint8)

# 解析 JSON 获取多边形区域
for shape in data["shapes"]:
    points = np.array(shape["points"], dtype=np.int32)  # 解析多边形点
    cv2.fillPoly(mask, [points], 255)  # 填充掩码区域

# 获取被分割的像素索引
indices = np.where(mask == 255)

# 获取对应的 RGB 颜色 & 深度值
colors = image[indices] / 255.0  # 归一化到 [0,1]
z_values = depth[indices]  # 获取深度值

# 生成 3D 点云
fx, fy = 525.0, 525.0  # 相机内参 (示例)
cx, cy = width / 2, height / 2  # 主点 (示例)

points_3d = []
for i in range(len(indices[0])):
    u, v = indices[1][i], indices[0][i]  # 图像坐标 (x, y)
    z = z_values[i]  # 深度值
    if z > 0:  # 过滤无效深度
        x = (u - cx) * z / fx
        y = (v - cy) * z / fy
        points_3d.append([x, y, z, *colors[i]])  # 添加 RGB 信息

# 转换为 NumPy 数组
points_3d = np.array(points_3d)

# 创建 Open3D 点云对象
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points_3d[:, :3])  # 3D 坐标
pcd.colors = o3d.utility.Vector3dVector(points_3d[:, 3:])  # 颜色信息

# 保存 PLY 文件
o3d.io.write_point_cloud(out_path, pcd)

# 可视化点云
o3d.visualization.draw_geometries([pcd], window_name="Segmented Point Cloud")
