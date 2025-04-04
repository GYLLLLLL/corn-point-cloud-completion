import bpy
import random
import os


# ===== 1️⃣ 清除已有模型（可选）=====
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()


# ===== 2️⃣ 导入 PLY 玉米模型 =====
def import_ply(file_path):
    bpy.ops.wm.ply_import(filepath=file_path)
    corn = bpy.context.selected_objects[0]  # 获取导入的模型
    return corn


# ===== 3️⃣ 对玉米进行随机变换 =====
def random_transform(obj):
    obj.location.x += random.uniform(-2.0, 2.0)  # 随机平移 X
    obj.location.y += random.uniform(-2.0, 2.0)  # 随机平移 Y
    obj.location.z += random.uniform(-1.0, 1.0)  # 随机平移 Z

    obj.rotation_euler.x += random.uniform(-0.5, 0.5)  # 随机旋转 X
    obj.rotation_euler.y += random.uniform(-0.5, 0.5)  # 随机旋转 Y
    obj.rotation_euler.z += random.uniform(-1.0, 1.0)  # 随机旋转 Z

    scale_factor = random.uniform(0.8, 1.2)  # 允许轻微缩放
    obj.scale = (scale_factor, scale_factor, scale_factor)


# ===== 4️⃣ 导出变换后的 PLY 文件 =====
def export_ply(obj, output_path):
    # 确保仅导出选中的模型
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.wm.ply_export(filepath=output_path)


# ===== 5️⃣ 运行完整流程 =====
def process_corn_ply(input_ply, output_folder, num_variations=5):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    clear_scene()  # 清理场景（可选）

    for i in range(num_variations):
        corn = import_ply(input_ply)  # 重新导入原始 PLY
        random_transform(corn)  # 变换模型

        output_ply_path = os.path.join(output_folder, f"corn_variant_{i + 1}.ply")
        export_ply(corn, output_ply_path)  # 导出 PLY
        clear_scene()
        print(f"✅ 生成并导出 {output_ply_path}")

    print("🚀 所有 PLY 生成完成！")


# ===== 6️⃣ 设置路径并运行 =====
input_ply_file = r"D:\point cloud 6D pose\make data\output.ply"  # 你的玉米 PLY 文件路径
output_directory = r"D:\point cloud 6D pose\make data\save_ply_single2"  # 变换后 PLY 文件的存储路径
num_corns = 5  # 生成 5 个不同的变换版本

process_corn_ply(input_ply_file, output_directory, num_corns)
