# Copyright (C) 2015-2016: The University of Edinburgh
#                 Authors: Craig Warren and Antonis Giannopoulos
#
# This file is part of gprMax.
#
# gprMax is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gprMax is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gprMax.  If not, see <http://www.gnu.org/licenses/>.

class Rx:
    """Receiever output points."""
    
    availableoutputs = ['Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz', 'Ix', 'Iy', 'Iz']
    
    def __init__(self, xcoord=None, ycoord=None, zcoord=None):
        """
        Args:
            xcoord (float): x-coordinate of location in model.
            ycoord (float): y-coordinate of location in model.
            zcoord (float): z-coordinate of location in model.
        """
        
        self.ID = None
        self.outputs = []
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.zcoord = zcoord