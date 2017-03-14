import luts
import geometric
import filters

def process(frame, state):
    lut_frame = luts.apply_luts(frame, state["luts"])
    filtered_frame = filters.apply_filters(lut_frame, state["filters"])
    affine_frame = geometric.apply_geometric(filtered_frame, state["geometric"])

    return affine_frame
