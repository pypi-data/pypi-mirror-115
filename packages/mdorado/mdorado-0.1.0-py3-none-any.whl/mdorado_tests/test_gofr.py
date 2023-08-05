#!/usr/bin/env python3.8

import unittest
import os
import numpy as np
import MDAnalysis
from mdorado.gofr import Gofr

class TestProgram(unittest.TestCase):
    def test_gofr(self):
        trajectory="water_testsim/trajectory.xtc"
        topology="water_testsim/topology.tpr"
        u = MDAnalysis.Universe(topology, trajectory)
        hgrp = u.select_atoms("name hw")
        ogrp = u.select_atoms("name ow")
        watergrp = u.select_atoms("resname SOL")
        sitesite = Gofr(universe=u, agrp=hgrp, bgrp=ogrp, rmin=1.0, rmax=6, bins=100, mode="site-site", outfilename="test.dat")
        cmscms = Gofr(universe=u, agrp=watergrp, bgrp=watergrp, rmin=1.0, rmax=6, bins=100, mode="cms-cms", outfilename="test.dat")
        sitecms = Gofr(universe=u, agrp=hgrp, bgrp=watergrp, rmin=1.0, rmax=6, bins=100, mode="site-cms", outfilename="test.dat")
        
        gss = np.loadtxt("data/gofr_ss.dat", unpack=True)
        gcc = np.loadtxt("data/gofr_cc.dat", unpack=True)
        gsc = np.loadtxt("data/gofr_sc.dat", unpack=True)

        resss = np.array([sitesite.rdat, sitesite.hist, sitesite.annn, sitesite.bnnn])
        rescc = np.array([cmscms.rdat, cmscms.hist, cmscms.annn, cmscms.bnnn])
        ressc = np.array([sitecms.rdat, sitecms.hist, sitecms.annn, sitecms.bnnn])
        self.assertIsNone(np.testing.assert_array_almost_equal(resss, gss))
        self.assertIsNone(np.testing.assert_array_almost_equal(rescc, gcc))
        self.assertIsNone(np.testing.assert_array_almost_equal(ressc, gsc))
        os.remove("test.dat")

if __name__ == '__main__':
        unittest.main()

