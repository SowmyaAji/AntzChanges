"""
 code to check for dupes in the list if required
"""

def get_dupes_dict(conf_dict):
    dupes = []
    for key in conf_dict.keys():
        values = [list(v.keys())[0] for v in conf_dict[key]]
        if len(values) != len(set(values)):
            dupes.append(key)
    return dupes
