def is_inside(inner_box, outer_box):
    ix, iy, iw, ih = inner_box
    ox, oy, ow, oh = outer_box
    return ix >= ox and iy >= oy and ix + iw <= ox + ow and iy + ih <= oy + oh

def match_acne_to_zone(zona_faces, jerawat):
    matched_zones = { 'dahi': [], 'pipi': [], 'hidung': [], 'dagu': [] }
    input_user_flags = { 'dahi': 0, 'pipi': 0, 'hidung': 0, 'dagu': 0 }

    for jer in jerawat:
        jer_box = jer['bbox']
        for zona in zona_faces:
            if is_inside(jer_box, zona['bbox']):
                matched_zones[zona['label']].append(jer)
                input_user_flags[zona['label']] = 1

    return matched_zones, input_user_flags
