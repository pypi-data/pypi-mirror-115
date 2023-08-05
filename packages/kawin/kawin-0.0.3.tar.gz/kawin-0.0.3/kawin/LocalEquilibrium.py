from pycalphad.core.eqsolver import pointsolve
from pycalphad.core.solver import Solver
from pycalphad.core.composition_set import CompositionSet
from pycalphad.core.utils import unpack_components, instantiate_models
from pycalphad.codegen.callables import build_phase_records
from pycalphad import calculate
import numpy as np

def local_equilibrium(dbf, comps, phases, conds):
    '''
    Local equilibrium calculation
    
    Chemical potential in a miscibility gap will be constant
    This method allows the user to get the free energy at the specified composition
    ignoring possible miscibility gaps

    Parameters
    ----------
    dbf : Database
    comps : list
        List of elements to consider
    phases : list
        List of phases to consider
    conds : dict
        Dictionary of conditions (v.N needs to be included)

    Returns
    -------
    Dataset containing free energy and chemical potential
    '''
    # Broadcasting conditions not supported
    cur_conds = {str(k): float(v) for k, v in conds.items()}
    species = sorted(unpack_components(dbf, comps), key=str)
    state_variables = np.array([cur_conds['N'], cur_conds['P'], cur_conds['T']], dtype=np.float64)
    # Note: filter_phases() not called, so all specified phases must be valid
    models = instantiate_models(dbf, species, phases)
    phase_records = build_phase_records(dbf, species, phases, conds, models,
                                        build_gradients=True, build_hessians=True)
    composition_sets = []

    # Choose a naive starting point for each phase
    # only one composition set per phase is chosen
    # here, we just choose the point with the minimum Gibbs energy
    # mass balance does not have to be preserved at the starting point
    for phase in phases:
        # arbitrary guess
        phase_amt = 1./len(phases)
        # callables are being unnecessarily rebuilt here
        calc_p = calculate(dbf, comps, phase, T=cur_conds['T'], P=cur_conds['P'],
                           pdens=10, model=models, callables=None)
        idx_p = np.argmin(calc_p.GM.values.squeeze())
        compset = CompositionSet(phase_records[phase])
        site_fractions = np.array(calc_p.Y.isel(points=idx_p).values.squeeze())
        compset.update(site_fractions, phase_amt, state_variables)
        composition_sets.append(compset)

    # Calculate a local equilibrium for the specified phases
    solver = Solver()
    result = pointsolve(composition_sets, species, cur_conds, solver)
    return result, composition_sets