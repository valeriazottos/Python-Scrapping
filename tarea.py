#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 16:53:53 2022

@author: vz
"""


#### Import package

from wwo_hist import retrieve_hist_data

#### Set working directory to store output csv file(s)

import os
os.chdir("/Volumes/GoogleDrive-112553083728584115268/My Drive/Herramientas computacionales/python/output/weather")



#### Example code

frequency=24
start_date = '01-JAN-2015'
end_date = '31-DEC-2015'
api_key = 'b26f3391ff5b421dabc131348221107'
location_list = ['20637', '20653', '20688', '20740', '20794', '20871', '21040', '21158', '21208', '21241', '21411', '21502', '21536', '21625', '21638', '21639', '21643', '21650', '21704', '21742', '21801', '21811', '21853', '21912']

hist_weather_data = retrieve_hist_data(api_key,
                                location_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = True)