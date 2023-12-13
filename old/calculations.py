#@title <b>2) Calculation functions (i.e. PE gain for a road route)</b>

##############################################################################################
# Specific, Tailored Calculation Functions
# NOTE: These are a little separate from weighted_world_map cost-adjustment
##############################################################################################

# E6B calculator for flight speed calculation (Vg)
import math

from csvData import points_are_a_diagonal


def E6B_calculate(Vw1,w1,Va,d):
  try:
    deltaA = (180/math.pi) * math.asin(Vw1*math.sin((math.pi/180)*(w1-d)) / Va)
    Vg = math.sqrt(math.pow(Va,2) + math.pow(Vw1,2)-2*Va*Vw1*math.cos((math.pi/180)*(d + deltaA - w1)))
    return Vg
  except:
    print('winds are too strong to calculate airspeed')
    return 0

# calculate time (in hrs) for any given FLIGHT path
def calc_flight_time_for_path(shortst_len_path,dist_btwn_coordinates,world_data_table,Va=1500):
  # the below toggle method is to calculate ground speed Vg by averging the nearby windspeeds, rather
  # than using the current index Vg
  use_method_avg_every_2_pts = True
  
  total_time = 0
  diagonal_dist = math.sqrt(math.pow(dist_btwn_coordinates,2)+math.pow(dist_btwn_coordinates,2))
  for i in range(0, len(shortst_len_path)-1):
    # get dist
    is_diagonal = points_are_a_diagonal(shortst_len_path[i],shortst_len_path[i+1])
    if is_diagonal:
        dist = diagonal_dist
    else:
        dist = dist_btwn_coordinates
        
    # get direction of motion d
    if is_diagonal:
        d = 45
        if shortst_len_path[i+1][0]<shortst_len_path[i][0]:
            d = 180+45
    else:
        if shortst_len_path[i+1][0] - shortst_len_path[i][0]==0:
            if shortst_len_path[i+1][1]>shortst_len_path[i][1]:
                d=0
            else:
                d=180
        if shortst_len_path[i+1][1]-shortst_len_path[i][1]==0:
            if shortst_len_path[i+1][0]>shortst_len_path[i][0]:
                d=90
            else:
                d=270
    
    Vg=0
    if use_method_avg_every_2_pts:
      # get Vw, w from world_data_table (averaging first and second point's Vg)
      # multiply by 3.6 to convert m/s to km/hr
      Vw1 = 3.6*(world_data_table[shortst_len_path[i][1]][shortst_len_path[i][0]][0])      #km/hr
      w1 = world_data_table[shortst_len_path[i][1]][shortst_len_path[i][0]][1]
      Vg1 = E6B_calculate(Vw1,w1,Va,d)
      # averaging with next cell's Vg calculation
      Vw2 = 3.6*(world_data_table[shortst_len_path[i+1][1]][shortst_len_path[i+1][0]][0])   #km/hr
      w2 = world_data_table[shortst_len_path[i+1][1]][shortst_len_path[i+1][0]][1]
      Vg2 = E6B_calculate(Vw2,w2,Va,d)

      Vg = (Vg1 + Vg2)/2      # get resultant Vg (ground speed)
    
    elif use_method_avg_every_2_pts==False:
      Vw1 = 3.6*(world_data_table[shortst_len_path[i][1]][shortst_len_path[i][0]][0])      #km/hr
      w1 = world_data_table[shortst_len_path[i][1]][shortst_len_path[i][0]][1]
      Vg = E6B_calculate(Vw1,w1,Va,d)

    #print(Vg)
    t = dist/Vg
    total_time += t
  return total_time

# calculate timing difference between two given flight paths
def calc_optiroute_flight_timing_comparison(shortst_len_path,path,world_data_table,dist_btwn_coordinates):
  total_time_for_direct_path = calc_flight_time_for_path(shortst_len_path,dist_btwn_coordinates,world_data_table,Va)
  print('total time for for direct path (hrs): ' + str(total_time_for_direct_path))
  print('total time for for direct path (s): ' + str(total_time_for_direct_path*3600))
  
  total_time_for_optiroute = calc_flight_time_for_path(path,dist_btwn_coordinates,world_data_table,Va)
  print('total time for opti-path (hrs): ' + str(total_time_for_optiroute))
  print('total time for opti-path (s): ' + str(total_time_for_optiroute*3600))
  print('Opti-Route has saved ' + str(total_time_for_direct_path-total_time_for_optiroute) + ' hrs, or ' +\
        str(3600*(total_time_for_direct_path-total_time_for_optiroute)) + ' s')
  if total_time_for_direct_path-total_time_for_optiroute < 0:
    print('You may want to adjust your cost function (for generating weighted_world_map) to fit this specific data better\n\
    You can simply change the range of cost values in the function: create_weighted_flight_data_map()\n\
    or perform more complex mathematical changes to properize the data')  

# calculate energy usage difference between two given road paths
def energy_compare_2_road_routes(shortst_len_path, path,world_data_table,m=1):
  PE_prev = 0
  unwanted_energy_joules_path1=0

  # count the total increase in PE for path1
  for coor in shortst_len_path:
    PE = 9.8*m*world_data_table[coor[1],coor[0]]      # PE = m*g*(height gain)
    delta_PE = PE-PE_prev
    if delta_PE>0:
      unwanted_energy_joules_path1+=delta_PE
    PE_prev = PE
  PE_prev = 0

  # count the total increase in PE for path2
  unwanted_energy_joules_path2=0
  for coor in path:
    PE = 9.8*m*world_data_table[coor[1],coor[0]]      # PE = m*g*(height gain)
    delta_PE = PE-PE_prev
    if delta_PE>0:
      unwanted_energy_joules_path2+=delta_PE
    PE_prev = PE

  # compare the 2 PE gains
  print('For a frictionless sliding object of mass ' + str(m) + 'kg:\nThe shortest length route has '\
        + str(unwanted_energy_joules_path1) + ' joules of PE gain')
  print('Opti-route has only ' + str(unwanted_energy_joules_path2) + ' joules of PE gain')
  print('Opt-route has saved ' + str(unwanted_energy_joules_path1-unwanted_energy_joules_path2)\
        + ' joules')
  energy_saved = 100*(1-(unwanted_energy_joules_path2/unwanted_energy_joules_path1))
  print('Opti-route saves ' + str(energy_saved) + '% potential energy gain')
  if energy_saved < 0:
    print('You may want to adjust your cost function (for generating weighted_world_map) to fit this specific data better\n\
    You can simply change the range of cost values in the function: make_weighted_elevation_map()\n\
    or perform more complex mathematical changes to properize the data')