

from __future__ import absolute_import
from __future__ import print_function
import os

try:
    CLAW = os.environ['CLAW']
except:
    raise Exception("*** Must first set CLAW enviornment variable")

# Scratch directory for storing topo and dtopo files:
scratch_dir = os.path.join(CLAW, 'geoclaw', 'scratch')

    
def make_dtopo(makeplots=False):
    """
    Create dtopo data file for deformation of sea floor due to earthquake.
    Uses the Okada model with fault parameters and mesh specified below.
    """
    from clawpack.geoclaw import dtopotools
    import numpy

    dtopo_fname = os.path.join(scratch_dir, "dtopoNavolato.tt3")

    # Specify subfault parameters for this simple fault model consisting
    # of a single subfault:

    usgs_subfault = dtopotools.SubFault()
    usgs_subfault.strike = 332.0
    usgs_subfault.length = 7.e3
    usgs_subfault.width = 2.e3
    usgs_subfault.depth = 15.e3
    usgs_subfault.slip = 850.0
    usgs_subfault.rake = 90.0
    usgs_subfault.dip = 350.0
    usgs_subfault.longitude = -108.8
    usgs_subfault.latitude = 23.9
    usgs_subfault.coordinate_specification = "top center"

    fault = dtopotools.Fault()
    fault.subfaults = [usgs_subfault]

    print("Magnitud: ",fault.Mw())

    if os.path.exists(dtopo_fname):
        print("*** Not regenerating dtopo file (already exists): %s" \
                    % dtopo_fname)
    else:
        print("Using Okada model to create dtopo file")

        x = numpy.linspace(-109.0, -107.4, 100)  # Longitudes (ajustadas a la región de Navolato)
        y = numpy.linspace(23.7, 25.0, 100)      # Latitudes (ajustadas a la región de Navolato)
        times = [1.]

        fault.create_dtopography(x,y,times)
        dtopo = fault.dtopo
        dtopo.write(dtopo_fname, dtopo_type=3)


    if makeplots:
        from matplotlib import pyplot as plt
        if fault.dtopo is None:
            # read in the pre-existing file:
            print("Reading in dtopo file...")
            dtopo = dtopotools.DTopography()
            dtopo.read(dtopo_fname, dtopo_type=3)
            x = dtopo.x
            y = dtopo.y
        plt.figure(figsize=(12,7))
        ax1 = plt.subplot(121)
        ax2 = plt.subplot(122)
        fault.plot_subfaults(axes=ax1,slip_color=True)
        ax1.set_xlim(x.min(),x.max())
        ax1.set_ylim(y.min(),y.max())
        dtopo.plot_dZ_colors(1.,axes=ax2)
        fname = os.path.splitext(os.path.split(dtopo_fname)[-1])[0] + '.png'
        plt.savefig(fname)
        print("Created ",fname)


if __name__=='__main__':
    make_dtopo(True)
