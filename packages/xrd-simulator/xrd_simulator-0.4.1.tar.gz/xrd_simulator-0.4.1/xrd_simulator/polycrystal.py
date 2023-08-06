"""The polycrystal module is used to represent a polycrystalline sample. The :class:`xrd_simulator.polycrystal.Polycrystal`
object holds the function :func:`xrd_simulator.polycrystal.Polycrystal.diffract` which may be used to compute diffraction.
To move the sample spatially, the function :func:`xrd_simulator.polycrystal.Polycrystal.transform` can be used.
Here is a minimal example of how to instantiate a polycrystal object and save it to disc:

    Examples:
        .. literalinclude:: examples/example_init_polycrystal.py

Below follows a detailed description of the polycrystal class attributes and functions.

"""
import numpy as np
from scipy.spatial import ConvexHull
import dill
import copy
from xfab import tools
from xrd_simulator.scattering_unit import ScatteringUnit
from xrd_simulator import utils, laue
from multiprocessing import Pool


def _diffract(dict):


    beam                = dict['beam']
    detector            = dict['detector']
    rigid_body_motion   = dict['rigid_body_motion']
    phases              = dict['phases']
    espherecentroids    = dict['espherecentroids']
    eradius             = dict['eradius']
    orientation_lab     = dict['orientation_lab']
    eB                  = dict['eB']
    element_phase_map   = dict['element_phase_map']
    ecoord              = dict['ecoord']
    verbose             = dict['verbose']
    number_of_elements  = ecoord.shape[0]

    rho_0_factor = -beam.wave_vector.dot(rigid_body_motion.rotator.K2)
    rho_1_factor = beam.wave_vector.dot(rigid_body_motion.rotator.K)
    rho_2_factor = beam.wave_vector.dot(
        np.eye(3, 3) + rigid_body_motion.rotator.K2)

    scattering_units = []

    proximity_intervals = beam._get_proximity_intervals(
                                        espherecentroids,
                                        eradius,
                                        rigid_body_motion)

    possible_scatterers = np.sum([pi[0] is not None for pi in proximity_intervals])

    if verbose: 
        progress_update_rate = 10**int(len(str(int(number_of_elements/1000.)))-1)

    for ei in range(number_of_elements):

        if verbose and ei % progress_update_rate == 0:
            progress_bar_message = "Found " + \
                str(possible_scatterers) + " scatterers (mesh has "+str(number_of_elements)+" elements)"
            progress_fraction = float(
                ei + 1) / number_of_elements
            utils._print_progress(
                progress_fraction,
                message=progress_bar_message)

        # skip elements not illuminated
        if proximity_intervals[ei][0] is None:
            continue
        
        G_0 = laue.get_G(orientation_lab[ei], eB[ei],
                            phases[element_phase_map[ei]].miller_indices.T)

        rho_0s = rho_0_factor.dot(G_0)
        rho_1s = rho_1_factor.dot(G_0)
        rho_2s = rho_2_factor.dot(G_0) + np.sum((G_0 * G_0), axis=0) / 2.

        t1, t2 = laue.find_solutions_to_tangens_half_angle_equation(rho_0s, rho_1s, rho_2s, rigid_body_motion.rotation_angle)

        for hkl_indx in range(G_0.shape[1]):
            for time in (t1[hkl_indx],t2[hkl_indx]):
                if ~np.isnan(time):

                    if utils._contained_by_intervals(time, proximity_intervals[ei]):

                        G = rigid_body_motion.rotate(
                            G_0[:, hkl_indx], time)
                        scattered_wave_vector = G + beam.wave_vector

                        source = rigid_body_motion(espherecentroids[ei], time)
                        zd, yd = detector.get_intersection(scattered_wave_vector, source)

                        if detector.contains(zd, yd):

                            element_vertices_0 = ecoord[ei]

                            element_vertices = rigid_body_motion(
                                element_vertices_0.T, time).T

                            scattering_region = beam.intersect(element_vertices)

                            if scattering_region is not None:
                                scattering_unit = ScatteringUnit(scattering_region,
                                                        scattered_wave_vector,
                                                        beam.wave_vector,
                                                        beam.wavelength,
                                                        beam.polarization_vector,
                                                        rigid_body_motion.rotation_axis,
                                                        time,
                                                        phases[element_phase_map[ei]],
                                                        hkl_indx,
                                                        ei)

                                scattering_units.append(scattering_unit)
    return scattering_units

class Polycrystal():

    """Represents a multi-phase polycrystal as a tetrahedral mesh where each element can be a single crystal

    The polycrystal is created in laboratory coordinates. At instantiation it is assumed that the sample and
    lab coordinate systems are aligned.

    Args:
        mesh (:obj:`xrd_simulator.mesh.TetraMesh`): Object representing a tetrahedral mesh which defines the
            geometry of the sample. (At instantiation it is assumed that the sample and lab coordinate systems
            are aligned.)
        orientation (:obj:`numpy array`): Per element orientation matrices (sometimes known by the capital letter U),
            (``shape=(N,3,3)``) or (``shape=(3,3)``) if the orientation is the same for all elements. The orientation
            matrix maps from crystal coordinates to sample coordinates.
        strain (:obj:`numpy array`): Per element (Green-Lagrange) strain tensor, in lab coordinates, (``shape=(N,3,3)``)
            or (``shape=(3,3)``) if the strain is the same for all elements elements.
        phases (:obj:`xrd_simulator.phase.Phase` or :obj:`list` of :obj:`xrd_simulator.phase.Phase`): Phase of the
            polycrystal, or for multiphase samples, a list of all phases present in the polycrystal.
        element_phase_map (:obj:`numpy array`): Index of phase that elements belong to such that phases[element_phase_map[i]]
            gives the xrd_simulator.phase.Phase object of element number i. None if the sample is composed of a single phase.
            (Defaults to None)

    Attributes:
        mesh_lab (:obj:`xrd_simulator.mesh.TetraMesh`): Object representing a tetrahedral mesh which defines the
            geometry of the sample in a fixed lab frame coordinate system. This quantity is updated when the sample transforms.
        mesh_sample (:obj:`xrd_simulator.mesh.TetraMesh`): Object representing a tetrahedral mesh which defines the
            geometry of the sample in a sample coordinate system. This quantity is not updated when the sample transforms.
        orientation_lab (:obj:`numpy array`): Per element orientation matrices mapping from the crystal to the lab coordinate
            system, this quantity is updated when the sample transforms. (``shape=(N,3,3)``).
        orientation_sample (:obj:`numpy array`): Per element orientation matrices mapping from the crystal to the sample
            coordinate system.,  this quantity is not updated when the sample transforms. (``shape=(N,3,3)``).
        strain_lab (:obj:`numpy array`): Per element (Green-Lagrange) strain tensor in a fixed lab frame coordinate
            system, this quantity is updated when the sample transforms. (``shape=(N,3,3)``).
        strain_sample (:obj:`numpy array`): Per element (Green-Lagrange) strain tensor in a sample coordinate
            system., this quantity is not updated when the sample transforms. (``shape=(N,3,3)``).
        phases (:obj:`list` of :obj:`xrd_simulator.phase.Phase`): List of all unique phases present in the polycrystal.
        element_phase_map (:obj:`numpy array`): Index of phase that elements belong to such that phases[element_phase_map[i]]
            gives the xrd_simulator.phase.Phase object of element number i.

    """

    def __init__(
            self,
            mesh,
            orientation,
            strain,
            phases,
            element_phase_map=None):

        self.orientation_lab = self._instantiate_orientation(orientation, mesh)
        self.strain_lab = self._instantiate_strain(strain, mesh)
        self.element_phase_map, self.phases = self._instantiate_phase(phases, element_phase_map, mesh)
        self._eB = self._instantiate_eB(self.orientation_lab, self.strain_lab, self.phases, self.element_phase_map, mesh)

        # Assuming sample and lab frames to be aligned at instantiation.
        self.mesh_lab = copy.deepcopy(mesh)
        self.mesh_sample = copy.deepcopy(mesh)
        self.strain_sample = np.copy(self.strain_lab)
        self.orientation_sample = np.copy(self.orientation_lab)

    def diffract(
                self,
                beam,
                detector,
                rigid_body_motion,
                min_bragg_angle=0,
                max_bragg_angle=None,
                verbose=False,
                number_of_processes=1,
                number_of_frames=1 
                ):
        """Compute diffraction from the rotating and translating polycrystal while illuminated by an xray beam.

        The xray beam interacts with the polycrystal producing scattering units which are stored in a detector frame.
        The scattering units may be rendered as pixelated patterns on the detector by using a detector rendering
        option.

        Args:
            beam (:obj:`xrd_simulator.beam.Beam`): Object representing a monochromatic beam of xrays.
            detector (:obj:`xrd_simulator.detector.Detector`): Object representing a flat rectangular detector.
            rigid_body_motion (:obj:`xrd_simulator.motion.RigidBodyMotion`): Rigid body motion object describing the
                polycrystal transformation as a function of time on the domain (time=[0,1]) over which diffraction is to be
                computed.
            min_bragg_angle (:obj:`float`): Minimum Bragg angle (radians) below which to not compute diffraction.
                Defaults to 0.
            max_bragg_angle (:obj:`float`): Maximum Bragg angle (radians) after which to not compute diffraction. By default
                the max_bragg_angle is approximated by wrapping the detector corners in a cone with apex at the sample-beam
                intersection centroid for time=0 in the rigid_body_motion.
            verbose (:obj:`bool`): Prints progress. Defaults to True.
            number_of_processes (:obj:`int`): Optional keyword specifying the number of desired processes to use for diffraction
                computation. Defaults to 1, i.e a single processes.
            number_of_frames (:obj:`int`): Optional keyword specifying the number of desired temporally equidistantly spaced frames
                to be collected. Defaults to 1, which means that the detector reads diffraction during the full rigid body
                motion and integrates out the signal to a single frame. The number_of_frames keyword primarily allows for single 
                rotation axis full 180 dgrs or 360 dgrs sample rotation data sets to be computed rapidly and convinently. 

        """
        if verbose and number_of_processes!=1:
            raise NotImplemented('Verbose mode is not implemented for multiprocesses computations')

        min_bragg_angle, max_bragg_angle = self._get_bragg_angle_bounds(
            detector, beam, min_bragg_angle, max_bragg_angle)

        for phase in self.phases:
            with utils._verbose_manager(verbose):
                phase.setup_diffracting_planes(
                    beam.wavelength,
                    min_bragg_angle,
                    max_bragg_angle)

        espherecentroids  = np.array_split(self.mesh_lab.espherecentroids, number_of_processes, axis=0)
        eradius           = np.array_split(self.mesh_lab.eradius,  number_of_processes, axis=0)
        orientation_lab   = np.array_split(self.orientation_lab, number_of_processes, axis=0)
        eB                = np.array_split(self._eB,  number_of_processes, axis=0)
        element_phase_map = np.array_split(self.element_phase_map,  number_of_processes, axis=0)
        enod              = np.array_split(self.mesh_lab.enod,  number_of_processes, axis=0)

        args = []
        for i in range(number_of_processes):
            ecoord = np.zeros((enod[i].shape[0], 4, 3))
            for k,en in enumerate(enod[i]):
                ecoord[k,:,:] = self.mesh_lab.coord[en]
            args.append( {
                        'beam': beam ,
                        'detector': detector,
                        'rigid_body_motion': rigid_body_motion ,
                        'phases': self.phases,
                        'espherecentroids': espherecentroids[i],
                        'eradius': eradius[i],
                        'orientation_lab': orientation_lab[i],
                        'eB': eB[i],
                        'element_phase_map': element_phase_map[i],
                        'ecoord': ecoord,
                        'verbose':verbose
                        } )

        if number_of_processes == 1:
            all_scattering_units = _diffract(args[0])
        else:
            with Pool(number_of_processes) as p:
                scattering_units = p.map( _diffract, args )
            all_scattering_units = []
            for su in scattering_units:
                all_scattering_units.extend(su)
        
        if number_of_frames==1:
            detector.frames.append(all_scattering_units)
        else:
            #TODO: unit test
            all_scattering_units.sort(key=lambda scattering_unit: scattering_unit.time, reverse=True)
            dt = 1./number_of_frames
            start_time_of_current_frame = 0
            while(start_time_of_current_frame <= 1 - 1e-8):
                frame = []
                while( len(all_scattering_units)>0 and all_scattering_units[-1].time < start_time_of_current_frame + dt):
                    frame.append( all_scattering_units.pop() )
                start_time_of_current_frame += dt
                detector.frames.append( frame )
            assert len(all_scattering_units)==0

    def transform(self, rigid_body_motion, time):
        """Transform the polycrystal by performing a rigid body motion (translation + rotation)

        This function will update the polycrystal mesh (update in lab frame) with any dependent quantities,
        such as face normals etc. Likewise, it will update the per element crystal orientation
        matrices (U) as well as the lab frame description of strain tensors.

        Args:
            rigid_body_motion (:obj:`xrd_simulator.motion.RigidBodyMotion`): Rigid body motion object describing the
                polycrystal transformation as a function of time on the domain time=[0,1].
            time (:obj:`float`): Time between [0,1] at which to call the rigid body motion.

        """

        self.mesh_lab.update(rigid_body_motion, time)

        Rot_mat = rigid_body_motion.rotator.get_rotation_matrix(
            rigid_body_motion.rotation_angle * time)

        self.orientation_lab = np.dot(Rot_mat, self.orientation_lab).swapaxes(0,1)
        self.strain_lab = np.dot( np.dot(Rot_mat, self.strain_lab), Rot_mat.T ).swapaxes(0,1)

    def save(self, path, save_mesh_as_xdmf=True):
        """Save polycrystal to disc (via pickling).

        Args:
            path (:obj:`str`): File path at which to save, ending with the desired filename.
            save_mesh_as_xdmf (:obj:`bool`): If true, saves the polycrystal mesh with associated
                strains and crystal orientations as a .xdmf for visualization (sample coordinates).
                The results can be vizualised with for instance paraview (https://www.paraview.org/).
                The resulting data fields of the mesh data are the 6 unique components of the strain
                tensor (in sample coordinates) and the 3 Bunge Euler angles (Bunge, H. J. (1982). Texture
                Analysis in Materials Science. London: Butterworths.). Additionally a single field specifying
                the material phases of the sample will be saved.

        """
        if not path.endswith(".pc"):
            pickle_path = path + ".pc"
            xdmf_path = path + ".xdmf"
        else:
            pickle_path = path
            xdmf_path = path.split('.')[0]+ ".xdmf"
        with open(pickle_path, "wb") as f:
            dill.dump(self, f, dill.HIGHEST_PROTOCOL)
        if save_mesh_as_xdmf:
            element_data = {}
            element_data['Strain Tensor Component xx'] = self.strain_sample[:, 0, 0]
            element_data['Strain Tensor Component yy'] = self.strain_sample[:, 1, 1]
            element_data['Strain Tensor Component zz'] = self.strain_sample[:, 2, 2]
            element_data['Strain Tensor Component xy'] = self.strain_sample[:, 0, 1]
            element_data['Strain Tensor Component xz'] = self.strain_sample[:, 0, 2]
            element_data['Strain Tensor Component yz'] = self.strain_sample[:, 1, 2]
            element_data['Bunge Euler Angle phi_1 [degrees]'] = []
            element_data['Bunge Euler Angle Phi [degrees]'] = []
            element_data['Bunge Euler Angle phi_2 [degrees]'] = []
            element_data['Misorientation from mean orientation [degrees]'] = []

            misorientations = utils.get_misorientations(self.orientation_sample)

            for U, misorientation in zip(self.orientation_sample, misorientations):
                phi_1, PHI, phi_2 = tools.u_to_euler(U)
                element_data['Bunge Euler Angle phi_1 [degrees]'].append(np.degrees(phi_1))
                element_data['Bunge Euler Angle Phi [degrees]'].append(np.degrees(PHI))
                element_data['Bunge Euler Angle phi_2 [degrees]'].append(np.degrees(phi_2))

                element_data['Misorientation from mean orientation [degrees]'].append(np.degrees(misorientation))

            element_data['Material Phase Index'] = self.element_phase_map
            self.mesh_sample.save(xdmf_path, element_data=element_data)

    @classmethod
    def load(cls, path):
        """Load polycrystal from disc (via pickling).

        Args:
            path (:obj:`str`): File path at which to load, ending with the desired filename.

        .. warning::
            This function will unpickle data from the provied path. The pickle module
            is not intended to be secure against erroneous or maliciously constructed data.
            Never unpickle data received from an untrusted or unauthenticated source.

        """
        if not path.endswith(".pc"):
            raise ValueError("The loaded polycrystal file must end with .pc")
        with open(path, 'rb') as f:
            return dill.load(f)

    def _instantiate_orientation(self, orientation, mesh):
        """Instantiate the orientations using for smart multi shape handling.

        """
        if orientation.shape==(3,3):
            orientation_lab = np.repeat(
                orientation.reshape(1, 3, 3), mesh.number_of_elements, axis=0)
        elif orientation.shape==(mesh.number_of_elements,3,3):
            orientation_lab = np.copy(orientation)
        else:
            raise ValueError("orientation input is of incompatible shape")
        return orientation_lab

    def _instantiate_strain(self, strain, mesh):
        """Instantiate the strain using for smart multi shape handling.

        """
        if strain.shape==(3,3):
            strain_lab = np.repeat(strain.reshape(1, 3, 3), mesh.number_of_elements, axis=0)
        elif strain.shape==(mesh.number_of_elements,3,3):
            strain_lab = np.copy(strain)
        else:
            raise ValueError("strain input is of incompatible shape")
        return strain_lab

    def _instantiate_phase(self, phases, element_phase_map, mesh):
        """Instantiate the phases using for smart multi shape handling.

        """
        if not isinstance(phases, list):
            phases = [phases]
        if element_phase_map is None:
            if len(phases)>1:
                raise ValueError("element_phase_map not set for multiphase polycrystal")
            element_phase_map = np.zeros((mesh.number_of_elements,), dtype=int)
        return element_phase_map, phases

    def _instantiate_eB(self, orientation_lab, strain_lab, phases, element_phase_map, mesh):
        """Compute per element 3x3 B matrices that map hkl (Miller) values to crystal coordinates.

            (These are upper triangular matrices such that
                G_s = U * B G_hkl
            where G_hkl = [h,k,l] lattice plane miller indices and G_s is the sample frame diffraction vectors.
            and U are the crystal element orientation matrices.)

        """
        _eB = np.zeros((mesh.number_of_elements, 3, 3))
        for i in range(mesh.number_of_elements):
            _eB[i,:,:] = utils.lab_strain_to_B_matrix(strain_lab[i,:,:],
                                                      orientation_lab[i,:,:],
                                                      phases[element_phase_map[i]].unit_cell)
        return _eB

    def _get_bragg_angle_bounds(
            self,
            detector,
            beam,
            min_bragg_angle,
            max_bragg_angle):
        """Compute a maximum Bragg angle cut of based on the beam sample interection region centroid and detector corners.

        If the beam graces or misses the sample, the sample centroid is used.
        """
        if max_bragg_angle is None:
            mesh_nodes_contained_by_beam = self.mesh_lab.coord[ beam.contains(self.mesh_lab.coord.T), : ]
            if mesh_nodes_contained_by_beam.shape[0] != 0:
                source_point = np.mean(mesh_nodes_contained_by_beam, axis=0)
            else:
                source_point = self.mesh_lab.centroid
            max_bragg_angle = detector.get_wrapping_cone(
                beam.wave_vector, source_point)
        assert min_bragg_angle >= 0, "min_bragg_angle must be greater or equal than zero"
        assert max_bragg_angle > min_bragg_angle, "max_bragg_angle "+str(np.degrees(max_bragg_angle))+"dgrs must be greater than min_bragg_angle "+str(np.degrees(min_bragg_angle))+"dgrs" 
        return min_bragg_angle, max_bragg_angle
