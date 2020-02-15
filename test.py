from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
from sys import stdout

#ff     = ForceField('amber/protein.ff14SB.xml','amber/tip3p_standard.xml')
prmtop = AmberPrmtopFile('prmtop')
#inpcrd = AmberInpcrdFile('input.inpcrd')
pdb    = PDBFile('linear_prod.pdb')

#model = Modeller(
#    prmtop.topology,
#    pdb.positions,
#)
#model.addSolvent(ff, padding=1.0*nanometers)
system = prmtop.createSystem(nonbondedMethod=CutoffNonPeriodic,nonbondedCutoff=1*nanometers,constraints=AllBonds,implicitSolvent=HCT)
integrator = LangevinIntegrator(300*kelvin,20/picosecond,0.002*picoseconds,)
#integrator = BAOABLangevinIntegrator(300*kelvin, 1/picosecond, 0.004*picoseconds)
simulation = Simulation(prmtop.topology, system, integrator)
#simulation.context.setPositions(inpcrd.positions)
simulation.context.setPositions(pdb.positions)
#if inpcrd.boxVectors is not None:
#    simulation.context.setPeriodicBoxVectors(*inpcrd.boxVectors)
simulation.minimizeEnergy()
simulation.reporters.append(PDBReporter('output.pdb', 1000))
simulation.reporters.append(StateDataReporter(stdout, 1000, step=True, potentialEnergy=True, temperature=True))
simulation.step(1000)
simulation.reporters.append(DCDReporter('output.dcd', 100))
simulation.reporters.append(CheckpointReporter('%s.chk' % 'output.dcd', 1000))
