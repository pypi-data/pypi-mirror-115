# pylint: disable=invalid-name
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-locals
# pylint: disable=too-many-arguments

"""
Class for doing inverse adding-doubling calculations for a sample.

    import iadpython.iad as iad

    n=4
    sample = ad.Sample(a=0.9, b=10, g=0.9, n=1.5, quad_pts=4)
    r, t = sample.rt()
    print(r)
    print(t)
"""

import copy
import numpy as np
import iadpython.ad


class Sphere():
    """Container class for an integrating sphere."""

    def __init__(self, sample, num_spheres, r_sphere=None, t_sphere=None,
                 n=1, n_above=1, n_below=1, quad_pts=4):
        """Object initialization."""

        self.as_r = 1
        self.ad_r = 1
        self.ae_r = 1
        self.aw_r = 1
        self.rd_r = 1
        self.rw_r = 1
        self.rstd_r = 1
        self.f_r = 1


class Experiment():
    """Container class for details of an experiment."""

    def __init__(self, sample, num_spheres, r_sphere=None, t_sphere=None,
                 n=1, n_above=1, n_below=1, quad_pts=4):
        """Object initialization."""
        self.sample = sample

        self.num_spheres = num_spheres
        self.r_sphere = r_sphere
        self.t_sphere = t_sphere

        self.d_beam = d_beam
        self.lambda0 = lambda0

        self.flip_sample = False
        self.fraction_of_rc_in_mr = 1
        self.fraction_of_tc_in_mt = 1

        self.m_r, m_t, m_u = 1

        self.as_r, ad_r, ae_r, aw_r, rd_r, rw_r, rstd_r, f_r = 1
        self.as_t, ad_t, ae_t, aw_t, rd_t, rw_t, rstd_t, f_t = 1
        self.ur1_lost, uru_lost, ut1_lost, utu_lost = 1
        self.d_sphere_r, d_sphere_t = 1


Class Analysis():
    """Container class for how analysis is done."""

    def __init__(self, a=0, b=1, g=0, n=1, n_above=1, n_below=1, quad_pts=4):
        """Object initialization."""
        self.a = 1  # the calculated albedo
        self.b = 1  # the calculated optical depth
        self.g = 1  # the calculated anisotropy

        self.found = 1
        self.search = 1
        self.metric = 1
        self.tolerance = 1
        self.MC_tolerance = 1
        self.final_distance = 1
        self.iterations = 1
        self.error = 1

        #  struct AD_slab_type slab = 1
        #  struct AD_method_type method = 1

        self.default_a = 1
        self.default_b = 1
        self.default_g = 1
        self.default_ba = 1
        self.default_bs = 1
        self.default_mua = 1
        self.default_mus = 1
