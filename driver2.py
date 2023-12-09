#@title <b>6) Driver code part 2: run the optimizer</b>
##############################################################################################
# DRIVER CODE - part 2: calculation & backend work
##############################################################################################

# CREATE THE BOUNDS FOR THE RECT REGION
import numpy as np
from calculations import calc_optiroute_flight_timing_comparison, energy_compare_2_road_routes

from csvData import create_region_rect_region_boundaries, get_desired_direction_d, get_shortest_length_path, read_table_from_csv
from optimization import optimize_path, show_optipath_coors
from weights import create_weighted_flight_data_map


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