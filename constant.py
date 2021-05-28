import math


CONTROLER_KWARGS = {
    "LP": 30,
    "LI": 0.06,
    "LD": 20,
    "L_init_duty": 40,
    "RP": 40,
    "RI": 0.01,
    "RD": 23,
    "R_init_duty": 40,
    "target_duty": 40,
    "lossBoundary": 2,
    "lossScale": 7
}

RETICLE_SHAPE = {
    "verticalHeight": 180, # max 480
    "verticalWidth": 100,   # max 640
    "horizontalHeight": 48,
    "horizontalWidth": 480,
    "offset": 0
}

# for tracking mode
LOSS_KWARGS = {
    "verticalLossBound": 0.8,
    'lossScale': 0.00000001
}

# for houghTracking mode
HOUGH_KWARGS = {
    "rho": 1,
    "theta": math.pi/180,
    "threshold": 400,
    "minLineLength": 200,
    "maxLineGap": 400,
    "lineBoundary": 520,
    "lossBoundary": 0.5,
    "slopScale": 0.1,
    "offsetScale": 0.001
}

# for edgeTracking mode
EDGE_KWARGS = {
    "firstLineY": 350,
    "secondLineY": 100,
    "slopScale": 10,
    "slopBound": 10
}