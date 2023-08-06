"""Collection of functions for solving time dependent Laue equations for arbitrary rigid body motions.
This module is mainly used internally by the :class:`xrd_simulator.polycrystal.Polycrystal`. However,
for the advanced user, access to these functions may be of interest.
"""
import numpy as np

def get_G(U, B, G_hkl):
    """Compute the diffraction vector

    .. math::
        \\boldsymbol{G} = \\boldsymbol{U}\\boldsymbol{B}\\boldsymbol{G}_{hkl}

    Args:
        U (:obj:`numpy array`) Orientation matrix of ``shape=(3,3)`` (unitary).
        B (:obj:`numpy array`): Reciprocal to grain coordinate mapping matrix of ``shape=(3,3)``.
        G_hkl (:obj:`numpy array`): Miller indices, i.e the h,k,l integers (``shape=(3,n)``).


    Returns:
        G (:obj:`numpy array`): Sample coordinate system diffraction vector. (``shape=(3,n)``)

    """
    return np.dot(np.dot(U, B), G_hkl)


def get_bragg_angle(G, wavelength):
    """Compute a Bragg angle given a diffraction (scattering) vector.

    Args:
        G (:obj:`numpy array`): Sample coordinate system diffraction vector. (``shape=(3,n)``)
        wavelength (:obj:`float`): Photon wavelength in units of angstrom.

    Returns:
        Bragg angles (:obj:`float`): in units of radians. (``shape=(n,)``)

    """
    return np.arcsin(np.linalg.norm(G, axis=0) * wavelength / (4 * np.pi))


def get_sin_theta_and_norm_G(G, wavelength):
    """Compute a Bragg angle given a diffraction (scattering) vector.

    Args:
        G (:obj:`numpy array`): Sample coordinate system diffraction vector.
        wavelength (:obj:`float`): Photon wavelength in units of angstrom.

    Returns:
        sin(Bragg angle) (:obj:`float`): in units of radians and ||G||.

    """
    normG = np.linalg.norm(G, axis=0)
    return normG * wavelength / (4 * np.pi), normG


def find_solutions_to_tangens_half_angle_equation(rho_0, rho_1, rho_2, delta_omega):
    """Find all solutions, :obj:`t`, to the equation (maximum 2 solutions exists)

    .. math::
        \\rho_0 \\cos(t \\Delta \\omega) + \\rho_1 \\sin(t \\Delta \\omega) + \\rho_2 = 0. \\quad\\quad (1)

    by rewriting as

    .. math::
        (\\rho_2 - \\rho_0) s^2 + 2 \\rho_1 s + (\\rho_0 + \\rho_2) = 0. \\quad\\quad (2)

    where

    .. math::
        s = \\tan(t \\Delta \\omega / 2). \\quad\\quad (3)

    and

        .. math:: \\Delta \\omega

    is a rotation angle

    Args:
        \\rho_0,\\rho_1,\\rho_2 (:obj:`float`): Coefficients \\rho_0,\\rho_1 and \\rho_2 of equation (1).
        delta_omega (:obj:`float`): Radians of rotation.

    Returns:
        (:obj:`tuple` of :obj:`numpy.array`): 2 Arrays of solutions of matching shape to input. if no solutions exist on
        an interval the corresponding instances in the solution array holds np.nan values.

    """
    denominator = rho_2 - rho_0
    a = np.divide(rho_1, denominator, out=np.full_like(rho_0, np.nan), where=denominator!=0)
    b = np.divide(rho_0 + rho_2, denominator, out=np.full_like(rho_0, np.nan), where=denominator!=0)
    rootval = a**2 - b
    leadingterm = -a
    rootval[rootval<0] = np.nan
    s1 = leadingterm + np.sqrt(rootval)
    s2 = leadingterm - np.sqrt(rootval)
    t1 = 2 * np.arctan(s1) / delta_omega
    t2 = 2 * np.arctan(s2) / delta_omega
    t1[(t1>1)|(t1<0)]=np.nan
    t2[(t2>1)|(t2<0)]=np.nan
    return t1, t2
