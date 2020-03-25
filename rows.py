import csv


def get_rows(in_file = 'china_aid.csv'):
    """Open csv files and return the data"""
    with open(in_file) as csvfile:
        rows = csv.DictReader(csvfile)
        return list(rows)

def get_column_names(in_file = 'china_aid.csv'):
    """
        Gets the column names as a single string to form the header
        
        :params: none
        :returns: column names as a string
    
    """
    with open(in_file, 'r') as f:
        return f.readline().strip().split(',')

def default_update_function(row, extras):
    """
    Dummy default function to clean up the params for change function
    It updates the row's extras -- default params
    
    """
    row.update(extras)

def default_condition_function(row):
    """
    Dummy default function to clean up the params for change function
    Defaults to false
    """
    return False

def change_function(rows, extras={}, 
                    condition_function = default_condition_function, 
                    update_function = default_update_function):
    """
        Catchall function that effects change in the rows    
    """
    try:
        output = []
        for row  in rows:
            if condition_function(row) and  (not row['id'] in ('1','2','3','4','5','6')):
                update_function(row, extras)
            output.append(row)
        print("Color output length", len(output))
        return output
    except ValueError:
        print("This row does not exist")   

def scale_xyz(rows, parent, scale_x='0.4', scale_y='0.4', scale_z='0.4'):
    """
        Sets the values for scale_x, scale_y and scale_z and parent_id based on input 
        and returns a CSV input with updated data

        :params: Data dict, parent, scale_x, scale_y, scale)z
        :returns: updated rows for CSV file
    
    """
    extras = dict(scale_x=scale_x, scale_y=scale_y, scale_z=scale_z)
    return change_function(rows, extras, lambda row:  row['parent_id'] == parent)


def change_color(rows, parent, color_r='0', color_g='255', color_b='0'):
    """
        Sets the values for scale_x, scale_y and scale_z and parent_id based on input 
        and returns a CSV input with updated data

        :params: Data dict, parent. Takes all the rest as defaults unless given as input.
        :returns: updated row for CSV file
    
    """
    extras = dict(color_r=color_r, color_g=color_g, color_b=color_b) 
    return change_function(rows, extras, lambda row: row['parent_id'] == parent)


# Change all objects with geometry = 3 to have topo = 4, translate_x = -90,  translate_y = 90, and color_r = 0, color_g=152, color_b=255. (not including rows with id 1-6)
def topo_color(rows, geometry, topo = '4', translate_x='-90', translate_y='90', color_r='0', color_g='152', color_b='255'):
    """
        Sets the values topo, translate_x, translate_y, color_r, color_g, color_b with defaults or changed based on input 
        and returns a CSV input with updated data

        :params: Data dict, geometry. Takes all the rest as defaults unless given as input.
        :returns: updated row for CSV file
    
    """
    extras = dict(topo=topo, translate_x=translate_x, translate_y=translate_y, color_r=color_r, color_g=color_g, color_b=color_b)
    return change_function(rows, extras, lambda row: row['geometry'] == geometry)


def make_interpolator(left_min, left_max, right_min, right_max): 
    # Figure out how 'wide' each range is  
    leftSpan = left_max - left_min  
    rightSpan = right_max - right_min  
    # Compute the scale factor between left and right values 
    scaleFactor = float(rightSpan) / float(leftSpan) 

    # create interpolation function using pre-calculated scaleFactor
    def interp_fn(value):
        return right_min + (float(value)-left_min)*scaleFactor

    return interp_fn


#Change all objects with geometry = 3, using the make interpolator function (in j.notebook) to scale within range .2 to 3. (not including rows with id 1-6)
def change_geometry(rows, geometry, left_min = 1e-06, left_max = 100, right_min = .2, right_max = 3):
    condition_function = lambda row: row['geometry'] == geometry 
    scalar = make_interpolator(left_min, left_max, right_min, right_max) 

    def update_function(row, extras, scalar = scalar):
        row['scale_x'] = scalar(row['scale_x'])
        row['scale_y'] = scalar(row['scale_y'])
        row['scale_z'] = scalar(row['scale_z'])

    return change_function(rows, {}, condition_function=condition_function, update_function=update_function)

# Change all objects with branch_level = 3 to color_r = 0, color_g=0, color_b=255. (not including rows with id 1-6)
def branch_color(rows, branch_level, color_r=0, color_g=0, color_b=255):
    extras = dict(color_r=color_r, color_g=color_g, color_b=color_b)
    return change_function(rows, extras, lambda row: row['branch_level'] == branch_level)

# Change all objects with branch_level = 2 AND geometry = 19, to translate_x = 0, color_r = 197, color_g=82, color_b=0 (not including rows with id 1-6)
def branch_geometry(rows, branch_level, geometry, translate_x ='0', color_r='197', color_g='82', color_b='0'):
    extras = dict(translate_x=translate_x, color_r=color_r, color_g=color_g, color_b=color_b)
    return change_function(rows, extras, lambda row: row['branch_level'] == branch_level and row['geometry'] == geometry)


# Change all objects with branch_level = 2 AND geometry =7, to translate_x = -30, and geometry = 11, and color_r = 0, color_g=255, color_b=255. (not including rows with id 1-6)
def change_branch_geometry(rows, branch_level, geometry, geom='11', translate_x='-30', color_r='0', color_g='255', color_b='255'):
    extras = dict(geometry=geom, translate_x=translate_x, color_r=color_r, color_g=color_g, color_b=color_b)
    return change_function(rows, extras, lambda row: row['branch_level'] == branch_level and row['geometry'] == geometry)


# Change all objects with branch_level = 1, to color_r = 185, color_g=153, color_b=102, and change topo = 11. (not including rows with id 1-6)
def branch_topo(rows, branch_level, topo='11', color_r='185', color_g='153', color_b='102'):
    extras = dict(topo=topo, color_r=color_r, color_g=color_g, color_b=color_b)
    return change_function(rows, extras, lambda row: row['branch_level'] == branch_level)


def write_to_file(output_rows, out_file = 'china_antz.csv'):
    """
        Prints the updated CSV file
    
    """
    with open(out_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames = get_column_names())
        writer.writeheader()
        for line in output_rows:
            writer.writerow(line)


def main():
    """
        Calls all the update functions and updates the output_list variable accordingly to get it to the final form
    """
    output_list = scale_xyz(get_rows(), '0', scale_x='0.3', scale_y='0.2', scale_z='0.4')
    output_list = change_color(output_list, '0')
    output_list = topo_color(output_list, '3')
    output_list = change_geometry(output_list, '3')
    output_list = branch_geometry(output_list,'2','19')
    output_list = branch_topo(output_list, '1')
    output_list = change_branch_geometry(output_list, '2', '7')
    write_to_file(branch_color(output_list, '3'))

if __name__ == "__main__":
    main()