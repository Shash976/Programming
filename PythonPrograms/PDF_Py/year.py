#!/usr/bin/env python3

import json
import cars

data = cars.process_data('cars_sales.json')

years = {}
for item in data:
  car_year = cars.format_car(item['car'])['car_year']
  if car_year not in years:
    years[car_year] = 0
  years[car_year] += 1

year = []
for k, v in years:
  year.append(v)

print (years)
print (year)
