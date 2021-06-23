import open3d as o3d
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

def convert_npy_ply(npy_array_path):
	npy_array_name = Path(npy_array_path).stem
	npy_array = np.load(npy_array_path)
	d, h, w, c = npy_array.shape

	color_img = npy_array[0,:,:,:] # (h, w, c) first image in stack
	depth_img = np.ones((h, w, 1)) # (h, w) depth
	color_img = o3d.geometry.Image(color_img.astype(np.uint8))
	depth_img = o3d.geometry.Image(depth_img.astype(np.uint8))

	rgbd_img = o3d.geometry.RGBDImage.create_from_color_and_depth(color_img, depth_img)
	# print(rgbd_img)
	# plt.imshow(rgbd_img.color)
	# plt.show()
	# plt.imshow(rgbd_img.depth)
	# plt.show()
	pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
		rgbd_img,
		o3d.camera.PinholeCameraIntrinsic(w, h, 10000000,10000000, w/2, h/2))
	# Flip it, otherwise the pointcloud will be upside down
	# pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])

	# print(np.asarray(pcd.points).shape)

	for i in range(2, d):
		color_img = npy_array[i,:,:,:]
		depth_img = np.ones((h,w, 1)) * i
		color_img = o3d.geometry.Image(color_img.astype(np.uint8))
		depth_img = o3d.geometry.Image(depth_img.astype(np.uint8))

		rgbd_img = o3d.geometry.RGBDImage.create_from_color_and_depth(color_img, depth_img)
		point_cloud = o3d.geometry.PointCloud.create_from_rgbd_image(
			rgbd_img,
			o3d.camera.PinholeCameraIntrinsic(w, h, 10000000,10000000, w/2, h/2))
		# print(np.asarray(point_cloud).shape)
		# Flip it, otherwise the pointcloud will be upside down
		# point_cloud.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
		pcd += point_cloud
		# print(np.asarray(pcd).shape)

	# # pcd = o3d.geometry.PointCloud()
	# # pcd.points = o3d.utility.Vector3dVector(npy_array)
	
	# o3d.io.write_point_cloud("labelCloud/pointclouds/" + npy_array_name + ".ply", pcd)
	o3d.visualization.draw_geometries([pcd])

convert_npy_ply("data/A18-1 HuChP ThS + Hoechst 2 spacer 40x.npy")