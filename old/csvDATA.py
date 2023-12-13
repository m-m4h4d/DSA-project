#@title <b>1) Initial csv-reading tasks</b>

#!pip install substring
import math
import re
# import substring
import csv
import numpy as np
import time
import matplotlib.pyplot as plt
# from numpy import genfromtxt


##############################################################################################
# Initial tasks (mostly csv-reading)
##############################################################################################

# get the end coor of a csv
def find_end_coor_of_csv(filename):
   num_rows=0
   num_cols=0
   with open(filename, newline='') as f:
       reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
       for row in reader:
           num_cols=len(row)
           break
       num_rows = len(f.readlines())+1
   return [num_cols-1,num_rows-1]     # (x, y)
# debugging function for printing things
def disp(coordinates_table, name='~'):
   print('')
   if isinstance(coordinates_table, float):        #if is a float
       if name != '~':
           print(name + ": " + str(coordinates_table))
       else: print(coordinates_table)
       print('')
       return

   if name != '~':
       print(name + ":")
   #check if is 1D or 2D array
   is_1D = False
   try:
       for row in coordinates_table:
           trash = len(row)
           break
   except TypeError:
       is_1D = True
    
   if is_1D == False:              #if is 2D array
       for row in coordinates_table:
           print((row))
   else:                           #if is 1D array
       print(coordinates_table)
   print('')

# string_stream function
# credit to butch---https://stackoverflow.com/questions/21843693/creating-stream-to-iterate-over-from-string-in-python
def string_stream(s, separators="_"):
   start = 0
   for end in range(len(s)):
       if s[end] in separators:
           yield s[start:end]
           start = end + 1
   if start < end:
       yield s[start:end+1]
# get our map data (without reading entire csv) - works for both types: single and double nums per csv cell
def read_table_from_csv(coordinates_file, region_rect_upleft_idx, region_rect_lowright_idx):
   coordinates_table = []
   on_first_cell = True
   csv_cell_has_multiple_nums= False
   with open(coordinates_file, newline='') as f:
       reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
       row_idx = 0
       for row in reader:
           # start/stop checking
           if row_idx < region_rect_upleft_idx[1]:
               row_idx+=1
               continue
           if row_idx == region_rect_lowright_idx[1]+1:
               break
        
           col_idx = 0
           coordinates_table_row = []
           for item in row:
               # start/stop checking
               if col_idx < region_rect_upleft_idx[0]:
                   col_idx+=1
                   continue
               if col_idx == region_rect_lowright_idx[0]+1:
                   break

               # check if we have multiple nums in a cell
               if on_first_cell:
                   on_first_cell = False
                   if '_' in str(item):
                       csv_cell_has_multiple_nums = True
                   else: csv_cell_has_multiple_nums = False
               # extract cell data (whether single or multiple nums per cell)
               if csv_cell_has_multiple_nums:
                   csv_cell = str(item)
                   csv_cell = re.sub("b", "", csv_cell)
                   csv_cell = re.sub("'", "", csv_cell)
                   csv_cell+=''   # safety append an extra '' for string stream parsing

                   stream = string_stream(csv_cell, "_")       #string stream
                   coordinate = []
                   for s in stream:
                       coordinate.append(float(s))
                   coordinates_table_row.append(coordinate)
               if not csv_cell_has_multiple_nums:
                   coordinates_table_row.append(float(item))
               col_idx +=1
           row_idx +=1
           coordinates_table.append(coordinates_table_row)
   return coordinates_table


##############################################################################################
# Standard path region size adjusment
##############################################################################################

# function to thicken the path rectangular region if too thin, by changing the boundary indexes
def widen_region_path_rect__boundaries(region_rect_lowright_idx,region_rect_upleft_idx,max_allowable_idx):
  while region_rect_lowright_idx[0]-region_rect_upleft_idx[0]<0.5*(region_rect_lowright_idx[1]-region_rect_upleft_idx[1]):
    if region_rect_upleft_idx[0] > 0:
        region_rect_upleft_idx[0] -=1
    if region_rect_lowright_idx[0] < max_allowable_idx[0]:
        region_rect_lowright_idx[0] +=1

  while region_rect_lowright_idx[1]-region_rect_upleft_idx[1]<0.5*(region_rect_lowright_idx[0]-region_rect_upleft_idx[0]):
    if region_rect_upleft_idx[1] > 0:
        region_rect_upleft_idx[1] -=1
    if region_rect_lowright_idx[1] < max_allowable_idx[1]:
        region_rect_lowright_idx[1] +=1
    
# CREATING BOUNDS FOR THE PATH RECTANGLE REGION
def create_region_rect_region_boundaries(start_idx,end_idx,world_data_file):
  cur_idx = start_idx.copy()
  region_rect_lowright_idx = [max(start_idx[0],end_idx[0]),max(start_idx[1],end_idx[1])]
  region_rect_upleft_idx = [min(start_idx[0],end_idx[0]),min(start_idx[1],end_idx[1])]
  
  # max_allowable_idx1 = find_end_coor_of_csv(coordinates_file)
  max_allowable_idx = find_end_coor_of_csv(world_data_file)

  #fix outer indexes of flight path rectangle if rectangle is too thin
  widen_region_path_rect__boundaries(region_rect_lowright_idx,region_rect_upleft_idx,max_allowable_idx)
  return region_rect_lowright_idx, region_rect_upleft_idx

# rescale the flight rect region indexes (fit original csv indexing to our table indexing)
def rescale_region_rect_region_idxs(start_idx,end_idx,region_rect_lowright_idx,region_rect_upleft_idx):
  index_x_diff = region_rect_upleft_idx[0]
  index_y_diff = region_rect_upleft_idx[1]
  region_rect_upleft_idx[0] -= index_x_diff
  region_rect_upleft_idx[1] -= index_y_diff
  region_rect_lowright_idx[0] -= index_x_diff
  region_rect_lowright_idx[1] -= index_y_diff
  start_idx[0] -= index_x_diff
  start_idx[1] -= index_y_diff
  end_idx[0] -= index_x_diff
  end_idx[1] -= index_y_diff
  return index_x_diff, index_y_diff



##############################################################################################
# Standard grid calculation functions
##############################################################################################

# Function to find shortest distance from pt to line
# credit to https://www.geeksforgeeks.org/perpendicular-distance-between-a-point-and-a-line-in-2-d/
def get_shortest_dist_pt_to_line(orig,dest,pt):
  try:
    x1,y1 = pt[1],pt[0]
    #temp = x1
    #x1 = y1
    #y1 = temp
    a = 1
    b = -(dest[1]-orig[1])/(dest[0]-orig[0])
    c = (-1)*orig[1]+(-1)(b)*orig[0]
    d = abs((a * x1 + b * y1 + c)) / (math.sqrt(a * a + b * b))
    return d
  except:
    return 0

# find desired direction of motion based on start and end idx
def get_desired_direction_d(start_idx,end_idx):
  x = end_idx[0]-start_idx[0]
  y = end_idx[1]-start_idx[1]
  # disp(x,'x')
  # disp(y,'y')
  if x<0 and y>0:
    d_pref = 270+math.atan((-1*y)/x)*180/math.pi
  elif x>0 and y>0:
    d_pref = 90-math.atan(y/x)*180/math.pi
  elif x<0 and y<0:
    d_pref = 270-math.atan(y/x)*180/math.pi
  elif x>0 and y<0:
    d_pref = 90+math.atan((-1*y)/x)*180/math.pi
  elif x==0 and y<0:
    d_pref=180
  elif x==0 and y>0:
    d_pref=0
  elif y==0 and x<0:
    d_pref=270
  elif y==0 and x>0:
    d_pref=90
  else:
    d_pref=0
  return d_pref

# show origin & destination pts
def show_orig_and_dest_pts(using_coordinates_table,coordinates_table,start_idx,end_idx,index_x_diff,index_y_diff):
  if using_coordinates_table:
    trash = 0
    # print('origin (lat/lon): ' + str(coordinates_table[start_idx[1],start_idx[0]]) + \
    #       ', destination: ' + str(coordinates_table[end_idx[1],end_idx[0]]) + '\n')
    # # print('(x,y) temp path indexes (for path plot visual): ' + str(start_idx) + ", " + str(end_idx) + '\n')   # (x, y)
  elif not using_coordinates_table:
    trash = 0
    # print('csv index (x,y)\norigin: ' + str([start_idx[0]+index_x_diff,start_idx[1]+index_y_diff]) + \
    #       ', destination: ' + str([end_idx[0]+index_x_diff,end_idx[1]+index_y_diff]) + '\n')

def dist_btwn_idxs(cur_idx,end_idx):    # find Euclidean distance between 2 table indexes
  d = math.sqrt(math.pow(end_idx[0]-cur_idx[0],2)+math.pow(end_idx[1]-cur_idx[1],2))
  return d

# GET THE SHORTEST LENGTH PATH FROM START IDX TO END IDX
def get_shortest_length_path(start_idx,end_idx,region_rect_lowright_idx,region_rect_upleft_idx):
  cur_idx = start_idx.copy()
  idx_path = [start_idx.copy()]
  # print('start idx: '+ str(start_idx))
  # print('end idx: '+ str(end_idx))
  # print('shortest distance path from start to end: indexes:')
  # print(start_idx)

  while cur_idx != end_idx:
    cur_dist_to_end = dist_btwn_idxs(cur_idx,end_idx)
    new_idx = cur_idx.copy()
    min_pt_dist_to_line = 99999999

    # # if pts are along completely straight line
    # if start_idx[0]==end_idx[0]:    # if delta x = 0
    #   if start_idx[1]>end_idx[1]:   # delta y < 0
    #     new_idx[1] = cur_idx[1] + 1     #y up, x same
    #     new_idx[0] = cur_idx[0]
    #     idx_path.append(cur_idx)
    #     continue
    #   elif dest[1]<orig[1]:   # delta y > 0
    # if start_idx[1]==end_idx[1]:    # if delta y = 0

    if cur_idx[1] + 1 <= region_rect_lowright_idx[1]:
        new_idx[1] = cur_idx[1] + 1     #y up, x same
        new_idx[0] = cur_idx[0]
        if dist_btwn_idxs(new_idx,end_idx) < cur_dist_to_end:
            pt_dist_to_line = get_shortest_dist_pt_to_line(start_idx,end_idx,new_idx)
            if pt_dist_to_line < min_pt_dist_to_line:
                min_pt_dist_to_line = pt_dist_to_line
                saved_idx = new_idx.copy()

    if cur_idx[1] - 1 >= region_rect_upleft_idx[1]:
        new_idx[1] = cur_idx[1] - 1     #y down, x same
        new_idx[0] = cur_idx[0]
        if dist_btwn_idxs(new_idx,end_idx) < cur_dist_to_end:
            pt_dist_to_line = get_shortest_dist_pt_to_line(start_idx,end_idx,new_idx)
            if pt_dist_to_line < min_pt_dist_to_line:
                min_pt_dist_to_line = pt_dist_to_line
                saved_idx = new_idx.copy()
    if cur_idx[1] + 1 <= region_rect_lowright_idx[1] and cur_idx[0]+1 <= region_rect_lowright_idx[0]:
        new_idx[1] = cur_idx[1] + 1     #y up, x up
        new_idx[0] = cur_idx[0] + 1
        if dist_btwn_idxs(new_idx,end_idx) < cur_dist_to_end:
            pt_dist_to_line = get_shortest_dist_pt_to_line(start_idx,end_idx,new_idx)
            if pt_dist_to_line < min_pt_dist_to_line:
                min_pt_dist_to_line = pt_dist_to_line
                saved_idx = new_idx.copy()
    if cur_idx[1] - 1 >= region_rect_upleft_idx[1] and cur_idx[0]-1 >= region_rect_upleft_idx[0]:
        new_idx[1] = cur_idx[1] - 1     #y down, x down
        new_idx[0] = cur_idx[0] - 1
        if dist_btwn_idxs(new_idx,end_idx) < cur_dist_to_end:
            pt_dist_to_line = get_shortest_dist_pt_to_line(start_idx,end_idx,new_idx)
            if pt_dist_to_line < min_pt_dist_to_line:
                min_pt_dist_to_line = pt_dist_to_line
                saved_idx = new_idx.copy()
    if cur_idx[0]-1 >= region_rect_upleft_idx[0]:
        new_idx[1] = cur_idx[1]         #y same, x down
        new_idx[0] = cur_idx[0] - 1
        if dist_btwn_idxs(new_idx,end_idx) < cur_dist_to_end:
            pt_dist_to_line = get_shortest_dist_pt_to_line(start_idx,end_idx,new_idx)
            if pt_dist_to_line < min_pt_dist_to_line:
                min_pt_dist_to_line = pt_dist_to_line
                saved_idx = new_idx.copy()
    if cur_idx[0]+1 <= region_rect_lowright_idx[0]:
        new_idx[1] = cur_idx[1]          #y same, x up
        new_idx[0] = cur_idx[0] + 1
        if dist_btwn_idxs(new_idx,end_idx) < cur_dist_to_end:
            pt_dist_to_line = get_shortest_dist_pt_to_line(start_idx,end_idx,new_idx)
            if pt_dist_to_line < min_pt_dist_to_line:
                min_pt_dist_to_line = pt_dist_to_line
                saved_idx = new_idx.copy()
    if cur_idx[1] - 1 >= region_rect_upleft_idx[1] and cur_idx[0]+1 <= region_rect_lowright_idx[0]:
        new_idx[1] = cur_idx[1] - 1     #y down, x up
        new_idx[0] = cur_idx[0] + 1
        if dist_btwn_idxs(new_idx,end_idx) < cur_dist_to_end:
            pt_dist_to_line = get_shortest_dist_pt_to_line(start_idx,end_idx,new_idx)
            if pt_dist_to_line < min_pt_dist_to_line:
                min_pt_dist_to_line = pt_dist_to_line
                saved_idx = new_idx.copy()
    if cur_idx[1] + 1 <= region_rect_lowright_idx[1] and cur_idx[0]-1 >= region_rect_upleft_idx[0]:
        new_idx[1] = cur_idx[1] + 1     #y up, x down
        new_idx[0] = cur_idx[0] - 1
        if dist_btwn_idxs(new_idx,end_idx) < cur_dist_to_end:
            pt_dist_to_line = get_shortest_dist_pt_to_line(start_idx,end_idx,new_idx)
            if pt_dist_to_line < min_pt_dist_to_line:
                min_pt_dist_to_line = pt_dist_to_line
                saved_idx = new_idx.copy()
                
    cur_idx = saved_idx.copy()
    idx_path.append(cur_idx)
  # print(idx_path)
  return idx_path

#tell if two given pts are along a diagonal
def points_are_a_diagonal(p1,p2):
   if p2[0]-p1[0]==0:
       return False
   if p2[1]-p1[1]==0:
       return False
   return True