import csv


def get_rows(in_file = 'chin.csv'):
    """Open csv files and return the data"""
    with open(in_file) as csvfile:
        rows = csv.DictReader(csvfile)
        return list(rows)

def get_column_names(in_file = 'chin.csv'):
    """
        Gets the column names as a single string to form the header
        
        :params: none
        :returns: column names as a string
    
    """
    with open(in_file, 'r') as f:
        return f.readline().strip().split(',')


def change_function(rows, selected_row, extras={}, condition_function = lambda row: False):
    """
        Over all function that effects change in the rows    
    """
    try:
        output = []
        for row  in rows:
            if row['id'] == selected_row and condition_function(row):
                row.update(extras)
            output.append(row)
        print("Color output length", len(output))
        return output
    except ValueError:
        print("This row does not exist")   

def scale_xyz(rows, selected_row, parent, scale_x='0.4', scale_y='0.4', scale_z='0.4'):
    """
        Sets the values for scale_x, scale_y and scale_z and parent_id based on input 
        and returns a CSV input with updated data

        :params: Data dict, id of selected row, parent, scale_x, scale_y, scale)z
        :returns: updated row for CSV file
    
    """
    extras = dict(scale_x=scale_x, scale_y=scale_y, scale_z=scale_z)
    return change_function(rows, selected_row, extras, lambda row: row['parent_id'] == parent)

def print_csv():
    output = scale_xyz(get_rows(), '36', '0', scale_x='0.3', scale_y='0.2', scale_z='0.4')
    with open('chin1.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames = get_column_names())
        writer.writeheader()
        for line in output:
            writer.writerow(line)


def change_color(rows, selected_row, parent, color_r='0', color_g='255', color_b='0'):
    """
        Sets the values for scale_x, scale_y and scale_z and parent_id based on input 
        and returns a CSV input with updated data

        :params: Data dict, id of selected row, parent. Takes all the rest as defaults unless given as input.
        :returns: updated row for CSV file
    
    """
    extras = dict(color_r=color_r, color_g=color_g, color_b=color_b) 
    return change_function(rows, selected_row, extras, lambda row: row['parent_id'] == parent)



def topo_color(rows, selected_row, geometry, topo = '4', translate_x='-90', translate_y='90', color_r='0', color_g='152', color_b='255'):
    """
        Sets the values topo, translate_x, translate_y, color_r, color_g, color_b with defaults or changed based on input 
        and returns a CSV input with updated data

        :params: Data dict, id of selected row, geometry. Takes all the rest as defaults unless given as input.
        :returns: updated row for CSV file
    
    """
    extras = dict(topo=top0, translate_x=translate_x, translate_y=translate_y, color_r=color_r, color_g=color_g, color_b=color_b)
    return change_function(rows, selected_row, extras, lambda row: row['geometry'] == geometry)


# Change all objects with geometry = 3 to have topo = 4, translate_x = -90,  translate_y = 90, and color_r = 0, color_g=152, color_b=255. (not including rows with id 1-6)




def write_to_file(output_rows, out_file = 'chin1.csv'):
    with open(out_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames = get_column_names())
        writer.writeheader()
        for line in output_rows:
            writer.writerow(line)


def main():
    output_list = scale_xyz(get_rows(), '36', '0', scale_x='0.3', scale_y='0.2', scale_z='0.4')
    output_list = change_color(output_list, '36', '0')
    output_list = topo_color(output_list, '36', '3')


if __name__ == "__main__":
    main()