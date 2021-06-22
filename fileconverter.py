import open3d as o3d
import numpy as np
from pathlib import Path
from PIL import Image

def convert_npy_ply(npy_array_path):
	npy_array = np.load(npy_array_path)
	npy_array = np.swapaxes(npy_array, 1,3)
	npy_array = np.swapaxes(npy_array, 2,3)
	npy_array = npy_array[0,:,:,:]
	print(npy_array.shape)
	npy_array_name = Path(npy_array_path).stem
	img = Image.fromarray(npy_array)
	# pcd = o3d.geometry.PointCloud()
	# pcd.points = o3d.utility.Vector3dVector(npy_array)
	# rgb = o3d.geometry.RGBDImage.create_from_color_and_depth(npy_array, npy_array)
	# o3d.io.write_point_cloud("labelCloud/pointclouds/" + npy_array_name + ".ply", pcd)

convert_npy_ply("data/A18-1 HuChP ThS + Hoechst 2 spacer 40x.npy")