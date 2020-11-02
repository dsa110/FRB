""" Sets parameters for FRB associations """
import os
from astropy import units

from IPython import embed

gdb_path = os.getenv('FRB_GDB')

base_config = dict(
    max_radius=10.,
    cut_size=None,
    deblend=False,
    cand_bright=None,
    cand_separation=None,
    skip_bayesian=False,
)

# ##############################
# FRB 180916
""" 
Notes:  
   Still work in progress!
"""
updates = dict(
    name='FRB180916',
    image_file=os.path.join(gdb_path, 'CHIME', 'Marcote2020', 'FRB180916_GMOS_r.fits'),
    cut_size = 30.,
    filter = 'r',
    ZP = 34.5,
    deblend=True,
    npixels=9,
    cand_bright=18.,
    cand_separation=10*units.arcsec,
    plate_scale = 0.1616 * units.arcsec,
)
frb180916 = {**base_config, **updates}  # Use | in 3.9


# ##############################
# FRB 180924
updates = dict(
    name='FRB180924',
    image_file=os.path.join(gdb_path, 'CRAFT', 'Bannister2019', 'FRB180924_VLT_FORS2_g.fits'),
    cut_size = 30.,
    filter = 'g',
    ZP = 34.5,
    deblend=True,
    npixels=9,
    cand_bright=18.,
    cand_separation=10*units.arcsec,
    plate_scale = 0.25226 * units.arcsec,
)
frb180924 = {**base_config, **updates}  # Use | in 3.9

# ##############################
# FRB 181112
updates = dict(
    name='FRB181112',
    image_file=os.path.join(gdb_path, 'CRAFT', 'Prochaska2019', 'FRB181112_VLT_FORS2_I.fits'),
    cut_size = 30.,
    filter = 'I',
    ZP = 32.3,
    deblend=True,
    npixels=9,
    cand_bright=18.,
    cand_separation=10*units.arcsec,
    plate_scale = 0.25226 * units.arcsec,
)
frb181112 = {**base_config, **updates}  # Use | in 3.9

# ##############################
# FRB 190102
updates = dict(
    name='FRB190102',
    image_file=os.path.join(gdb_path, 'CRAFT', 'Macquart2020', 'FRB190102_FORS2_I.fits'),
    cut_size = 30.,
    filter = 'I',
    ZP = 26.9,
    deblend=True,
    npixels=9,
    cand_bright=18.,
    cand_separation=10*units.arcsec,
    plate_scale = 0.252 * units.arcsec,
)
frb190102 = {**base_config, **updates}  # Use | in 3.9

# ##############################
# FRB 190523
updates = dict(
    name='FRB190523',
    image_file = os.path.join(gdb_path, 'DSA', 'Ravi2019', 'FRB190523_Keck_LRIS_R.fits'),
    cut_size = 30.,
    filter = 'R',
    ZP = 33.,
    deblend=True,
    plate_scale = 0.28 * units.arcsec,
    cand_separation=10*units.arcsec,
    npixels=9,
)
frb190523 = {**base_config, **updates}  # Use | in 3.9

# ##############################
# FRB 190614
updates = dict(
    name='FRB190614',
    image_file = os.path.join(gdb_path, 'Realfast', 'Law2020', 'FRB190614_LRISr_I_img.fits'),
    cut_size = 30.,
    filter='I',
    ZP=34.,
    deblend=True,
    plate_scale = 0.135 * units.arcsec,
    cand_separation=10*units.arcsec,
    npixels=9,
)
frb190614 = {**base_config, **updates}

# ##############################
# FRB 190711
"""
Notes:
   Figure out if the 2nd source is a star (HST data)
"""
updates = dict(
    name='FRB190711',
    image_file=os.path.join(gdb_path, 'CRAFT', 'Macquart2020', 'FRB190711_GMOS-S_i_img.fits'),
    cut_size = 30.,
    filter = 'i',
    ZP = 32.7,
    deblend=True,
    npixels=9,
    cand_bright=18.,
    cand_separation=10*units.arcsec,
    plate_scale = 0.160*units.arcsec,
)
frb190711 = {**base_config, **updates}  # Use | in 3.9

# ##############################
# FRB 190714
"""
Notes:
"""
updates = dict(
    name='FRB190714',
    image_file=os.path.join(gdb_path, 'CRAFT', 'Heintz2020', 'FRB190714_FORS2_I_img.fits'),
    cut_size = 30.,
    filter = 'I',
    ZP = 27.39,
    deblend=True,
    npixels=9,
    cand_bright=18.,
    cand_separation=10*units.arcsec,
    plate_scale=0.252*units.arcsec,
)
frb190714 = {**base_config, **updates}  # Use | in 3.9

# ##############################
# FRB 191001
"""
Notes:
"""
updates = dict(
    name='FRB191001',
    image_file=os.path.join(gdb_path, 'CRAFT', 'Heintz2020', 'FRB191001_FORS2_I_img.fits'),
    cut_size = 30.,
    filter = 'I',
    ZP = 27.5,
    deblend=True,
    npixels=9,
    cand_bright=17.,
    cand_separation=10*units.arcsec,
    plate_scale=0.252*units.arcsec,
)
frb191001 = {**base_config, **updates}  # Use | in 3.9

# ##############################
# FRB 200430
"""
Notes:
"""
updates = dict(
    name='FRB200430',
    image_file=os.path.join(gdb_path, 'CRAFT', 'Heintz2020', 'FRB200430_LRISr_I_img.fits'),
    cut_size = 30.,
    filter = 'I',
    ZP = 34.2,  # Tied to Pan-Starrs i-band
    deblend=True,
    npixels=9,
    cand_bright=17.,
    cand_separation=10*units.arcsec,
    plate_scale=0.134*units.arcsec,
)
frb200430 = {**base_config, **updates}  # Use | in 3.9

