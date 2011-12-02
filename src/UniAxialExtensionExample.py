#> \file
#> \author Chris Bradley
#> \brief This is an example script to solve a finite elasticity equation using openCMISS calls in python.
#>
#> \section LICENSE
#>
#> Version: MPL 1.1/GPL 2.0/LGPL 2.1
#>
#> The contents of this file are subject to the Mozilla Public License
#> Version 1.1 (the "License"); you may not use this file except in
#> compliance with the License. You may obtain a copy of the License at
#> http://www.mozilla.org/MPL/
#>
#> Software distributed under the License is distributed on an "AS IS"
#> basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
#> License for the specific language governing rights and limitations
#> under the License.
#>
#> The Original Code is openCMISS
#>
#> The Initial Developer of the Original Code is University of Auckland,
#> Auckland, New Zealand and University of Oxford, Oxford, United
#> Kingdom. Portions created by the University of Auckland and University
#> of Oxford are Copyright (C) 2007 by the University of Auckland and
#> the University of Oxford. All Rights Reserved.
#>
#> Contributor(s): 
#>
#> Alternatively, the contents of this file may be used under the terms of
#> either the GNU General Public License Version 2 or later (the "GPL"), or
#> the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
#> in which case the provisions of the GPL or the LGPL are applicable instead
#> of those above. if you wish to allow use of your version of this file only
#> under the terms of either the GPL or the LGPL, and not to allow others to
#> use your version of this file under the terms of the MPL, indicate your
#> decision by deleting the provisions above and replace them with the notice
#> and other provisions required by the GPL or the LGPL. if you do not delete
#> the provisions above, a recipient may use your version of this file under
#> the terms of any one of the MPL, the GPL or the LGPL.
#>

#> \example FiniteElasticity/UniAxialExtension/src/UniAxialExtensionExample.py
## Example script to solve a finite elasticity equation using openCMISS calls in python.
## \par Latest Builds:
## \li <a href='http://autotest.bioeng.auckland.ac.nz/opencmiss-build/logs_x86_64-linux/FiniteElasticity/UniAxialExtension/build-intel'>Linux Intel Build</a>
## \li <a href='http://autotest.bioeng.auckland.ac.nz/opencmiss-build/logs_x86_64-linux/FiniteElasticity/UniAxialExtension/build-gnu'>Linux GNU Build</a>
#<

#> Main script
# Add Python bindings directory to PATH
import sys, os

sys.path.append(os.sep.join((os.environ['OPENCMISS_ROOT'],'cm','bindings','python')))

# Intialise OpenCMISS
from opencmiss import CMISS

# Set problem parameters
height = 1.0
width = 1.0
length = 1.0

UsePressureBasis = False
NumberOfGaussXi = 2

coordinateSystemUserNumber = 1
regionUserNumber = 1
basisUserNumber = 1
pressureBasisUserNumber = 2
generatedMeshUserNumber = 1
meshUserNumber = 1
decompositionUserNumber = 1
geometricFieldUserNumber = 1
fibreFieldUserNumber = 2
materialFieldUserNumber = 3
dependentFieldUserNumber = 4
equationsSetUserNumber = 1
equationsSetFieldUserNumber = 5
problemUserNumber = 1

CMISS.ErrorHandlingModeSet(CMISS.ErrorHandlingModes.TrapError)

# Set all diganostic levels on for testing
CMISS.DiagnosticsSetOn(CMISS.DiagnosticTypes.All,[1,2,3,4,5],"Diagnostics",["DOMAIN_MAPPINGS_LOCAL_FROM_GLOBAL_CALCULATE"])

numberGlobalXElements = 1
numberGlobalYElements = 1
numberGlobalZElements = 1
totalNumberOfNodes=8
totalNumberOfElements=1
InterpolationType = 1
if(UsePressureBasis):
  numberOfMeshComponents = 2
else:
  numberOfMeshComponents = 1
if(numberGlobalZElements==0):
    numberOfXi = 2
else:
    numberOfXi = 3

# Get the number of computational nodes and this computational node number
numberOfComputationalNodes = CMISS.ComputationalNumberOfNodesGet()
computationalNodeNumber = CMISS.ComputationalNodeNumberGet()

# Create a 3D rectangular cartesian coordinate system
coordinateSystem = CMISS.CoordinateSystem()
coordinateSystem.CreateStart(coordinateSystemUserNumber)
coordinateSystem.DimensionSet(3)
coordinateSystem.CreateFinish()

# Create a region and assign the coordinate system to the region
region = CMISS.Region()
region.CreateStart(regionUserNumber,CMISS.WorldRegion)
region.LabelSet("Region")
region.coordinateSystem = coordinateSystem
region.CreateFinish()

# Define basis
basis = CMISS.Basis()
basis.CreateStart(basisUserNumber)
if InterpolationType == (1,2,3,4):
    basis.type = CMISS.BasisTypes.LagrangeHermiteTP
elif InterpolationType == (7,8,9):
    basis.type = CMISS.BasisTypes.BasisSimplexType
basis.numberOfXi = numberOfXi
basis.interpolationXi = [CMISS.BasisInterpolationSpecifications.LinearLagrange]*numberOfXi
if(NumberOfGaussXi>0):
    basis.quadratureNumberOfGaussXi = [NumberOfGaussXi]*numberOfXi
basis.CreateFinish()

if(UsePressureBasis):
    # Define pressure basis
    pressureBasis = CMISS.Basis()
    pressureBasis.CreateStart(pressureBasisUserNumber)
    if InterpolationType == (1,2,3,4):
        pressureBasis.type = CMISS.BasisTypes.LagrangeHermiteTP
    elif InterpolationType == (7,8,9):
        pressureBasis.type = CMISS.BasisTypes.BasisSimplexType
    pressureBasis.numberOfXi = numberOfXi
    pressureBasis.interpolationXi = [CMISS.BasisInterpolationSpecifications.LinearLagrange]*numberOfXi
    if(NumberOfGaussXi>0):
        pressureBasis.quadratureNumberOfGaussXi = [NumberOfGaussXi]*numberOfXi
    pressureBasis.CreateFinish()

# Start the creation of a manually generated mesh in the region
mesh = CMISS.Mesh()
mesh.CreateStart(meshUserNumber,region,numberOfXi)
mesh.NumberOfComponentsSet(numberOfMeshComponents)
mesh.NumberOfElementsSet(totalNumberOfElements)

#Define nodes for the mesh
nodes = CMISS.Nodes()
nodes.CreateStart(region,totalNumberOfNodes)
nodes.CreateFinish()

elements = CMISS.MeshElements()
meshComponentNumber=1
elements.CreateStart(mesh,meshComponentNumber,basis)
elements.NodesSet(1,[1,2,3,4,5,6,7,8])
elements.CreateFinish()

mesh.CreateFinish() 

# Create a decomposition for the mesh
decomposition = CMISS.Decomposition()
decomposition.CreateStart(decompositionUserNumber,mesh)
decomposition.type = CMISS.DecompositionTypes.Calculated
decomposition.numberOfDomains = numberOfComputationalNodes
decomposition.CreateFinish()

# Create a field for the geometry
geometricField = CMISS.Field()
geometricField.CreateStart(geometricFieldUserNumber,region)
geometricField.MeshDecompositionSet(decomposition)
geometricField.TypeSet(CMISS.FieldTypes.Geometric)
geometricField.VariableLabelSet(CMISS.FieldVariableTypes.U,"Geometry")
geometricField.ComponentMeshComponentSet(CMISS.FieldVariableTypes.U,1,1)
geometricField.ComponentMeshComponentSet(CMISS.FieldVariableTypes.U,2,1)
geometricField.ComponentMeshComponentSet(CMISS.FieldVariableTypes.U,3,1)
if InterpolationType == 4:
    geometricField.fieldScalingType = CMISS.FieldScalingTypes.ArithmeticMean
geometricField.CreateFinish()

# Update the geometric field parameters manually
geometricField.ParameterSetUpdateStart(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues)
# node 1
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,1,1,0.0)
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,1,2,0.0)
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,1,3,0.0)
# node 2
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,2,1,height)
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,2,2,0.0)
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,2,3,0.0)
# node 3
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,3,1,0.0)
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,3,2,width)
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,3,3,0.0)
# node 4
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,4,1,height)
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,4,2,width)
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,4,3,0.0)
# node 5
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,5,1,0.0)
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,5,2,0.0)
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,5,3,length)
# node 6
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,6,1,height)
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,6,2,0.0)
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,6,3,length)
# node 7
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,7,1,0.0)
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,7,2,width)
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,7,3,length)
# node 8
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,8,1,height)
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,8,2,width)
geometricField.ParameterSetUpdateNodeDP(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,1,8,3,length)
geometricField.ParameterSetUpdateFinish(CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues)

# Create a fibre field and attach it to the geometric field
fibreField = CMISS.Field()
fibreField.CreateStart(fibreFieldUserNumber,region)
fibreField.TypeSet(CMISS.FieldTypes.Fibre)
fibreField.MeshDecompositionSet(decomposition)
fibreField.GeometricFieldSet(geometricField)
fibreField.VariableLabelSet(CMISS.FieldVariableTypes.U,"Fibre")
if InterpolationType == 4:
    fibreField.fieldScalingType = CMISS.FieldScalingTypes.ArithmeticMean
fibreField.CreateFinish()

# Create the equations_set
equationsSetField = CMISS.Field()
equationsSet = CMISS.EquationsSet()
equationsSet.CreateStart(equationsSetUserNumber,region,fibreField, \
    CMISS.EquationsSetClasses.Elasticity,
    CMISS.EquationsSetTypes.FiniteElasticity, \
    CMISS.EquationsSetSubtypes.MooneyRivlin, \
    equationsSetFieldUserNumber, equationsSetField)
equationsSet.CreateFinish()

# Create the dependent field
dependentField = CMISS.Field()
equationsSet.DependentCreateStart(dependentFieldUserNumber,dependentField)
dependentField.VariableLabelSet(CMISS.FieldVariableTypes.U,"Dependent")
dependentField.ComponentInterpolationSet(CMISS.FieldVariableTypes.U,4,CMISS.FieldInterpolationTypes.ElementBased)
dependentField.ComponentInterpolationSet(CMISS.FieldVariableTypes.DelUDelN,4,CMISS.FieldInterpolationTypes.ElementBased)
if(UsePressureBasis):
    # Set the pressure to be nodally based and use the second mesh component
    if InterpolationType == 4:
        dependentField.ComponentInterpolationSet(CMISS.FieldVariableTypes.U,4,CMISS.FieldInterpolationTypes.NodeBased)
        dependentField.ComponentInterpolationSet(CMISS.FieldVariableTypes.DelUDelN,4,CMISS.FieldInterpolationTypes.NodeBased)
    dependentField.ComponentMeshComponentSet(CMISS.FieldVariableTypes.U,4,2)
    dependentField.ComponentMeshComponentSet(CMISS.FieldVariableTypes.DelUDelN,4,2)
if InterpolationType == 4:
    dependentField.fieldScalingType = CMISS.FieldScalingTypes.ArithmeticMean
equationsSet.DependentCreateFinish()


# Initialise dependent field from undeformed geometry and displacement bcs and set hydrostatic pressure
CMISS.Field.ParametersToFieldParametersComponentCopy( \
    geometricField,CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1, \
    dependentField,CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1)
CMISS.Field.ParametersToFieldParametersComponentCopy( \
    geometricField,CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,2, \
    dependentField,CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,2)
CMISS.Field.ParametersToFieldParametersComponentCopy( \
    geometricField,CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,3, \
    dependentField,CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,3)
CMISS.Field.ComponentValuesInitialiseDP( \
    dependentField,CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,4,-8.0)

# Create the material field
materialField = CMISS.Field()
equationsSet.MaterialsCreateStart(materialFieldUserNumber,materialField)
materialField.VariableLabelSet(CMISS.FieldVariableTypes.U,"Material")
equationsSet.MaterialsCreateFinish()

# Set Mooney-Rivlin constants c10 and c01 respectively.
CMISS.Field.ComponentValuesInitialiseDP( \
    materialField,CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,1,2.0)
CMISS.Field.ComponentValuesInitialiseDP( \
    materialField,CMISS.FieldVariableTypes.U,CMISS.FieldParameterSetTypes.FieldValues,2,6.0)

# Create equations
equations = CMISS.Equations()
equationsSet.EquationsCreateStart(equations)
equations.sparsityType = CMISS.EquationsSparsityTypes.Sparse
equations.outputType = CMISS.EquationsOutputTypes.NONE
equationsSet.EquationsCreateFinish()

# Define the problem
problem = CMISS.Problem()
problem.CreateStart(problemUserNumber)
problem.SpecificationSet(CMISS.ProblemClasses.Elasticity, \
        CMISS.ProblemTypes.FiniteElasticity, \
        CMISS.ProblemSubTypes.NONE)
problem.CreateFinish()

# Create control loops
problem.ControlLoopCreateStart()
problem.ControlLoopCreateFinish()

# Create problem solver
nonLinearSolver = CMISS.Solver()
linearSolver = CMISS.Solver()
problem.SolversCreateStart()
problem.SolverGet([CMISS.ControlLoopIdentifiers.Node],1,nonLinearSolver)
nonLinearSolver.outputType = CMISS.SolverOutputTypes.Progress
nonLinearSolver.NewtonJacobianCalculationTypeSet(CMISS.JacobianCalculationTypes.FDCalculated)
nonLinearSolver.NewtonLinearSolverGet(linearSolver)
linearSolver.linearType = CMISS.LinearSolverTypes.Direct
#linearSolver.libraryType = CMISS.SolverLibraries.LAPACK
problem.SolversCreateFinish()

# Create solver equations and add equations set to solver equations
solver = CMISS.Solver()
solverEquations = CMISS.SolverEquations()
problem.SolverEquationsCreateStart()
problem.SolverGet([CMISS.ControlLoopIdentifiers.Node],1,solver)
solver.SolverEquationsGet(solverEquations)
solverEquations.sparsityType = CMISS.SolverEquationsSparsityTypes.Sparse
equationsSetIndex = solverEquations.EquationsSetAdd(equationsSet)
problem.SolverEquationsCreateFinish()

# Prescribe boundary conditions (absolute nodal parameters)
boundaryConditions = CMISS.BoundaryConditions()
solverEquations.BoundaryConditionsCreateStart(boundaryConditions)

#Set x=0 nodes to no x displacment in x. Set x=width nodes to 10% x displacement
boundaryConditions.AddNode(dependentField,CMISS.FieldVariableTypes.U,1,1,1,1,CMISS.BoundaryConditionsTypes.Fixed,0.0)
boundaryConditions.AddNode(dependentField,CMISS.FieldVariableTypes.U,1,1,3,1,CMISS.BoundaryConditionsTypes.Fixed,0.0)
boundaryConditions.AddNode(dependentField,CMISS.FieldVariableTypes.U,1,1,5,1,CMISS.BoundaryConditionsTypes.Fixed,0.0)
boundaryConditions.AddNode(dependentField,CMISS.FieldVariableTypes.U,1,1,7,1,CMISS.BoundaryConditionsTypes.Fixed,0.0)

boundaryConditions.AddNode(dependentField,CMISS.FieldVariableTypes.U,1,1,2,1,CMISS.BoundaryConditionsTypes.Fixed,0.1*width)
boundaryConditions.AddNode(dependentField,CMISS.FieldVariableTypes.U,1,1,4,1,CMISS.BoundaryConditionsTypes.Fixed,0.1*width)
boundaryConditions.AddNode(dependentField,CMISS.FieldVariableTypes.U,1,1,6,1,CMISS.BoundaryConditionsTypes.Fixed,0.1*width)
boundaryConditions.AddNode(dependentField,CMISS.FieldVariableTypes.U,1,1,8,1,CMISS.BoundaryConditionsTypes.Fixed,0.1*width)

# Set y=0 nodes to no y displacement
boundaryConditions.AddNode(dependentField,CMISS.FieldVariableTypes.U,1,1,1,2,CMISS.BoundaryConditionsTypes.Fixed,0.0)
boundaryConditions.AddNode(dependentField,CMISS.FieldVariableTypes.U,1,1,2,2,CMISS.BoundaryConditionsTypes.Fixed,0.0)
boundaryConditions.AddNode(dependentField,CMISS.FieldVariableTypes.U,1,1,5,2,CMISS.BoundaryConditionsTypes.Fixed,0.0)
boundaryConditions.AddNode(dependentField,CMISS.FieldVariableTypes.U,1,1,6,2,CMISS.BoundaryConditionsTypes.Fixed,0.0)

# Set z=0 nodes to no y displacement
boundaryConditions.AddNode(dependentField,CMISS.FieldVariableTypes.U,1,1,1,3,CMISS.BoundaryConditionsTypes.Fixed,0.0)
boundaryConditions.AddNode(dependentField,CMISS.FieldVariableTypes.U,1,1,2,3,CMISS.BoundaryConditionsTypes.Fixed,0.0)
boundaryConditions.AddNode(dependentField,CMISS.FieldVariableTypes.U,1,1,3,3,CMISS.BoundaryConditionsTypes.Fixed,0.0)
boundaryConditions.AddNode(dependentField,CMISS.FieldVariableTypes.U,1,1,4,3,CMISS.BoundaryConditionsTypes.Fixed,0.0)

# Below commented out until CMISSGeneratedMeshSurfaceGet becomes available through the OpenCMISS python api.
#CMISS.GeneratedMeshSurfaceGet(GeneratedMesh,CMISSGeneratedMeshRegularBottomSurface,BottomSurfaceNodes,BottomNormalXi)
#CMISS.GeneratedMeshSurfaceGet(GeneratedMesh,CMISSGeneratedMeshRegularLeftSurface,LeftSurfaceNodes,LeftNormalXi)
#CMISS.GeneratedMeshSurfaceGet(GeneratedMesh,CMISSGeneratedMeshRegularRightSurface,RightSurfaceNodes,RightNormalXi)
#CMISS.GeneratedMeshSurfaceGet(GeneratedMesh,CMISSGeneratedMeshRegularFrontSurface,FrontSurfaceNodes,BackNormalXi)
#if(InterpolationType==CMISSBasisCubicHermiteInterpolation):
##Fix x derivatives at x=0 and x=1 in xi2 and xi3
#  DO node_idx=1,SIZE(LeftSurfaceNodes,1)
#    NodeNumber=LeftSurfaceNodes(node_idx)
#  CMISS.DecompositionNodeDomainGet(Decomposition,NodeNumber,1,NodeDomain)
#    if(NodeDomain==ComputationalNodeNumber):
#    CMISS.BoundaryConditionsSetNode(BoundaryConditions,DependentField,CMISSFieldUVariableType,1,CMISSGlobalDerivativeS2, &
#        & NodeNumber,1,CMISSBoundaryConditionFixed,0.0_CMISSDP)
#    CMISS.BoundaryConditionsSetNode(BoundaryConditions,DependentField,CMISSFieldUVariableType,1,CMISSGlobalDerivativeS3, &
#        & NodeNumber,1,CMISSBoundaryConditionFixed,0.0_CMISSDP)
#    CMISS.BoundaryConditionsSetNode(BoundaryConditions,DependentField,CMISSFieldUVariableType,1,CMISSGlobalDerivativeS2S3, &
#        & NodeNumber,1,CMISSBoundaryConditionFixed,0.0_CMISSDP)
#    ENDif
#  ENDDO
#  DO node_idx=1,SIZE(RightSurfaceNodes,1)
#    NodeNumber=RightSurfaceNodes(node_idx)
#  CMISS.DecompositionNodeDomainGet(Decomposition,NodeNumber,1,NodeDomain)
#    if(NodeDomain==ComputationalNodeNumber):
#    CMISS.BoundaryConditionsSetNode(BoundaryConditions,DependentField,CMISSFieldUVariableType,1,CMISSGlobalDerivativeS2, &
#        & NodeNumber,1,CMISSBoundaryConditionFixed,0.0_CMISSDP)
#    CMISS.BoundaryConditionsSetNode(BoundaryConditions,DependentField,CMISSFieldUVariableType,1,CMISSGlobalDerivativeS3, &
#        & NodeNumber,1,CMISSBoundaryConditionFixed,0.0_CMISSDP)
#    CMISS.BoundaryConditionsSetNode(BoundaryConditions,DependentField,CMISSFieldUVariableType,1,CMISSGlobalDerivativeS2S3, &
#        & NodeNumber,1,CMISSBoundaryConditionFixed,0.0_CMISSDP)
#    ENDif
#  ENDDO
#ENDif

solverEquations.BoundaryConditionsCreateFinish()

# Solve the problem
problem.Solve()

# Export results
fields = CMISS.Fields()
CMISS.FieldsTypeCreateRegion(region,fields)
CMISS.FieldIONodesExport(fields,"../UniAxialExtension","FORTRAN")
CMISS.FieldIOElementsExport(fields,"../UniAxialExtension","FORTRAN")
fields.Finalise()


