from pkg_resources import resource_filename

water_topology = resource_filename(__name__, 'water.tpr')
water_trajectory = resource_filename(__name__, 'water.xtc')
test_gofr_ss = resource_filename(__name__, 'gofr_ss.dat')
test_gofr_sc = resource_filename(__name__, 'gofr_sc.dat')
test_gofr_cc = resource_filename(__name__, 'gofr_cc.dat')
del resource_filename
