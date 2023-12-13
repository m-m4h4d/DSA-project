#@title <b>5) Driver code part 1: general parameter initialization</b>
##############################################################################################
# DRIVER CODE - part 1: adjustable parameters
##############################################################################################

#===========================================
# SECTION 1: Initializing basic flight path parameters

# SETTING THE DEPENDENCY FILES
# NOTE: the files must both start at the same exact lat/lon index and increment
# upward from there. The increment sizes must be the same for both. But they can
# end at different coordinates.
import time


lets_optimize_a_road_route = True
lets_optimize_a_flight_route = False

# coordinates file is OPTIONAL
using_coordinates_table = False
coordinates_file = 'sample_data/california_housing_test.csv'      #set the lat/lon coordinates file

# SET THE PARAMS IF WE'RE OPTIMIZING A FLIGHT
if lets_optimize_a_flight_route:
  world_data_file = 'sample_data/mnist_test.csv'    #set the wind map file
  
  dist_btwn_coordinates = 2*1.609344      # 2mi -> km   (for accurate distance calculation)
  Va = 1500       # airspeed (km/hr)
  # NOTE: wind speed data MUST BE in m/s

# SET THE PARAMS IF WE'RE OPTIMIZING A ROAD ROUTE
elif lets_optimize_a_road_route:
  world_data_file = 'sample_data/california_housing_train.csv'


# DECLARING PATH ORIGIN/DESTINATION
# NOTE: Algorithm works best if start_idx[x,y] has x=0
# FORMAT: [col, row]
#     0 1 2 3 4
#   0
#   1
#   2
#   3
starttime = time.time()
start_idx = [0,31]   # origin (x, y) index - corresponds to world data file and optional coordinates file
end_idx = [107,241]     # destination (x, y) index - corresponds to world data file and optional coordinates file

#@title <b>6) Driver code part 2: run the optimizer</b>
##############################################################################################
# DRIVER CODE - part 2: calculation & backend work
##############################################################################################

# CREATE THE BOUNDS FOR THE RECT REGION
import numpy as np
from calculations import calc_optiroute_flight_timing_comparison, energy_compare_2_road_routes

from csvData import create_region_rect_region_boundaries, get_desired_direction_d, get_shortest_length_path, read_table_from_csv, rescale_region_rect_region_idxs, show_orig_and_dest_pts
from optimization import optimize_path, show_optipath_coors
from weights import create_weighted_flight_data_map, make_weighted_elevation_map


region_rect_lowright_idx,region_rect_upleft_idx = create_region_rect_region_boundaries(start_idx,end_idx,world_data_file)
# EXTRACT MAP COORDINATES TABLE INTO GIANT ARRAY
try:
  coordinates_table= np.array(read_table_from_csv(coordinates_file, region_rect_upleft_idx, region_rect_lowright_idx))
except:
  using_coordinates_table = False
  coordinates_table = []
world_data_table= np.array(read_table_from_csv(world_data_file, region_rect_upleft_idx, region_rect_lowright_idx))
# RESCALE OUR MAP RECTANGLE REGION INDEXES - subtract to 0 to fit our data table, rather than csv indexing
index_x_diff,index_y_diff = rescale_region_rect_region_idxs(start_idx,end_idx,region_rect_lowright_idx,region_rect_upleft_idx)
show_orig_and_dest_pts(using_coordinates_table,coordinates_table,start_idx,end_idx,index_x_diff,index_y_diff)   # show origin & destination pts

# CREATE WEIGHTED WORLD MAP
if lets_optimize_a_flight_route:
  d_pref = get_desired_direction_d(start_idx,end_idx)   # get desired direction d
  weighted_world_data_map = create_weighted_flight_data_map(world_data_table,start_idx,end_idx)   # create weighted wind map

elif lets_optimize_a_road_route:
  weighted_world_data_map = make_weighted_elevation_map(world_data_table,start_idx,end_idx)

#===========================================
# SECTION 2: OPTIMAL ROUTE FINDING

# optimize the path
rotation_message = ""
path,rotation_message = optimize_path(start_idx,end_idx,region_rect_lowright_idx,region_rect_upleft_idx,weighted_world_data_map,rotation_message)
shortst_len_path = get_shortest_length_path(start_idx,end_idx,region_rect_lowright_idx,region_rect_upleft_idx)  # find shortest-length path from orig to dest

# calculating time for shortest-2D-length path versus original path
if lets_optimize_a_flight_route:
  calc_optiroute_flight_timing_comparison(shortst_len_path,path,world_data_table,dist_btwn_coordinates)
elif lets_optimize_a_road_route:
  energy_compare_2_road_routes(shortst_len_path, path, world_data_table,m=100)    # m = vehicle mass

#===========================================
# final output showcasing

display_path = False
show_optipath_coors(using_coordinates_table,path,coordinates_table,index_x_diff, index_y_diff,display_path)   # display path
#print('program execution time: ' + str(time.time() - starttime)+ '\n')
if len(rotation_message)>0:
  print(rotation_message)
#print('temp path indexes (x,y) (for path plot visual):\norigin:' + str(start_idx) + ', destination: ' + str(end_idx)+ '\n')