#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math


def calculate_distance(df):
    """
    from latitude and longitude, calculates Euclidean
    distance between pickup and dropoff
    """
    earth_radius = 6373.0  # Earth radius (Km)

    dlon = np.radians((df["dropoff_longitude"]).values -
                      (df["pickup_longitude"]).values)
    dlat = np.radians((df["dropoff_latitude"]).values -
                      (df["pickup_latitude"]).values)

    a = np.power(np.sin(
        dlat / 2), 2) + np.cos(np.radians(
            (df["dropoff_latitude"]).values
        )) * np.cos(np.radians(
            (df["pickup_latitude"]).values)) * np.power(np.sin(dlon / 2), 2)
    return earth_radius * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))


if __name__ == '__main__':
    df = pd.read_csv("../data/train.csv")

    df['distance'] = calculate_distance(df)

    df.to_csv("../data/train.csv", index=False)
