from typing import Dict, List, Optional, Tuple

from ase.io import read
from ase.io.vasp import write_vasp
from numpy.typing import NDArray
from pymatgen.core import Lattice, Structure
from pymatgen.core.periodic_table import Element
from pymatgen.io.vasp import Poscar
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


def convert_lammps_structure_to_poscar_by_ase(
    lammps_structure_file: str,
    poscar_structure_file: str,
    symbol_of_each_type: Optional[Dict[int, str]] = None,
) -> None:
    """Convert lammps structure file to POSCAR format

    Args:
        lammps_structure_file (str): lammps-data format structure filename
        poscar_structure_file (str): poscar format structure filename
        symbol_of_each_type (Optional[Dict[int, str]], optional): The element symbol
            of each type in original lammps structure. Defaults to None.
    """
    if symbol_of_each_type is None:
        z_of_type = None
    else:
        z_of_type = {}
        for atomic_type in symbol_of_each_type.keys():
            element = Element(symbol_of_each_type[atomic_type])
            z_of_type[atomic_type] = element.Z

    atoms = read(
        lammps_structure_file, format="lammps-data", Z_of_type=z_of_type, style="atomic"
    )
    write_vasp(poscar_structure_file, atoms=atoms, direct=True)


# flake8: noqa: CCR001
def optimize_fractional_coordinates(coords: NDArray) -> List[float]:
    """Optimize fractional coordinates

    Args:
        coords (NDArray): The fractional coordinates of Structure object.

    Returns:
        List[float]: Original object of fractional coordinates.
    """
    n_atom = len(coords)
    new_coords = []
    for i in range(n_atom):
        if i == 0:
            continue

        for j in range(3):
            coords[i][j] -= coords[0][j]
            if coords[i][j] > 1:
                coords[i][j] -= 1
            elif coords[i][j] < 0:
                coords[i][j] += 1
            new_coords.append(float(coords[i][j]))

    return new_coords


def pymat_structure(
    lattice: List[float], coords: List[float], species: List[str]
) -> Structure:
    """Create Pymatgen Structure object

    Args:
        lattice (List[float]): Original object of lattice.
        coords (List[float]): Original object of fractional coordinates.
        species (List[str]): List of specie.

    Returns:
        Structure: Pymatgen Structure object.
    """
    assert (len(coords) % 3) == 0
    n_free_atom = len(coords) // 3

    pymat_lattice = Lattice.from_parameters(
        a=lattice[0],
        b=lattice[1],
        c=lattice[2],
        alpha=lattice[3],
        beta=lattice[4],
        gamma=lattice[5],
    )
    frac_coords = [[0.0, 0.0, 0.0]]
    for i in range(n_free_atom):
        begin = 3 * i
        end = 3 * (i + 1)
        frac_coords.append(coords[begin:end])
    return Structure(pymat_lattice, species, frac_coords)


def extract_optimized_structure(
    structure: Structure,
) -> Tuple[List[float], List[float], List[str]]:
    """Extract original structure object where fractional coordinates is optimized

    Args:
        structure (Structure): Object of structure.

    Returns:
        Tuple[List[float], List[float], List[str]]: Original structure objects.
    """
    lattice = list(structure.lattice.parameters)
    coords = optimize_fractional_coordinates(structure.frac_coords)

    species = []
    for specie in structure.species:
        species.append(str(specie).split()[-1])

    return lattice, coords, species


def refine_cell(
    lattice: List[float], coords: List[float], species: List[str]
) -> Tuple[List[float], List[float], List[str]]:
    """Refine original structure objects

    Args:
        lattice (List[float]): Original object of lattice.
        coords (List[float]): Original object of fractional coordinates.
        species (List[str]): List of specie.

    Returns:
        Tuple[List[float], List[float], List[str]]: Original structure objects.
    """
    structure = pymat_structure(lattice, coords, species)
    analyzer = SpacegroupAnalyzer(structure, symprec=1e-05, angle_tolerance=-1.0)
    refined_structure = analyzer.get_refined_structure()

    return extract_optimized_structure(refined_structure)


def refine_poscar_file(poscar_name: str = "POSCAR") -> None:
    """Refine POSCAR

    Args:
        poscar_name (str, optional): Path to POSCAR. Defaults to "POSCAR".
    """
    # Read POSCAR
    structure = Poscar.from_file(poscar_name).structure
    lattice, coords, species = extract_optimized_structure(structure)

    lattice, coords, species = refine_cell(lattice, coords, species)

    # Write POSCAR
    structure = pymat_structure(lattice, coords, species)
    content = Poscar(structure).get_str(significant_figures=16)
    with open(poscar_name, "w") as f:
        f.write(content)
