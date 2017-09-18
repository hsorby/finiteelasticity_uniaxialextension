
# Add example executable
add_executable(uniaxial_extension_f uniaxial_extension.F90)

# Link to opencmiss
# -----------------
#
# This simply uses the 'opencmisslibs' target created by finding the OpenCMISSLibs package earlier.
#
# Alternatively, you can also directly invoke 'find_package(Iron <IRON_VERSION>)' to explicitly
# require that version.  If you do this you will also need to change the target link library from
# 'opencmisslibs' to 'iron'. 
target_link_libraries(uniaxial_extension_f PRIVATE opencmisslibs mpi)

# Add an install target to place the executable in the install tree.
install(TARGETS uniaxial_extension_f 
    DESTINATION bin)
