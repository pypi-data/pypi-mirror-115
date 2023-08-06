'`matflow_abaqus.main.py`'

import numpy as np
from abaqus_parse import materials
from abaqus_parse.parts import generate_compact_tension_specimen_parts
from abaqus_parse.steps import generate_compact_tension_specimen_steps
from abaqus_parse.writers import write_inp
from abaqus_parse.generate_MK_mesh import generate_MK_mesh
from abaqus_parse.save_model_response import save_model_response
from abaqus_parse.compute_forming_limit_curve import compute_forming_limit_curve


from matflow_abaqus import (
    input_mapper,
    output_mapper,
    cli_format_mapper,
    register_output_file,
    func_mapper,
    software_versions,
)


# tells Matflow this function satisfies the requirements of the task
@func_mapper(task='generate_material_models', method='default')
def generate_material_models(materials_list):
    mat_mods = materials.generate_material_models(materials_list)
    out = {
        'material_models': mat_mods
    }
    return out


@func_mapper(task='generate_specimen_parts', method='compact_tension_fracture')
def generate_parts(dimension, mesh_definition,
                   elem_type, size_type, fraction, specimen_material):
    specimen_parts = generate_compact_tension_specimen_parts(
        dimension, mesh_definition, elem_type, size_type, fraction, specimen_material)
    out = {
        'specimen_parts': specimen_parts
    }
    return out


@func_mapper(task='generate_steps', method='compact_tension_steps')
def generate_steps(applied_displacement, number_contours, time_increment_definition):
    compact_tension_steps = generate_compact_tension_specimen_steps(
        applied_displacement, number_contours, time_increment_definition)
    out = {
        'steps': compact_tension_steps
    }
    return out


@cli_format_mapper(input_name="memory", task="simulate_deformation", method="FE")
def memory_formatter(memory):
    return f'memory={memory.replace(" ", "")}'


@func_mapper(task='generate_MK_model', method='default')
def generate_sample(sample_size, inhomogeneity_factor, L_groove, L_slope, material_angle,
                    groove_angle, elastic_modulus, poisson_ratio, density, law,
                    path_plastic_table, mesh_size, bulk_parameters, elem_type,
                    strain_rate, total_time, displacment_BC, time_step,
                    fitted_yield_functions, yield_point_criterion, max_plastic_strain,
                    Nb_el_thickness, num_interval):

    plastic = np.loadtxt(path_plastic_table, comments='%', delimiter=',')
    if not law:
        # Generate law from `fitted_yield_functions` and `yield_point_criterion`:
        if fitted_yield_functions is None or yield_point_criterion is None:
            msg = ('Specify either `law` or both `fitted_yield_functions` and '
                   '`yield_point_criterion`.')
            raise ValueError(msg)

        # Find the matching fitted yield function given the specified yield point
        # criterion:
        YPC_idx = None
        YPC_value_idx = None
        for idx, i in enumerate(fitted_yield_functions['yield_point_criteria']):
            if (
                i['threshold'] == yield_point_criterion['threshold'] and
                i['source'] == yield_point_criterion['source'] and
                yield_point_criterion['value'] in i['values']
            ):
                YPC_idx = idx
                YPC_value_idx = np.where(
                    np.array(i['values']) == yield_point_criterion['value']
                )[0][0]
                break
        if YPC_idx is None:
            msg = (f'Matching yield point criterion could not be found in the fitted '
                   f'yield functions: {yield_point_criterion}.')
            raise ValueError(msg)

        yield_func = None
        for yld_func_i in fitted_yield_functions['fitted_yield_functions']:
            if (
                yld_func_i['YPC_idx'] == YPC_idx and
                yld_func_i['YPC_value_idx'] == YPC_value_idx
            ):
                yield_func = yld_func_i['yield_function']
                break

        if yield_func is None:
            msg = (f'No fitted yield function with the specified yield point criterion '
                   f'could be found: {yield_point_criterion}.')
            raise ValueError(msg)

        law = {
            'type': yield_func['name'],
            'parameters': {
                i: yield_func[i]
                for i in yield_func.keys() if i not in [
                    'equivalent_stress',
                    'exponent',
                    'fit_info',
                ]
            }
        }
        if 'exponent' in yield_func:
            law.update({'power': yield_func['exponent']})

    elif fitted_yield_functions is not None or yield_point_criterion is not None:
        msg = ('Specify either `law` or both `fitted_yield_functions` and '
               '`yield_point_criterion`.')
        raise ValueError(msg)

    FE_input_data = {
        'sample_size': sample_size,
        'inhomogeneity_factor': inhomogeneity_factor,
        'L_groove': L_groove,
        'L_slope': L_slope,
        'material_angle': material_angle,
        'groove_angle': groove_angle,
        'elastic_modulus': elastic_modulus,
        'poisson_ratio': poisson_ratio,
        'density': density,
        'law': law,
        'plastic': plastic,
        'mesh_size': mesh_size,
        'bulk_parameters': bulk_parameters,
        'elem_type': elem_type,
        'strain_rate': strain_rate,
        'total_time': total_time,
        'displacment_BC': displacment_BC,
        'time_step': time_step,
        'max_plastic_strain': max_plastic_strain,
        'Nb_el_thickness': Nb_el_thickness,
        'num_interval': num_interval,
    }
    out = {
        'FE_input_data': FE_input_data
    }
    return out


@input_mapper(input_file='inputs.inp', task='simulate_MK_deformation', method='FE')
def write_MK_inputs_file(path, FE_input_data):
    generate_MK_mesh(path, FE_input_data)


@output_mapper(output_name="model_response", task='simulate_MK_deformation', method='FE')
def generate_model_response(path):
    model_response = save_model_response(path)
    return model_response


@func_mapper(task='find_forming_limit_curve', method='strain_rate_ratio')
def forming_limit_curve(all_model_responses, strain_rate_ratio_threshold,
                        all_displacement_BCs, all_groove_angles):
    FLC = compute_forming_limit_curve(
        all_model_responses,
        strain_rate_ratio_threshold,
        all_displacement_BCs,
        all_groove_angles,
    )
    out = {
        'forming_limit_curve': FLC
    }
    return out


@cli_format_mapper(input_name="memory", task="simulate_MK_deformation", method="FE")
def memory_formatter(memory):
    return f'memory={memory.replace(" ", "")}'
