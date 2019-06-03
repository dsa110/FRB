""" Module for basic plots related to FRB host and foreground galaxies"""
import os
import numpy as np

from pkg_resources import resource_filename

from matplotlib import pyplot as plt

from astropy.io import fits
from astropy.table import Table

from frb.figures import utils


def sub_bpt(ax_BPT, galaxies, clrs, markers, show_kewley=True, SDSS_clr='BuGn'):
    """
    Generate a BPT diagram

    To use this code, you must download the SDSS_DR14_PM.fits file from
    https://drive.google.com/file/d/17r9kLh_mWGRX7Zx3DNmQEhoCGNUmzcCY/view?usp=sharing

    Args:
        ax_BPT: matplotlib.axis
        galaxies (list):
          List of FRBGalaxy objects
        clrs (list):
        markers (list):
        show_kewley (bool):
        SDSS_clr (str):
          Set the color map

    Returns:
        ax_BPT is modified in place

    """

    # Read in data
    sdss_file = os.path.join(resource_filename('frb', 'data'), 'Galaxies', 'SDSS', 'SDSS_DR14_PM.fits')
    hdulist = fits.open(sdss_file)
    bptdat = hdulist[1].data

    # Select only non zero entries and SNR over 5
    lines = np.array(bptdat.names)[[("flux" in name) & ("err" not in name) for name in bptdat.names]]
    line_err = np.array(bptdat.names)[["flux_err" in name for name in bptdat.names]]
    select = {}
    for line, err in zip(lines, line_err):
        select[line] = bptdat[line] / bptdat[err] >= 5

    # SDSS
    bpt1 = select['oiii_5007_flux'] & select['h_beta_flux'] & select['nii_6584_flux'] & select['h_alpha_flux']
    y = bptdat['oiii_5007_flux'][bpt1] / bptdat['h_beta_flux'][bpt1]
    x = bptdat['nii_6584_flux'][bpt1] / bptdat['h_alpha_flux'][bpt1]

    xbins = 100
    ybins = 100
    counts, xedges, yedges = np.histogram2d(np.log10(x), np.log10(y), bins=(xbins, ybins))
    cm = plt.get_cmap(SDSS_clr)
    mplt = ax_BPT.pcolormesh(xedges, yedges, np.log10(counts.transpose()), cmap=cm)

    for kk,galaxy in enumerate(galaxies):
        NII, NII_err = galaxy.calc_nebular_lum('[NII] 6584')
        Ha, Ha_err = galaxy.calc_nebular_lum('Halpha')
        Hb, Hb_err = galaxy.calc_nebular_lum('Hbeta')
        try:
            OIII, OIII_err = galaxy.calc_nebular_lum('[OIII] 5007')
        except:
            import pdb; pdb.set_trace()
        #
        x0 = (NII/Ha).decompose().value
        y0 = (OIII/Hb).decompose().value
        x0_err = x0 * np.sqrt((NII_err / NII).decompose().value**2 +
                (Ha_err/Ha).decompose().value**2)
        y0_err = y0 * np.sqrt((OIII_err / OIII).decompose().value**2 +
                              (Hb_err/Hb).decompose().value**2)
        # Require at least 20% error
        x0_err = max(x0_err, 0.2*x0)
        y0_err = max(y0_err, 0.2*y0)

        logx, xerr = utils.log_me(x0, x0_err)
        logy, yerr = utils.log_me(y0, y0_err)
        #
        ax_BPT.errorbar([logx], [logy], xerr=xerr, yerr=yerr,
                        color=clrs[kk], marker=markers[kk], markersize="8",
                        capsize=3, label=galaxy.name)

    # Standard curves
    demarc = lambda x: 0.61 / (x - 0.05) + 1.3  # Kauffman et al 2003, MNRAS, 346, 4, pp. 1055-1077. Eq 1
    demarc_kewley = lambda x: 0.61 / (
                x - 0.47) + 1.19  # Kewley F., Dopita M., Sutherland R., Heisler C., Trevena J., 2001, ApJ, 556,121
    demarc_liner = lambda x: 1.01 * x + 0.48  # Cid Fernandes et al 2010, MNRAS, 403,1036 Eq 10
    ax_BPT.plot(np.linspace(-2, 0), demarc(np.linspace(-2, 0)), "k-", lw=2)#, label="Kauffman et al 2003")
    if show_kewley:
        ax_BPT.plot(np.linspace(-2, 0.25), demarc_kewley(np.linspace(-2, 0.25)), "k--", lw=2)#, label="Kewley et al 2001")
    ax_BPT.plot(np.linspace(-0.43, 0.5), demarc_liner(np.linspace(-0.43, 0.5)), "k--", lw=2)#, label="Cid Fernandes et al 2010")

    # Labels
    lsz = 13.
    ax_BPT.annotate(r"\textbf{Star-forming}", (-1.30, 0), fontsize=lsz)
    ax_BPT.annotate(r"\textbf{LINER}", (0.23, 0), fontsize=lsz)
    ax_BPT.annotate(r"\textbf{Seyfert}", (-0.5, 1), fontsize=lsz)

    # Legend
    ax_BPT.legend(loc="lower left")
    # Axes
    ax_BPT.set_xlabel(r"$\log \, ({\rm [NII]/H_\alpha)}$")
    ax_BPT.set_ylabel(r"$\log \, ({\rm [OIII]/H_\beta)}$")
    ax_BPT.set_xlim(-1.5, 0.5)
    ax_BPT.set_ylim(-1, 1.2)
    utils.set_fontsize(ax_BPT, 13.)




def sub_sfms(ax_M, galaxies, clrs, markers):
    """
    Generate a SF vs. M* plot on top of PRIMUS galaxies

    Args:
        ax_M (matplotlib.axis):
        galaxies (list):  List of FRB.galaxies.frbgalaxy.FRBGalaxy objects
        clrs (list): List of matplotlib colors
        markers (list): List of matplotlib marker types

    """
    primus_path = os.path.join(resource_filename('frb', 'data'), 'Galaxies')
    utils.set_mplrc()

    # Load up
    primus_zcat = Table.read(os.path.join(primus_path, 'PRIMUS_2013_zcat_v1.fits'))
    primus_mass = Table.read(os.path.join(primus_path, 'PRIMUS_2014_mass_v1.fits'))

    gdz = (primus_zcat['Z'] > 0.2) & (primus_zcat['Z'] < 0.4)
    gd_mag = primus_zcat['SDSS_ABSMAG'][:,0] != 0.

    good_mass = primus_mass['ISGOOD'] == 1

    # PRIMUS
    # Photometry
    gd_color = gdz & gd_mag
    u_r = primus_zcat['SDSS_ABSMAG'][gd_color,0] - primus_zcat['SDSS_ABSMAG'][gd_color,2]
    rmag = primus_zcat['SDSS_ABSMAG'][gd_color,2]

    # Mass/SFR
    gd_msfr = good_mass & gdz
    mass = primus_mass['MASS'][gd_msfr]
    sfr = primus_mass['SFR'][gd_msfr]

    # Plot
    ms = 22.

    # Histogram
    xbins = 50
    ybins = 50
    counts, xedges, yedges = np.histogram2d(mass, sfr, bins=(xbins, ybins))
    #cm = plt.get_cmap('Reds')
    cm = plt.get_cmap('Greys')

    # SF
    mplt = ax_M.pcolormesh(xedges, yedges, counts.transpose(), cmap=cm)

    # Relation
    logm_star = np.linspace(8, 12)
    logsfr = lambda logm_star: -0.49 + 0.65 * (logm_star - 10) + 1.07 * (0.35 - 0.1)
    ax_M.plot(logm_star, logsfr(logm_star), "k--", lw=3)#, label="Moustakas et al 2013")

    # Galaxies
    for kk,galaxy in enumerate(galaxies):
        logM, sig_logM = utils.log_me(galaxy.derived['Mstar'], galaxy.derived['Mstar_err'])
        logS, sig_logS = utils.log_me(galaxy.derived['SFR_nebular'], 0.3*galaxy.derived['SFR_nebular'])
        ax_M.errorbar([logM], [logS], xerr=sig_logM, yerr=sig_logS,
                      color=clrs[kk], marker=markers[kk],
                     markersize="12", capsize=3, label=galaxy.name)

    ax_M.annotate(r"\textbf{Star forming}", (8.5, 0.8), fontsize=13.)
    ax_M.annotate(r"\textbf{Quiescent}", (11, -0.9), fontsize=13.)
    ax_M.set_xlabel("$\log \, (M_*/M_\odot)$")
    ax_M.set_ylabel("$\log \, SFR (M_\odot$/yr)")
    ax_M.legend(loc='lower right')
    ax_M.set_xlim(7.5, 11.8)
    ax_M.set_ylim(-3.4, 2.)