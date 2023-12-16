#@title <b>3) Adding weights to the world data map; data scaling functions</b>
##############################################################################################
# Weighted map generation (cost-adjustment)
##############################################################################################

# make penalty matrix for distance of points from the desired path
import numpy as np
from calculations import E6B_calculate

from csvData import get_desired_direction_d, get_shortest_dist_pt_to_line


def make_distance_from_straight_path_penalty(weighted_map,startidx,endidx,add_or_multiply,penalty_matrix_range):
  distance_from_path_penalty = np.zeros((weighted_map.shape[0],weighted_map.shape[1]))
  for y in range(weighted_map.shape[0]):
    for x in range(weighted_map.shape[1]):
      distance_from_path_penalty[y,x] = get_shortest_dist_pt_to_line(startidx,endidx,[x,y])
  distance_from_path_penalty = penalty_matrix_range*distance_from_path_penalty/np.amax(distance_from_path_penalty)
  if add_or_multiply=='add':
    weighted_map = np.add(weighted_map,distance_from_path_penalty)
  else:
    weighted_map = np.multiply(weighted_map,distance_from_path_penalty)
    weighted_map += penalty_matrix_range
  weighted_map -= np.amin(weighted_map)
  return weighted_map
  
# generate the weighted flight data map (costs must be scaled down to range(0-10))
def create_weighted_flight_data_map(world_data_table,startidx,endidx):
  normal_cost_range = 4     # set range for cost values
  distance_from_straight_path_penalty_range = 0.04   # set range for added cost values
  
  # E6B calculate airspeed at every index
  wid = world_data_table.shape[0]
  hei = world_data_table.shape[1]
  weighted_world_data_map = np.zeros((wid, hei))
  for i in range(wid):
    for j in range(hei):    # E6B ground speed calculation (km/hr)
      d_ = get_desired_direction_d([j,i],endidx)
      weighted_world_data_map[i,j] = E6B_calculate(3.6*world_data_table[i,j][0],world_data_table[i,j][1],Va,d_)
  
  # find max & min possible airspeed
  max_in_map = np.amax(weighted_world_data_map)   # km/hr
  min_in_map = np.amin(weighted_world_data_map)   # km/hr
  print('\nmax possible Vg: '+ str(max_in_map) + ' km/hr')
  print('min possible Vg: '+ str(min_in_map) + ' km/hr\n')

  # rescale the weighted wind map to fit heatmap showcasing
  weighted_world_data_map = weighted_world_data_map * ( normal_cost_range / max_in_map )

  # reverse weighting
  maxx = np.amax(weighted_world_data_map)
  weighted_world_data_map = (weighted_world_data_map*(-1)) + maxx

  # add slight penalty for being far from straight line path
  weighted_world_data_map = make_distance_from_straight_path_penalty(weighted_world_data_map, startidx, endidx,'add', distance_from_straight_path_penalty_range)
  
  return weighted_world_data_map


# generate the weighted elevation data map
def make_weighted_elevation_map(world_data_table,startidx,endidx):
  normal_cost_range = 0.5     # set range for cost values
  distance_from_straight_path_penalty_range = 0.1   # set range for added distance penalty cost values
  
  # apply normal_cost_range rescaling 
  weighted_map = world_data_table.copy()
  maxx = np.amax(weighted_map)
  minn = np.amin(weighted_map)
  if minn < 0:
    weighted_map = (weighted_map-minn) * (normal_cost_range / maxx)
  else:
    weighted_map = (weighted_map) * (normal_cost_range / maxx)

  # add penalty for being far from straight line path
  weighted_map = make_distance_from_straight_path_penalty(weighted_map, startidx, endidx,'add', distance_from_straight_path_penalty_range)
  
  return weighted_map