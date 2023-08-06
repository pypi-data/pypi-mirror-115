import pandas
import numpy
import dtale
import glob
import os
import ipywidgets
from IPython.display import display
import sys
from scipy.spatial.distance import cdist, pdist
from matplotlib import rcParams
import matplotlib.pyplot as plt
from plotnine import *

def RamachandranPlot(TorsionAngleDataFrame, ResidueRange = 1, ChainIDsToExclude = [], Name = '', ColorColumn = None, Colors = None):
    if type(ResidueRange) is int :
        ResidueStart = ResidueRange
        ResidueStop = TorsionAngleDataFrame["Residue Number"].max()
    elif type(ResidueRange) is list and len(ResidueRange) == 1:
        ResidueStart = ResidueRange[0]
        ResidueStop = TorsionAngleDataFrame["Residue Number"].max()
    else:
        ResidueStart = ResidueRange[0]
        ResidueStop =  ResidueRange[1]
    residues = list(numpy.linspace(ResidueStart, ResidueStop, dtype=numpy.integer))
    TorsionAngleDataFrame = TorsionAngleDataFrame[TorsionAngleDataFrame["Residue Number"].isin(residues)]
    TorsionAngleDataFrame = TorsionAngleDataFrame[~TorsionAngleDataFrame["Chain ID"].isin(ChainIDsToExclude)]
    plot = (ggplot(aes(x='Phi', y='Psi'), data=TorsionAngleDataFrame) 
     + geom_point(colour = "blue", alpha = .5)
     + scale_x_continuous(
            limits = (-180, 180),
            labels = (-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180),
            breaks = (-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180))
     + scale_y_continuous(
            limits = (-180, 180),
            labels = (-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180),
            breaks = (-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180))
     + theme_bw()
    )
    if ResidueStart == ResidueStop:
        plot += ggtitle(Name + " Torsion Angles for Residue " + str(ResidueStart))
    else:
        plot += ggtitle(Name + " Torsion Angles for Residues " + str(ResidueStart) + " to " + str(ResidueStop))
    if ColorColumn != None:
        plot += aes(color = ColorColumn)
        plot += geom_point()
    if Colors != None:
        plot += scale_color_manual(values=Colors)
    return plot
def SavePlot(Plot, FileName):
    ggsave(Plot, FileName)
def DisplayPlot(Plot):
    Plot.draw()
def ResizePlot(Plot, Dimension1, Dimension2):
    Plot += theme(figure_size = (Dimension1, Dimension2))
    return Plot
def SavePlot(Plot, FileName):
    rcParams.update({'text.usetex': False, "svg.fonttype": 'none' })
    ggsave(Plot, FileName)
def FindPotentialClashes(PDBDataFrame, Atom1Name, Atom2Name, DistanceLimit):
    PDBDataFrame["atom_name"] = PDBDataFrame.atom_name.str.slice(stop=1)
    Atom1Array = PDBDataFrame.loc[PDBDataFrame["atom_name"] == Atom1Name][["x_coord", "y_coord", "z_coord"]]
    Atom2Array = PDBDataFrame.loc[PDBDataFrame["atom_name"] == Atom2Name][["x_coord", "y_coord", "z_coord"]]
    if(Atom1Name != Atom2Name): Distances = cdist(Atom1Array, Atom2Array, metric = "euclidean") 
    elif(Atom1Name == Atom2Name): Distances = pdist(Atom1Array)
    Distances = Distances[Distances < DistanceLimit]
    Histogram = plt.hist(Distances)
    plt.xlabel(Atom1Name+  "-"+ Atom2Name +  " Distances up to " +str(DistanceLimit) + " angstroms")
    return Histogram, pandas.DataFrame(Distances)