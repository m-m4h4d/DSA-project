# get user input
from csvData import string_stream


bad_input = False
filenums = input("Enter the numbers for which files you would like to load, separated by COMMAS: ")
# filenums = filenums.replace(" ",",").replace(",,",",").replace(",,",",").replace(",,",",")

for i in range(9):
    try:
        if not filenums[len(filenums)-1].isdigit():
            filenums = filenums[0:len(filenums)-1]
    except:
        trash = 0

filenums = filenums.replace("  "," ").replace(" ",",").replace(",,",",")
filenums += ","
for i in range(len(filenums)):
    if not (filenums[i].isdigit()) and not filenums[i]==",":
        print('Bad Input')
        bad_input = True
        break
print(str(filenums[0:len(filenums)-1]))

# parse input for nums
if bad_input != True:
    filenums_array = []
    stream = string_stream(filenums, ",")
    for s in stream:
        num = int(s)
        if num not in filenums_array:
            filenums_array.append(num)  # add nums to array
        if num < 1 or num > 12:
            print('Bad Input')
            bad_input = True
            break

bad_input = False
if bad_input != True:
    for num in filenums_array:    # download corresponding files to the nums
        print('Downloading file ' + available_world_data_files[num])
        file_id = corresponding_keys[num]
        destination = '/content/' + available_world_data_files[num]
        download_file_from_google_drive(file_id, destination)

if not bad_input:
    print("\n")
    print('SUCCESS')