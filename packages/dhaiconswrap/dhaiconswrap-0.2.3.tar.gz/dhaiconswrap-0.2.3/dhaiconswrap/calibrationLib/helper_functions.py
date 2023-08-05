##################################################################################################
##       License: Apache 2.0. See LICENSE file in root directory.		                      ####
##################################################################################################
##                  Box Dimensioner with multiple cameras: Helper files 					  ####
##################################################################################################

# Opencv helper functions and class
import cv2
import numpy as np

import warnings
warnings.filterwarnings("error")

"""
  _   _        _                      _____                     _    _
 | | | |  ___ | | _ __    ___  _ __  |  ___|_   _  _ __    ___ | |_ (_)  ___   _ __   ___
 | |_| | / _ \| || '_ \  / _ \| '__| | |_  | | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
 |  _  ||  __/| || |_) ||  __/| |    |  _| | |_| || | | || (__ | |_ | || (_) || | | |\__ \
 |_| |_| \___||_|| .__/  \___||_|    |_|    \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
				 _|
"""

def calculate_rmsd(points1, points2, validPoints=None):
	"""
	calculates the root mean square deviation between to point sets

	Parameters:
	-------
	points1, points2: numpy matrix (K, N)
	where K is the dimension of the points and N is the number of points

	validPoints: bool sequence of valid points in the point set.
	If it is left out, all points are considered valid
	"""
	assert(points1.shape == points2.shape)
	N = points1.shape[1]

	if validPoints == None:
		validPoints = [True]*N

	assert(len(validPoints) == N)

	points1 = points1[:,validPoints]
	points2 = points2[:,validPoints]

	N = points1.shape[1]

	dist = points1 - points2
	rmsd = 0
	for col in range(N):
		rmsd += np.matmul(dist[:,col].transpose(), dist[:,col]).flatten()[0]

	return np.sqrt(rmsd/N)


def get_chessboard_points_3D(chessboard_params):
	"""
	Returns the 3d coordinates of the chessboard corners
	in the coordinate system of the chessboard itself.

	Returns
	-------
	objp : array
		(3, N) matrix with N being the number of corners
	"""
	assert(len(chessboard_params) == 3)
	width = chessboard_params[0]
	height = chessboard_params[1]
	square_size = chessboard_params[2]
	objp = np.zeros((width * height, 3), np.float32)
	objp[:,:2] = np.mgrid[0:width,0:height].T.reshape(-1,2)
	return objp.transpose() * square_size/1000


def cv_find_chessboard(color_frame, chessboard_params):
	"""
	Searches the chessboard corners using the set infrared image and the
	checkerboard size

	Returns:
	-----------
	chessboard_found : bool
						  Indicates wheather the operation was successful
	corners          : array
						  (2,N) matrix with the image coordinates of the chessboard corners
	"""
	assert(len(chessboard_params) == 3)
	color_to_gray = cv2.cvtColor(color_frame,cv2.COLOR_RGB2GRAY)
	color_copy = color_frame.copy()
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
	chessboard_found = False
	chessboard_found, corners = cv2.findChessboardCorners(color_to_gray, (chessboard_params[0], chessboard_params[1]))

	if chessboard_found:
		corners = cv2.cornerSubPix(color_to_gray, corners, (5,5),(-1,-1), criteria)
		corners = np.transpose(corners, (2,0,1))
		if corners is not None:
			first = True
			cornersBis = corners.squeeze()
			cornersBis = cornersBis.T
			for corner in cornersBis:
				if not first:
					cv2.circle(color_copy,corner.astype(int),2,(0,255,0),-1)
				else:
					cv2.circle(color_copy,corner.astype(int),2,(0,0,255),-1)
					first = False

	return chessboard_found, corners, color_copy



def get_depth_at_pixel(depth_frame, pixel_x, pixel_y):
	"""
	Get the depth value at the desired image point

	Parameters:
	-----------
	depth_frame 	 : rs.frame()
						   The depth frame containing the depth information of the image coordinate
	pixel_x 	  	 	 : double
						   The x value of the image coordinate
	pixel_y 	  	 	 : double
							The y value of the image coordinate

	Return:
	----------
	depth value at the desired pixel

	"""

	return depth_frame[round(pixel_y), round(pixel_x)]


# def convert_metric_coordinate_to_depth_pixel(x, y, z, camera_intrinsics):
# 	"""
# 	Convert the depth and image point information to metric coordinates

# 	Parameters:
# 	-----------
# 	depth 	 	 	 : double
# 						   The depth value of the image point
# 	pixel_x 	  	 	 : double
# 						   The x value of the image coordinate
# 	pixel_y 	  	 	 : double
# 							The y value of the image coordinate
# 	camera_intrinsics : The intrinsic values of the imager in whose coordinate system the depth_frame is computed

# 	Return:
# 	----------
# 	X : double
# 		The x value in meters
# 	Y : double
# 		The y value in meters
# 	Z : double
# 		The z value in meters

# 	"""
# 	pixel_x = X * camera_intrinsics.fx *depth + camera_intrinsics.ppx
# 	pixel_y = Y * camera_intrinsics.fy *depth + camera_intrinsics.ppy
# 	return pixel_x, pixel_y


def convert_depth_pixel_to_metric_coordinate(depth, pixel_x, pixel_y, camera_intrinsics):
	"""
	Convert the depth and image point information to metric coordinates

	Parameters:
	-----------
	depth 	 	 	 : double
						   The depth value of the image point
	pixel_x 	  	 	 : double
						   The x value of the image coordinate
	pixel_y 	  	 	 : double
							The y value of the image coordinate
	camera_intrinsics : The intrinsic values of the imager in whose coordinate system the depth_frame is computed

	Return:
	----------
	X : double
		The x value in meters
	Y : double
		The y value in meters
	Z : double
		The z value in meters

	"""
	X = (pixel_x - camera_intrinsics.cx)/camera_intrinsics.fx *depth
	Y = (pixel_y - camera_intrinsics.cy)/camera_intrinsics.fy *depth
	return X, Y, depth



def convert_depth_frame_to_pointcloud(depth_image, camera_intrinsics,dofilter = True):
	"""
	Convert the depthmap to a 3D point cloud

	Parameters:
	-----------
	depth_frame 	 	 : rs.frame()
						   The depth_frame containing the depth map
	camera_intrinsics : The intrinsic values of the imager in whose coordinate system the depth_frame is computed

	Return:
	----------
	x : array
		The x values of the pointcloud in meters
	y : array
		The y values of the pointcloud in meters
	z : array
		The z values of the pointcloud in meters

	"""

	[height, width] = depth_image.shape

	nx = np.linspace(0, width-1, width)
	ny = np.linspace(0, height-1, height)

	u, v = np.meshgrid(nx, ny)
	x = (u.flatten() - camera_intrinsics.ppx)/camera_intrinsics.fx
	y = (v.flatten() - camera_intrinsics.ppy)/camera_intrinsics.fy

	z = depth_image.flatten() / 1000
	x = np.multiply(x,z)
	y = np.multiply(y,z)

	if dofilter:
		valid_index = np.nonzero(z)

		x = x[valid_index]
		y = y[valid_index]
		z = z[valid_index]

	return (x, y, z)


def convert_pointcloud_to_depth(pointcloud, camera_intrinsics):
	"""
	Convert the world coordinate to a 2D image coordinate

	Parameters:
	-----------
	pointcloud 	 	 : numpy array with shape 3xN

	camera_intrinsics : The intrinsic values of the imager in whose coordinate system the depth_frame is computed

	Return:
	----------
	x : array
		The x coordinate in image
	y : array
		The y coordiante in image

	"""

	assert (pointcloud.shape[0] == 3)
	x_ = pointcloud[0,:]
	y_ = pointcloud[1,:]
	z_ = pointcloud[2,:]

	m = x_[np.nonzero(z_)]/z_[np.nonzero(z_)]
	n = y_[np.nonzero(z_)]/z_[np.nonzero(z_)]

	x = m*camera_intrinsics.fx + camera_intrinsics.ppx
	y = n*camera_intrinsics.fy + camera_intrinsics.ppy

	return x, y



def get_boundary_corners_2D(points):
	"""
	Get the minimum and maximum point from the array of points
	
	Parameters:
	-----------
	points 	 	 : array
						   The array of points out of which the min and max X and Y points are needed
	
	Return:
	----------
	boundary : array
		The values arranged as [minX, maxX, minY, maxY]
	
	"""
	padding=0.05
	if points.shape[0] == 3:
		assert (len(points.shape)==2)
		minPt_3d_x = np.amin(points[0,:])
		maxPt_3d_x = np.amax(points[0,:])
		minPt_3d_y = np.amin(points[1,:])
		maxPt_3d_y = np.amax(points[1,:])

		boudary = [minPt_3d_x-padding, maxPt_3d_x+padding, minPt_3d_y-padding, maxPt_3d_y+padding]

	else:
		raise Exception("wrong dimension of points!")

	return boudary



def get_clipped_pointcloud(pointcloud, point_color_cloud, point_cloud_base, boundary):
	"""
	Get the clipped pointcloud withing the X and Y bounds specified in the boundary
	
	Parameters:
	-----------
	pointcloud 	 	 : array
						   The input pointcloud which needs to be clipped
	boundary      : array
										The X and Y bounds 
	
	Return:
	----------
	pointcloud : array
		The clipped pointcloud
	
	"""
	assert (pointcloud.shape[0]>=2)

	filter1 = np.logical_and(pointcloud[0,:]<boundary[1], pointcloud[0,:]>boundary[0])
	pointcloud = pointcloud[:,filter1]
	point_color_cloud = point_color_cloud[:,filter1]
	point_cloud_base = point_cloud_base[:,filter1] 

	filter2 = np.logical_and(pointcloud[1,:]<boundary[3], pointcloud[1,:]>boundary[2])
	pointcloud = pointcloud[:,filter2]
	point_color_cloud = point_color_cloud[:,filter2]
	point_cloud_base = point_cloud_base[:,filter2]
	
	return pointcloud, point_color_cloud, point_cloud_base

def get_vector_angle_XY_plane(C, V):
	u = V - C
	p = projectvector_onplane(np.array([0,0,1]) ,u)
	return np.arctan2(p[1], p[0])


def projecttranslatevector_onplan(C, n , u, norm = None):

	n = n - C
	u = u - C
	p = projectvector_onplane(n ,u)

	p_norm = np.sqrt(sum(np.square(p)))
	if norm is not None and p_norm > 0:
		p = p / p_norm * norm

	return p + C


def projectvector_onplane(n ,u):

	# Task: Project vector u on Plane P 

	# finding norm of the vector n  
	n_norm = np.sqrt(sum(n**2))     

	# Apply the formula as mentioned above 
	# for projecting a vector onto the orthogonal vector n 
	# find dot product using np.dot() 
	return u - (np.dot(u, n)/n_norm**2)*n 

def normalVector(obj):
    """ Takes a set of points, assumed to be flat, and returns a normal vector with unit length.
    """
    n = np.cross(np.array(obj[1])-np.array(obj[0]), np.array(obj[2])-np.array(obj[0]))
    return n/np.sqrt(np.dot(n,n))


def rotateVector3D(v, theta, axis):
    """ Takes a three-dimensional vector v and rotates it by the angle theta around the specified axis.
    """
    return np.dot(v,rotationMatrix3D(theta, axis).T) #np.dot(rotationMatrix3D(theta, axis), v.T).T


def rotationMatrix3D(theta, axis):
    """ Return the rotation matrix associated with counterclockwise rotation about
        the given axis by theta radians.
    """
    axis = np.asarray(axis) / np.sqrt(np.dot(axis, axis)) 
    a = np.cos(theta/2.0)
    b, c, d = -axis*np.sin(theta/2.0)
    aa, bb, cc, dd = a**2, b**2, c**2, d**2
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])


# create empy variables for detection
def InitCloudArrays(frames_devices):

	XYZ_cloud_valid_bycam = {}
	RGB_cloud_valid_bycam = {}
	XYZ_map_valid_bycam = {}
	RGB_map_valid_bycam = {}
	BOX_valid_bycam = {}
	RGB_cloud_filter_valid_bycam = {}
	colorimages_base_bycam = {}
	colorimages_filtered_bycam = {}
	valid_tex = {}

	for (device, _) in frames_devices.items():
		XYZ_cloud_valid_bycam[device] = []
		RGB_cloud_valid_bycam[device] = []
		XYZ_map_valid_bycam[device] = []
		RGB_map_valid_bycam[device] = []
		BOX_valid_bycam[device] = []
		RGB_cloud_filter_valid_bycam[device] = []
		colorimages_base_bycam[device] = []
		colorimages_filtered_bycam[device] = []
		valid_tex[device] = False

	return XYZ_cloud_valid_bycam, RGB_cloud_valid_bycam, XYZ_map_valid_bycam, RGB_map_valid_bycam, BOX_valid_bycam, RGB_cloud_filter_valid_bycam, colorimages_base_bycam, colorimages_filtered_bycam, valid_tex

