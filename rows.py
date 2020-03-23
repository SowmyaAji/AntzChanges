import csv



def get_rows():
    """Open csv files and return the data"""
    with open('chin.csv') as csvfile:
        rows = csv.DictReader(csvfile)
        return list(rows)

def get_column_names():
    """
        Gets the column names as a single string to form the header
        
        :params: none
        :returns: column names as a string
    
    """
    with open("chin.csv", 'r') as f:
        columns = f.readline().strip()   
        return str(columns)
# get_column_names()

def scale_xyz(rows, selected_row, parent, scale_x='0.4', scale_y='0.4', scale_z='0.4'):
    """
        Sets the values for scale_x, scale_y and scale_z and parent_id based on input 
        and returns a CSV input with updated data

        :params: Data dict, id of selected row, parent, scale_x, scale_y, scale)z
        :returns: updated row for CSV file
    
    """
    print("I AM AT SCALE XYZ")
    print('IM ROW ONE', rows[0])
    try:
        output = list()
        for row in rows:
            if row['id'] == selected_row:
                if parent == '0':
                    row['id'] = selected_row
                    row['parent_id'] = parent
                    row['scale_x'] = scale_x
                    row['scale_y'] = scale_y
                    row['scale_z'] = scale_z 
                print("Scale values changed!")
                print("Changed row", row)                
            output.append(list(row.values()))
        print(len(output))
        return output
    except ValueError:
        print("This row does not exist")
# scale_xyz(get_rows(), '1', '0')  
# scale_xyz(get_rows(), '36', '0', scale_x='0.3', scale_y='0.2', scale_z='0.4')

def print_csv():
    output = scale_xyz(get_rows(), '36', '0', scale_x='0.3', scale_y='0.2', scale_z='0.4')
    columns = get_column_names()
    with open('chin.csv', 'w') as f:
            f.write(columns)
            f.write("\n".join([",".join(line) for line in output]))
print_csv()





def change_color(reader, selected_row, parent, color_r='0', color_g='255', color_b='0'):
    """
        Sets the values for scale_x, scale_y and scale_z and parent_id based on input 
        and returns a CSV input with updated data

        :params: Data dict, id of selected row, parent, scale_x, scale_y, scale)z
        :returns: updated row for CSV file
    
    """
    try:
        output = []
        for row  in reader:
            if row['id'] == selected_row:
                if parent == '0':
                    row['parent_id'] = parent
                    row['color_r'] = color_r
                    row['color_g'] = color_g
                    row['color_b'] = color_b
                    print("Color values changed!")
            output.append(row.values())
        print("Color output length", len(output))
        return output
    except ValueError:
        print("This row does not exist")

# def main():

# # scale_xyz(get_rows(), '1', '0')  
# scale_xyz(get_rows(), '36', '0', scale_x='0.3', scale_y='0.2', scale_z='0.4')
# change_color 

# def write_list(columns):
#     with open('column_list.csv', 'w') as f:
#         for column in columns:
#                 f.write(column + '\n')
# write_list(get_column_names())
