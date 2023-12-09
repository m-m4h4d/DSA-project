#@title <b>4) Dijikstra's Algorithm Optimization Functions</b>
##############################################################################################
# Dijikstra Optimization Functions
##############################################################################################

# DIJIKSTRA ALGORITHM
# THIS FUNCTION IS COPIED FROM: https://levelup.gitconnected.com/dijkstras-shortest-path-algorithm-in-a-grid-eb505eb3a290
# CREDITS TO Roman Kositski
from matplotlib import pyplot as plt
import numpy as np


def dijikstra(map, startidx_x, startidx_y, endidx_x, endidx_y):
  # startidx_x, startidx_y = 3,0
  # endidx_x,endidx_y = 40,65
  min_val, max_val_row, max_val_col = 0, map.shape[0], map[0].shape[0]
  min_possible_Vg = np.amin(map)
  max_possible_Vg = np.amax(map)

  # # refactoring map scale
  # map += 3
  # map *= 0.8
  # maxx = np.amax(map)
  # map = -map + maxx
  # print(map)

  #min_val, max_val = 0, 10
  #map = np.random.randint(1, 20, size=(max_val, max_val))

  map[startidx_x,startidx_y]=0
  map[max_val_row-1,max_val_col-1]=0

  fig, ax = plt.subplots(figsize=(8,8))
  ax.matshow(map, cmap=plt.cm.Blues, vmin=min_possible_Vg, vmax=max_possible_Vg)
  for i in range(max_val_col):
      for j in range(max_val_row):
        c = map[j,i]
        # ax.text(i, j, str(c), va='center', ha='center')

  #Initialize auxiliary arrays
  distmap=np.ones((max_val_row,max_val_col),dtype=int)*np.Infinity
  distmap[startidx_x,startidx_y]=0
  originmap=np.ones((max_val_row,max_val_col),dtype=int)*np.nan
  visited=np.zeros((max_val_row,max_val_col),dtype=bool)
  finished = False
  count=0
  x,y=int(startidx_x),int(startidx_y)
  # x,y=int(3),int(3)
  # distmap[3,3]=0
  # visited[0:3,0:3]=True
  # for i in originmap:
  #   i+=3

  #Loop Dijkstra until reaching the target cell
  while not finished:
    # move to x+1,y
    if x < max_val_row-1:
      if distmap[x+1,y]>map[x+1,y]+distmap[x,y] and not visited[x+1,y]:
        distmap[x+1,y]=map[x+1,y]+distmap[x,y]
        originmap[x+1,y]=np.ravel_multi_index([x,y], (max_val_row,max_val_col))
    # move to x-1,y
    if x>0:
      if distmap[x-1,y]>map[x-1,y]+distmap[x,y] and not visited[x-1,y]:
        distmap[x-1,y]=map[x-1,y]+distmap[x,y]
        originmap[x-1,y]=np.ravel_multi_index([x,y], (max_val_row,max_val_col))
    # move to x,y+1
    if y < max_val_col-1:
      if distmap[x,y+1]>map[x,y+1]+distmap[x,y] and not visited[x,y+1]:
        distmap[x,y+1]=map[x,y+1]+distmap[x,y]
        originmap[x,y+1]=np.ravel_multi_index([x,y], (max_val_row,max_val_col))
    # move to x,y-1
    if y>0:
      if distmap[x,y-1]>map[x,y-1]+distmap[x,y] and not visited[x,y-1]:
        distmap[x,y-1]=map[x,y-1]+distmap[x,y]
        originmap[x,y-1]=np.ravel_multi_index([x,y], (max_val_row,max_val_col))


	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # MY ADDED SECTION FOR DIAGONAL MANUEVERS (to minimize distance calc error to < 8%)
    # move to x+1,y+1
    if y < max_val_col-1 and x < max_val_row-1:
      if distmap[x+1,y+1]>map[x+1,y+1]+distmap[x,y] and not visited[x+1,y+1]:
        distmap[x+1,y+1]= 1.414213562*(map[x+1,y+1])+distmap[x,y]
        originmap[x+1,y+1]=np.ravel_multi_index([x,y], (max_val_row,max_val_col))
    # move to x-1,y+1
    if y < max_val_col-1 and x > 0:
      if distmap[x-1,y+1]>map[x-1,y+1]+distmap[x,y] and not visited[x-1,y+1]:
        distmap[x-1,y+1]= 1.414213562*(map[x-1,y+1])+distmap[x,y]
        originmap[x-1,y+1]=np.ravel_multi_index([x,y], (max_val_row,max_val_col))
    # move to x-1,y-1
    if y > 0 and x > 0:
      if distmap[x-1,y-1]>map[x-1,y-1]+distmap[x,y] and not visited[x-1,y-1]:
        distmap[x-1,y-1]= 1.414213562*(map[x-1,y-1])+distmap[x,y]
        originmap[x-1,y-1]=np.ravel_multi_index([x,y], (max_val_row,max_val_col))
    # move to x+1,y-1
    if y > 0 and x < max_val_row-1:
      if distmap[x+1,y-1]>map[x+1,y-1]+distmap[x,y] and not visited[x+1,y-1]:
        distmap[x+1,y-1]= 1.414213562*(map[x+1,y-1])+distmap[x,y]
        originmap[x+1,y-1]=np.ravel_multi_index([x,y], (max_val_row,max_val_col))
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



    visited[x,y]=True
    dismaptemp=distmap
    dismaptemp[np.where(visited)]=np.Infinity
    # now we find the shortest path so far
    minpost=np.unravel_index(np.argmin(dismaptemp),np.shape(dismaptemp))
    x,y=minpost[0],minpost[1]
    if x==endidx_x and y==endidx_y:
      finished=True
    count=count+1

  #Start backtracking to plot the path  
  mattemp=map.astype(float)
  x,y=endidx_x,endidx_y
  path=[]
  mattemp[int(x),int(y)]=np.nan
  
  
  while x>startidx_x or y>startidx_y:
    path.append([int(x),int(y)])
    xxyy=np.unravel_index(int(originmap[int(x),int(y)]), (max_val_row,max_val_col))
    x,y=xxyy[0],xxyy[1]
    mattemp[int(x),int(y)]=np.nan
  path.append([int(x),int(y)])

  #Output and visualization of the path
  current_cmap = plt.cm.Blues
  current_cmap.set_bad(color='red')
  fig, ax = plt.subplots(figsize=(8,8))
  ax.matshow(mattemp,cmap=plt.cm.Blues, vmin=min_possible_Vg, vmax=max_possible_Vg)
  for i in range(max_val_col):
      for j in range(max_val_row):
        c = map[j,i]
        # ax.text(i, j, str(c), va='center', ha='center')

  # print('The path length is: '+np.str(distmap[max_val_row-1,max_val_col-1]))
  path = path[::-1]     # reverse path
  # print('The dump/mean path should have been: '+np.str(maxnum*max_val))

  ## save path to csv
  # for coor in pa:
  #   map[coor[0]][coor[1]] = -4
  # np.savetxt('path.csv', map, delimiter=',')
  return path.copy()

# function to switch path values to original route (x, y) indexing
def switch_path_idxs(path):
  for coor in path:
    temp = coor[0]
    coor[0] = coor[1]# + index_x_diff
    coor[1] = temp# + index_y_diff
# func to show the start/end idxs before optimizing
def show_startend_pts(start_row, start_col, end_row, end_col, num_rows, num_cols, weighted_world_data_map):
  print('start_row: ' + str(start_row))
  print('start_col: ' + str(start_col))
  print('end_row: ' + str(end_row))
  print('end_col: ' + str(end_col))
  print('num_rows: ' + str(num_rows))
  print('num_cols: ' + str(num_cols))
  print('map size (rows,cols): ' + str(weighted_world_data_map.shape[0]) + ', ' + str(weighted_world_data_map.shape[1]))

# BIG OPTIMIZATION FUNCTION
# (will rotate map to fit Dijikstra's Alg, then find optimal path, and, when done, unrotate path indexes)
def optimize_path(start_idx,end_idx,region_rect_lowright_idx,region_rect_upleft_idx,weighted_world_data_map,rotation_message):
  path = []

  # ROTATION OPTION 1: JUST KEEP MAP THE SAME
  if start_idx[0]==0:
    # set the start/end pts
    start_row = start_idx[1]
    start_col = 0   # <--DO NOT CHANGE THIS
    end_row = end_idx[1]
    end_col = end_idx[0]

    # set the boundaries
    num_rows = region_rect_lowright_idx[1]+1
    num_cols = region_rect_lowright_idx[0]+1

    # get path
    path = dijikstra(weighted_world_data_map, start_row,start_col,end_row,end_col)		# (map, startidx_row, startidx_col, endidx_row, endidx_col)
    switch_path_idxs(path)      # switch to (x, y) indexing
    
  # ROTATION OPTION 2: ROTATE MAP 180 DEG
  elif end_idx[0]==0:
    weighted_world_data_map = np.flip(weighted_world_data_map)    # rotate map 180 deg
    # set the boundaries
    num_rows = region_rect_lowright_idx[1]+1
    num_cols = region_rect_lowright_idx[0]+1

    # set the start/end pts
    start_row = num_rows - start_idx[1] -1
    start_col = 0   # <--DO NOT CHANGE THIS
    end_row = num_rows - end_idx[1] - 1
    end_col = num_cols - end_idx[0] - 1
    rotation_message = ('SHOWN PLOTS ARE ROTATED 180 DEG')

    path = dijikstra(weighted_world_data_map, start_row,start_col,end_row,end_col)		# (map, startidx_row, startidx_col, endidx_row, endidx_col)
    switch_path_idxs(path)    # switch to (x, y) indexing
    for item in path:       # rotate path indexes 180 deg
      item[0] = num_cols - item[0] - 1
      item[1] = num_rows - item[1] - 1

  # ROTATION OPTION 3: ROTATE MAP 90 DEG COUNTERCLOCKWISE
  elif start_idx[1]==0:
    weighted_world_data_map = np.rot90(weighted_world_data_map)   # rotate map 90deg counterclockwise
    rotation_message = ('SHOWN PLOTS ARE ROTATED 90 DEG COUNTERCLOCKWISE')
    
    # set the boundaries
    num_rows = region_rect_lowright_idx[0]+1
    num_cols = region_rect_lowright_idx[1]+1
    
    # set the start/end pts
    start_col = 0             # <--DO NOT CHANGE THIS
    start_row = num_rows - start_idx[0] -1
    end_row = num_rows - end_idx[0] -1
    end_col = end_idx[1]

    show_startend_pts(start_row, start_col, end_row, end_col, num_rows, num_cols, weighted_world_data_map)

    path = dijikstra(weighted_world_data_map, start_row,start_col,end_row,end_col)		# (map, startidx_row, startidx_col, endidx_row, endidx_col)
    #switch_path_idxs(path)    # switch to (x, y) indexing        # NOT NEEDED
    #for item in path:       # rotate path indexes 90 deg
    #  item[0] = num_rows - item[0] - 1

  # ROTATION OPTION 4: ROTATE MAP 90 DEG CLOCKWISE
  elif end_idx[1]==0:
    weighted_world_data_map = np.rot90(weighted_world_data_map,-1)    #rotate map 90 deg clockwise
    rotation_message = ('SHOWN PLOTS ARE ROTATED 90 DEG CLOCKWISE')
    
    # set the boundaries
    num_rows = region_rect_lowright_idx[0]+1
    num_cols = region_rect_lowright_idx[1]+1
    
    # set the start/end pts
    start_col = 0
    start_row = start_idx[0]
    end_row = end_idx[0]
    end_col = start_idx[1]-end_idx[1]
    
    # get path
    path = dijikstra(weighted_world_data_map, start_row,start_col,end_row,end_col)		# (map, startidx_row, startidx_col, endidx_row, endidx_col)
    
    # switch back to original indexing
    for item in path:
      item[0] = num_rows - item[0] - 1
    path = path[::-1]     # reverse path finally

  return path, rotation_message

# finally show/save the path
def show_optipath_coors(using_coordinates_table,path,coordinates_table,index_x_diff,index_y_diff,display_path):
  path_as_str = ""
  if using_coordinates_table:

    if display_path==True: print('\nPath lat/lon coors:')
    for loc in path:
      if display_path==True: print(coordinates_table[loc[1],loc[0]])
      path_as_str += str(coordinates_table[loc[1],loc[0]]) + '\n'
  elif not using_coordinates_table:
    if display_path==True: print('\nPath csv-indexed coors (x,y):')
    for loc in path:
      if display_path==True: print([loc[0]+index_x_diff,loc[1]+index_y_diff])
      path_as_str += str([loc[1],loc[0]]) + '\n'

  text_file = open("optimized_path.txt", "w")
  n = text_file.write(path_as_str)
  text_file.close()