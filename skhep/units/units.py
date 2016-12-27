# Licensed under a 3-clause BSD style license, see LICENSE.
"""
*************************
Module of HEP basic units
*************************

In HEP the standard set of basic units was originally defined by the CLHEP [1]_ project. It is:

===================   ================== ====
Quantity              Name               Unit
===================   ================== ====
Length                millimeter         mm
Time                  nanosecond         ns
Energy                Mega electron Volt MeV
Positron charge       eplus
Temperature           kelvin             K
Amount of substance   mole               mol
Luminous intensity    candela            cd
Plane angle           radian             rad
Solid angle           steradian          sr
===================   ================== ====

----

**References**

.. [1] http://proj-clhep.web.cern.ch/proj-clhep/.
"""

#-----------------------------------------------------------------------------
# Import statements
#-----------------------------------------------------------------------------
from __future__ import absolute_import

from math import pi

from .prefixes import *

class Unit(object):
    # define the algebra of units in mul and div

    @staticmethod
    def mul(one, two):
        if isinstance(one, Millimeter) and isinstance(two, Millimeter):
            return Millimeter2(one.multiplier * two.multiplier)

        elif isinstance(one, Millimeter) and isinstance(two, Millimeter2):
            return Millimeter3(one.multiplier * two.multiplier)

        elif isinstance(one, Millimeter2) and isinstance(two, Millimeter):
            return Millimeter3(one.multiplier * two.multiplier)

        else:
            return one.__class__(one.multiplier * float(two))
        
    @staticmethod
    def div(one, two):
        if issubclass(one.__class__, two.__class__) or issubclass(two.__class__, one.__class__):
            return one.multiplier / two.multiplier

        elif isinstance(one, Millimeter2) and isinstance(two, Millimeter):
            return Millimeter(one.multiplier / two.multiplier)

        elif isinstance(one, Millimeter3) and isinstance(two, Millimeter):
            return Millimeter2(one.multiplier / two.multiplier)

        elif isinstance(one, Millimeter3) and isinstance(two, Millimeter2):
            return Millimeter(one.multiplier / two.multiplier)

        else:
            return one.__class__(one.multiplier / float(two))

    def __init__(self, multiplier):
        self.multiplier = float(multiplier)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.multiplier == other.multiplier
    def __ne__(self, other):
        return not self == other
    def __hash__(self):
        return hash((self.__class__, self.multiplier))

    def __repr__(self):
        return "{1}({0})".format(self.multiplier, self.__class__.__name__)
    def __str__(self):
        return "{0}*{1}".format(self.multiplier, self.name)

    def __abs__(self):
        return self.__class__(abs(self.multiplier))
    def __pos__(self):
        return self
    def __neg__(self):
        return self.__class__(-self.multiplier)
    def __round__(self, places=0):
        return self.__class__(round(self.multiplier, places))

    def __add__(self, other):
        if isinstance(other, Unit) and issubclass(other.__class__, self.__class__):
            return other.__class__(self.multiplier + other.multiplier)
        elif isinstance(other, Unit) and issubclass(self.__class__, other.__class__):
            return self.__class__(self.multiplier + other.multiplier)
        else:
            raise TypeError("cannot add {0} and {1}".format(self, other))
    def __radd__(other, self):
        if isinstance(other, Unit) and issubclass(other.__class__, self.__class__):
            return other.__class__(self.multiplier + other.multiplier)
        elif isinstance(other, Unit) and issubclass(self.__class__, other.__class__):
            return self.__class__(self.multiplier + other.multiplier)
        else:
            raise TypeError("cannot add {1} and {0}".format(self, other))
    def __sub__(self, other):
        if isinstance(other, Unit) and issubclass(other.__class__, self.__class__):
            return other.__class__(self.multiplier - other.multiplier)
        elif isinstance(other, Unit) and issubclass(self.__class__, other.__class__):
            return self.__class__(self.multiplier - other.multiplier)
        else:
            raise TypeError("cannot subtract {0} and {1}".format(self, other))
    def __rsub__(other, self):
        if isinstance(other, Unit) and issubclass(other.__class__, self.__class__):
            return other.__class__(self.multiplier - other.multiplier)
        elif isinstance(other, Unit) and issubclass(self.__class__, other.__class__):
            return self.__class__(self.multiplier - other.multiplier)
        else:
            raise TypeError("cannot subtract {1} and {0}".format(self, other))
    def __mul__(self, other):
        return Unit.mul(self, other)
    def __rmul__(other, self):
        return Unit.mul(other, self)
    def __pow__(self, other):
        if other == 2:
            return Unit.mul(self, self)
        elif other == 3:
            return Unit.mul(Unit.mul(self, self), self)
        elif other == 4:
            return Unit.mul(Unit.mul(Unit.mul(self, self), self), self)
        elif round(other, 7) == 1.0/2.0:
            return Unit.div(self, self)
        elif round(other, 7) == 1.0/3.0:
            return Unit.div(Unit.div(self, self), self)
        elif round(other, 7) == 1.0/4.0:
            return Unit.div(Unit.div(Unit.div(self, self), self), self)
        else:
            raise TypeError("cannot raise {1} to the {0} power".format(self, other))
    def __rpow__(other, self):
        raise TypeError("cannot raise {1} to the {0} power".format(self, other))
    def __div__(self, other):
        return Unit.div(self, other)
    def __rdiv__(other, self):
        return Unit.div(self, other)
    def __truediv__(self, other):
        return Unit.div(self, other)
    def __rtruediv__(other, self):
        return Unit.div(self, other)
    def __floordiv__(self, other):
        raise TypeError("cannot floor-divide {0} by {1}".format(self, other))
    def __rfloordiv__(other, self):
        raise TypeError("cannot floor-divide {1} by {0}".format(self, other))

    def __mod__(self, other):
        raise TypeError("cannot take {0} modulo {1}".format(self, other))
    def __rmod__(other, self):
        raise TypeError("cannot take {0} modulo {1}".format(self, other)) 
    def __divmod__(self, other):
        raise TypeError("cannot divmod {0} by {1}".format(self, other))
    def __rdivmod__(other, self):
        raise TypeError("cannot divmod {0} by {1}".format(self, other))

# --------------------------------------------------------------------
# Units of length
# ---------------

class Millimeter(Unit):
    name = "mm"

class Millimeter2(Unit):
    name = "mm2"

class Millimeter3(Unit):
    name = "mm3"

millimeter  = Millimeter(1.0)
millimeter2 = Millimeter2(1.0)
millimeter3 = Millimeter3(1.0)

mm  = millimeter
mm2 = millimeter2
mm3 = millimeter3

meter  = kilo * millimeter
meter2 = meter * meter
meter3 = meter * meter * meter

m  = meter
m2 = meter2
m3 = meter3

centimeter  = centi * meter
centimeter2 = centimeter * centimeter
centimeter3 = centimeter * centimeter * centimeter

cm  = centimeter
cm2 = centimeter2
cm3 = centimeter3

kilometer = kilo * meter
kilometer2 = kilometer * kilometer
kilometer3 = kilometer * kilometer * kilometer

km  = kilometer
km2 = kilometer2
km3 = kilometer3

micrometer = micro * meter
nanometer  = nano  * meter
angstrom   = 1e-10 * meter
fermi      = femto * meter

barn = 1.e-28 * meter2

millibarn  = milli * barn
microbarn  = micro * barn
nanobarn   = nano  * barn
picobarn   = pico  * barn

# --------------------------------------------------------------------
# Units of time
# -------------

nanosecond  = 1.

second      = giga  * nanosecond
millisecond = milli * second
microsecond = micro * second
picosecond  = pico  * second
femtosecond = femto * second

ns = nanosecond
s  = second
ms = millisecond

hertz = 1. / second
kilohertz = kilo * hertz
megahertz = mega * hertz

Hz = hertz
kHz = kilo * hertz
MHz = mega * hertz
GHz = giga * hertz

# --------------------------------------------------------------------
# Units of energy
# ---------------

megaelectronvolt = 1.

electronvolt     = micro * megaelectronvolt
kiloelectronvolt = kilo  * electronvolt
gigaelectronvolt = giga  * electronvolt
teraelectronvolt = tera  * electronvolt
petaelectronvolt = peta  * electronvolt
exaelectronvolt  = exa   * electronvolt

eV  = electronvolt
keV = kiloelectronvolt
MeV = megaelectronvolt
GeV = gigaelectronvolt
TeV = teraelectronvolt
PeV = petaelectronvolt
EeV = exaelectronvolt

# --------------------------------------------------------------------
# Units of electric charge
# ------------------------

eplus = 1.    # positron charge

# --------------------------------------------------------------------
# Units of temperature
# ---------------------

kelvin = 1.

# --------------------------------------------------------------------
# Units of amount of substance
# ----------------------------

mole = 1.

mol = mole

# --------------------------------------------------------------------
# Units of luminous intensity
# ---------------------------

candela = 1.

# --------------------------------------------------------------------
# Units of angles
# ---------------

radian      = 1.    # plane angle
milliradian = milli * radian

steradian   = 1.    # solid angle

degree = (pi/180.) * radian

rad  = radian
mrad = milliradian
sr   = steradian

deg  = degree
