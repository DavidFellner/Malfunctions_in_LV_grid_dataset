import pflib.pf as pf
import pandas as pd
import numpy as np
import os
import importlib
from experiment_config import experiment_path, chosen_experiment

spec = importlib.util.spec_from_file_location(chosen_experiment, experiment_path)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)


def define_PV_controls(app):
    '''
    define cos(phi)/Q(P) control for PVs
    '''

    # Get folder where to create new QP char object
    o_QPCurves_IntPrjfolder = app.GetProjectFolder('qpc')

    # Clear QP char folder
    for o in o_QPCurves_IntPrjfolder.GetContents():
        o.Delete()

    # Clear Capability Curve Folder (for Q and P limits)
    o_QlimCurve_IntPrjfolder = app.GetProjectFolder('mvar')
    for o in o_QlimCurve_IntPrjfolder.GetContents():
        o.Delete()

    # Create cosphi(P) char object and set attributes
    o_IntcosphiPcurve = o_QPCurves_IntPrjfolder.CreateObject('IntQpcurve', 'QP acting as cosphi(P) char')
    o_IntcosphiPcurve.SetAttribute('inputmod', 1)
    o_IntcosphiPcurve.SetAttribute('Ppu',
                                   [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13,
                                    0.14, 0.15,
                                    0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29,
                                    0.3, 0.31,
                                    0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45,
                                    0.46,
                                    0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6,
                                    0.61, 0.62,
                                    0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76,
                                    0.77,
                                    0.78, 0.79, 0.8, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9, 0.91,
                                    0.92, 0.93,
                                    0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1
                                    ])
    o_IntcosphiPcurve.SetAttribute('Qpu',
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                    0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0633406, 0.08971208,
                                    0.11004031, 0.12725592, 0.14249228, 0.15632983, 0.1691129, 0.18106551, 0.19234309,
                                    0.20305866, 0.21329743, 0.22312553, 0.23259549, 0.24174985, 0.25062362, 0.25924607,
                                    0.26764189, 0.2758322, 0.28383518, 0.29166667, 0.2993405, 0.3068689, 0.31426269,
                                    0.32153154,
                                    0.32868411, 0.33572819, 0.34267085, 0.34951849, 0.35627693, 0.36295153, 0.36954718,
                                    0.37606838, 0.38251928, 0.38890373, 0.39522529, 0.40148728, 0.40769277, 0.41384466,
                                    0.41994564, 0.42599822, 0.43200477, 0.43796754, 0.44388861, 0.44976996, 0.45561346,
                                    0.46142089, 0.46719391, 0.47293413, 0.47864305, 0.4843221])

    # Create Q(P) char object and set attributes
    o_IntQpcurve = o_QPCurves_IntPrjfolder.CreateObject('IntQpcurve', 'General PQ char')
    o_IntQpcurve.SetAttribute('inputmod', 1)
    o_IntQpcurve.SetAttribute('Ppu', [0, 0.5, 1])
    o_IntQpcurve.SetAttribute('Qpu', [0, 0, -0.338])

    # Create disfunctional Q(P) char object and set attributes
    o_brokenIntQpcurve = o_QPCurves_IntPrjfolder.CreateObject('IntQpcurve', 'Broken PQ char')
    o_brokenIntQpcurve.SetAttribute('inputmod', 1)
    o_brokenIntQpcurve.SetAttribute('Ppu', [0, 0.5, 1])
    o_brokenIntQpcurve.SetAttribute('Qpu', [0, 0, 0])

    # Create wrong Q(P) char object and set attributes (inverse curve)
    o_wrongIntcosphiPcurve = o_QPCurves_IntPrjfolder.CreateObject('IntQpcurve', 'Wrong QP acting as cosphi(P) char')
    o_wrongIntcosphiPcurve.SetAttribute('inputmod', 1)
    o_wrongIntcosphiPcurve.SetAttribute('Ppu',
                                        [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13,
                                         0.14, 0.15,
                                         0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28,
                                         0.29,
                                         0.3, 0.31,
                                         0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44,
                                         0.45,
                                         0.46,
                                         0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59,
                                         0.6,
                                         0.61, 0.62,
                                         0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.74, 0.75,
                                         0.76,
                                         0.77,
                                         0.78, 0.79, 0.8, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9,
                                         0.91,
                                         0.92, 0.93,
                                         0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1
                                         ])
    o_wrongIntcosphiPcurve.SetAttribute('Qpu',
                                        list(-np.array(
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                             0, 0, 0,
                                             0, 0, 0,
                                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0633406,
                                             0.08971208,
                                             0.11004031, 0.12725592, 0.14249228, 0.15632983, 0.1691129, 0.18106551,
                                             0.19234309,
                                             0.20305866, 0.21329743, 0.22312553, 0.23259549, 0.24174985, 0.25062362,
                                             0.25924607,
                                             0.26764189, 0.2758322, 0.28383518, 0.29166667, 0.2993405, 0.3068689,
                                             0.31426269,
                                             0.32153154,
                                             0.32868411, 0.33572819, 0.34267085, 0.34951849, 0.35627693, 0.36295153,
                                             0.36954718,
                                             0.37606838, 0.38251928, 0.38890373, 0.39522529, 0.40148728, 0.40769277,
                                             0.41384466,
                                             0.41994564, 0.42599822, 0.43200477, 0.43796754, 0.44388861, 0.44976996,
                                             0.45561346,
                                             0.46142089, 0.46719391, 0.47293413, 0.47864305, 0.4843221])))

    return o_IntcosphiPcurve, o_IntQpcurve, o_brokenIntQpcurve, o_wrongIntcosphiPcurve


def place_PVs(app, o_ElmNet, o_ChaTime, PV_apparent_power):
    '''
    Place photvoltaics next to every load, assign control/capability curve &  charactersitic and scale their output
    to the consumption of the load they are attached to so as it yields about the yearly consumption of the load
    '''

    curves = define_PV_controls(app)

    o_QlimCurve_IntPrjfolder = app.GetProjectFolder('mvar')
    o_IntQlim = o_QlimCurve_IntPrjfolder.SearchObject('Capability Curve')
    if o_IntQlim is None or o_IntQlim.loc_name != 'Capability Curve':
        o_IntQlim = o_QlimCurve_IntPrjfolder.CreateObject('IntQlim', 'Capability Curve')
        o_IntQlim.SetAttribute('cap_Ppu', [0, 1])
        o_IntQlim.SetAttribute('cap_Qmnpu',
                               [0, -0.436])  # operational limits following the standard; max cosphi = 0.9
        o_IntQlim.SetAttribute('cap_Qmxpu', [0, 0.436])
        o_IntQlim.SetAttribute('inputmod', 1)

    for o_ElmLod in app.GetCalcRelevantObjects('.ElmLod'):
        load_cubicle = o_ElmLod.bus1  # elements are connected to terminals via cubicles in powerfactory
        o_ElmTerm = load_cubicle.cterm

        o_StaCubic = o_ElmTerm.CreateObject('StaCubic',
                                            'Cubicle_' + o_ElmLod.loc_name.split(' ')[0] + ' SGen ' +
                                            o_ElmLod.loc_name.split(' ')[2])
        o_Elm = o_ElmNet.CreateObject('ElmGenstat',
                                      o_ElmLod.loc_name.split(' ')[0] + ' SGen ' + o_ElmLod.loc_name.split(' ')[2])
        o_Elm.SetAttribute('bus1', o_StaCubic)
        o_Elm.SetAttribute('sgn', PV_apparent_power)
        o_Elm.pgini = o_Elm.sgn * 0.9 * (o_ElmLod.plini / 0.004)
        o_Elm.cCategory = 'Photovoltaic'
        pf.set_referenced_characteristics(o_Elm, 'pgini', o_ChaTime)  # set characteristic for inserted PV

        o_Elm.outserv = 1  # deactivate all PVs at first and then activate random ones during simulation
        o_Elm.SetAttribute('av_mode', 'qpchar')  # Control activated
        o_Elm.SetAttribute('pQPcurve', curves[config.control_curve_choice])  # Control assigned

        o_Elm.SetAttribute('Pmax_ucPU', 1)  # set the operational limits for the PV
        o_Elm.SetAttribute('pQlimType', o_IntQlim)

    return curves


def utf8_complaint_naming(o_ElmNet):
    '''
    Check for UTF-8 correct naming of elements (important for reading the result file into a dataframe)
    '''

    l_objects = o_ElmNet.GetContents(1)  # get all network elements
    not_utf = []
    for o in l_objects:
        string = o.loc_name
        if len(string.encode('utf-8')) == len(string):  # check if name is UTF-8
            # print ("string is UTF-8, length %d bytes" % len(string))
            continue
        else:
            print("string is not UTF-8")
            count = 0
            not_utf.append(o)
            for l in string:
                if len(l.encode('utf-8')) > 1:  # replace not UTF-8 character with _
                    new = string.replace(l, '_', count)
                    string = new
                count += 1
            o.loc_name = string
    print('%d element names changed to match UTF-8 format' % len(not_utf))

    return 0


def prepare_grid(app, file, o_ElmNet):
    # set path for load and generation profiles
    char_folder = app.GetProjectFolder('chars')
    chars = list(
        pd.read_csv(os.path.join(config.data_folder, file, 'LoadProfile.csv'), sep=';', index_col='time').columns) \
            + list(
        pd.read_csv(os.path.join(config.data_folder, file, 'RESProfile.csv'), sep=';', index_col='time').columns)
    for char_name in chars:
        char = char_folder.SearchObject(char_name + '.ChaTime')
        if os.name == 'nt':
            init_f_name_ending = char.f_name.split('\\')[-1]
        else:
            init_f_name_ending = char.f_name.split('/')[-1]
        char.f_name = os.path.join(config.data_folder, file, init_f_name_ending)

    for o_ElmLod in app.GetCalcRelevantObjects('.ElmLod'):  # gas to be done like this to active profiles
        o_ChaTime = pf.get_referenced_characteristics(o_ElmLod, 'plini')[
            0]  # get P characteristic (profile) from load
        pf.set_referenced_characteristics(o_ElmLod, 'plini', o_ChaTime)  # set characteristic for inserted PV
        o_ChaTime = pf.get_referenced_characteristics(o_ElmLod, 'qlini')[  # same for Q (reactive Power)
            0]
        pf.set_referenced_characteristics(o_ElmLod, 'qlini', o_ChaTime)

    # deactivate storages in grid and count PVs for later use
    for o_ElmGenstat in app.GetCalcRelevantObjects('.ElmGenstat'):
        if o_ElmGenstat.cCategory == 'Storage':
            o_ElmGenstat.outserv = 1
        elif o_ElmGenstat.cCategory == 'Photovoltaic':
            o_ChaTime = pf.get_referenced_characteristics(o_ElmGenstat, 'pgini')[
                0]  # get characteristic (profile) from original PV
            PV_apparent_power = o_ElmGenstat.sgn
            o_ElmGenstat.Delete()  # delete PV in order to make space for own setup
            if len(pf.get_referenced_characteristics(o_ElmGenstat, 'pgini')) > 1:
                print('More than one PV profile found; consider which one to choose (default: first one found chosen)')

    curves = place_PVs(app, o_ElmNet, o_ChaTime, PV_apparent_power)
    utf8_complaint_naming(o_ElmNet)  # check if element names are UTF8 compliant and rename if not

    return curves
