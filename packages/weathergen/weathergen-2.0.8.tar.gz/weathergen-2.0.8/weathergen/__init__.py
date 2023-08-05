import time as ttime
import numpy as np
import scipy as sp
import pandas as pd
import h5py, os
from . import utils

RGI = sp.interpolate.RegularGridInterpolator

base, this_filename = os.path.split(__file__)
#base = '/users/tom/desktop/repos/weathergen/weathergen'

def get_sites(base):
    sites = pd.read_csv(f'{base}/sites.csv', index_col=0).fillna('')
    sites = sites.loc[[os.path.exists(f'{base}/site_data/{tag}.h5') for tag in sites.index]]
    return sites

sites = get_sites(base)
        
def generate(**kwargs): return weather(**kwargs)

class weather():

    def __init__(self, site=None, time=None):

        if site is None: site = 'princeton' # if no site is supplied, use 'princeton'
        if time is None: time = ttime.time() # if no time is supplied, use current time

        if not site in sites.index:
            raise ValueError(f'The site \'{site}\' is not supported. Available sites are:\n{list(sites.index)}')
    
        self.site, self.time = site, np.atleast_1d(time)
        self.lat, self.lon, self.alt = sites.loc[sites.index == self.site, ['lat', 'lon', 'alt']].values[0]

        for k, v in self.generate().items(): setattr(self, k, v)

        # define some stuff
        if self.has_surface_data:

            self.precipitation[self.precipitation < 0.05] = 0 # we ignore precipitation less than 0.05 mm/hr

            self.surface_wind_bearing = np.degrees(np.arctan2(self.surface_wind_east, self.surface_wind_north) + np.pi)
            self.surface_wind_speed   = np.sqrt(np.square(self.surface_wind_east) + np.square(self.surface_wind_north))
            
            self.surface_rel_hum      = np.minimum(100, np.maximum(1, utils.AH_to_RH(self.surface_air_temp, self.surface_abs_hum)))
            self.surface_dew_point    = utils.get_dew_point(self.surface_air_temp, self.surface_rel_hum)
            self.total_cloud_cover    = np.minimum(1, np.maximum(0, self.total_cloud_cover))
            
        if self.has_profile_data:

            self.wind_bearing      = np.degrees(np.arctan2(self.wind_east, self.wind_north) + np.pi)
            self.wind_speed        = np.sqrt(np.square(self.wind_east) + np.square(self.wind_north))

            self.rel_hum           = np.minimum(100, np.maximum(1, utils.AH_to_RH(self.air_temp, self.abs_hum)))
            self.dew_point         = utils.get_dew_point(self.air_temp, self.rel_hum)
            self.cloud_cover       = np.minimum(1, np.maximum(0, self.cloud_cover))

            surface_abs_hum        = self.surface_abs_hum if self.has_surface_data else self.abs_hum[0]
            self.total_water_vapor = np.trapz(np.r_[surface_abs_hum[None], self.abs_hum], np.r_[self.alt, self.height], axis=0)
            self.total_ozone       = np.trapz(np.r_[self.ozone[0][None], self.ozone], np.r_[self.alt, self.height], axis=0)

    def generate(self):

        filename = f'{base}/site_data/{self.site}.h5'
        self._gen_data = {}
        with h5py.File(filename, 'r') as f:
            for key in list(f.keys()): 
                self._gen_data[key] = f[key][()] if not key == 'gen_labels' else f[key][()].astype(str)

        self.has_surface_data = self._gen_data['has_surface_data']
        self.has_profile_data = self._gen_data['has_profile_data']
        
        dt_gen = np.gradient(self.time).min()
        gen_time = np.arange(self.time.min(), self.time.max() + dt_gen, dt_gen)
            
        n_gen  = len(gen_time)
        f_gen  = np.fft.fftfreq(n_gen, dt_gen)

        self.year_day = list(map(utils.get_utc_year_day, gen_time))
        self.day_hour = list(map(utils.get_utc_day_hour, gen_time))

        GOOD    = ~np.isnan(self._gen_data['azdft_binned'])
        AZDFT   = np.c_[[sp.interpolate.interp1d(self._gen_data['azdft_freq'][g], azdft[g], fill_value=0, bounds_error=False, kind='cubic')(f_gen) 
                                                    for azdft, g in zip(self._gen_data['azdft_binned'], GOOD)]]

        GEN_DFT = AZDFT * np.sqrt(n_gen / dt_gen) * np.exp(1j*np.random.uniform(low=0,high=2*np.pi,size=AZDFT.shape))
        GEN_V   = np.real(np.fft.ifft(GEN_DFT))
        ZD      = np.matmul(self._gen_data['eigenmodes'][:,:GEN_V.shape[0]], GEN_V)

        yd_points = self._gen_data['year_day_edge_points']
        dh_points = self._gen_data['day_hour_edge_points']
        self.binned_mean_data = self._gen_data['binned_mean_grid']
        self.binned_norm_data = self._gen_data['binned_norm_grid']

        ZD *= RGI((yd_points, dh_points), self.binned_norm_data, method='linear')((self.year_day, self.day_hour)).T
        self.offset = RGI((yd_points, dh_points), self.binned_mean_data, method='linear')((self.year_day, self.day_hour)).T
        ZD += self.offset

        self.ZD = ZD.T
        self.QD = self._gen_data['QD']

        D = np.zeros(ZD.shape)
        for i in range(D.shape[0]):
            D[i] = sp.interpolate.interp1d(self._gen_data['z'], self.QD[i], kind='quadratic',  bounds_error=False, fill_value='extrapolate')(ZD[i]) 

        weather = {}
        for c, cg in zip(self._gen_data['gen_labels'], np.split(D, np.cumsum(self._gen_data['gen_widths'].astype(int))[:-1])):
            
            weather[c] = sp.interpolate.interp1d(gen_time, cg)(self.time)
            if weather[c].shape[0] == 1: weather[c] = weather[c][0]

        weather['height'] = self._gen_data['height']
        
        return weather

