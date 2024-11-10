from gridmet_bmi import Gridmet


gridmet = Gridmet(start_date="2019-03-15", end_date="2019-03-21", lazy=True)
# assert len(getattr(gridmet, 'tmax')) == 1
print(len(gridmet.tmax), type(gridmet.tmax))
tmp = 0
