

#!/usr/bin/env python

# noinspection PyUnresolvedReferences
import vtk
import vtkmodules.vtkInteractionStyle
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkIOImage import vtkDICOMImageReader
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkIOXML import vtkXMLImageDataReader
#from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkCommonCore import vtkStringArray
from vtkmodules.vtkCommonDataModel import (
    vtkCylinder,
    vtkSphere
)
from vtkmodules.vtkImagingCore import (
  vtkImageCast,
  vtkImageShiftScale
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty
)


from vtkmodules.vtkRenderingVolume import vtkFixedPointVolumeRayCastMapper
# noinspection PyUnresolvedReferences
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkOpenGLRayCastImageDisplayHelper
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera

def get_program_parameters():
  import argparse
  description = 'Read a VTK image data file.'
  epilogue = ''''''
  parser = argparse.ArgumentParser(description=description, epilog=epilogue,
                                   formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('filename', help='ironProt.vtk')
  args = parser.parse_args()
  return args.filename

def main():
  filename = get_program_parameters()
  colors = vtkNamedColors()

  # Create the renderers, render window, and interactor
  renWin = vtkRenderWindow()
  iren = vtkRenderWindowInteractor()
  iren.SetRenderWindow(renWin)
  ren = vtkRenderer()
  renWin.AddRenderer(ren)
  renWin.SetWindowName("MinIntensityRendering")

  # Read the data from a vtk file
  reader = vtkStructuredPointsReader()
  reader.SetFileName(filename)
  reader.Update()

  # Create a transfer function mapping scalar value to opacity
  oTFun = vtkPiecewiseFunction()
  oTFun.AddSegment(0, 1.0, 256, 0.1)

  cTFun = vtkColorTransferFunction()
  cTFun.AddRGBPoint(0, 1.0, 1.0, 1.0)
  cTFun.AddRGBPoint(255, 1.0, 1.0, 1.0)

  # Need to crop to actually see minimum intensity
  clip = vtk.vtkImageClip()
  clip.SetInputConnection(reader.GetOutputPort())
  clip.SetOutputWholeExtent(0, 66, 0, 66, 30, 37)
  clip.ClipDataOn()

  property = vtkVolumeProperty()
  property.SetScalarOpacity(oTFun)
  property.SetColor(cTFun)
  property.SetInterpolationTypeToLinear()

  mapper = vtkFixedPointVolumeRayCastMapper()
  mapper.SetBlendModeToMinimumIntensity()
  mapper.SetInputConnection(clip.GetOutputPort())

  volume = vtkVolume()
  volume.SetMapper(mapper)
  volume.SetProperty(property)

  ren.AddViewProp(volume)
  ren.SetBackground(colors.GetColor3d("MidnightBlue"))

  renWin.Render()

  ren.GetActiveCamera().Zoom(1.3)

  iren.Start()

if __name__ == '__main__':
    main()