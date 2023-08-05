
"""Module computing the best coefficient of a QC automatically"""

# Required imports
from pybsrnqc import open_data as od
from pybsrnqc import qc_functions as qcf
from pybsrnqc import plot_limits as pl
from pybsrnqc import coef_study as cs

import importlib.resources
import json


# Coefficients initialisation
# Get data conf from JSON file
with importlib.resources.path("pybsrnqc", "qcrad_conf.json") as data_path:
    with open(data_path, 'r') as f:
        dic_coefs = json.load(f)


def compute(path=None, level='level_2', bw_sel=None):

    # Choosing the QC
    QC = input('What QC do you want to study ? \n Enter QCn where n is the number of the QC chosen \n Answer : ')
    level = input('What level do you want to study ? \n Enter level_1 for 1rst level \n Enter level_2 for 2nd level \n Answer :')

    if QC == 'QC1':
        QC = qcf.QC1()
    if QC == 'QC2':
        QC = qcf.QC2()
    if QC == 'QC3':
        QC = qcf.QC3()
    if QC == 'QC5':
        QC = qcf.QC5()
    if QC == 'QC10':
        QC = qcf.QC10()

    # Get datas
    if path is not None:
        df = od.open_all(path=path + '/')
    else:
        df = od.open_all()

    # Calculating kernel density for the dataset
    if QC.name == 'QC3' or QC.name == 'QC10':
        log_kernel, selected = pl.kde_computing(df, QC, select=True, bw_sel=bw_sel)
    else:
        log_kernel = pl.kde_computing(df, QC, bw_sel=bw_sel)

    # Choosing the threshold
    threshold = float(input('Threshold for outliers : '))

    # Nb of coefficients tried
    nb_try = float(input("Number of coefficients tried (200 is ok): "))

    # Field of research
    coef_range = QC.coef_range
    step = (coef_range[1] - coef_range[0]) / nb_try

    if QC.vary == 'downward_avg':
        coef_range_min = QC.coef_range_min
        step_min = (coef_range_min[1] - coef_range_min[0]) / nb_try

    # Finding the best coefficient for a density threshold given
    if QC.vary == 'downward_avg':
        if QC.name == 'QC10':
            df_score, score, df_score_min, score_min = cs.calc_coef(df, log_kernel, QC, threshold, level=level,
                                                                    coef_range=coef_range, coef_range_min=coef_range_min,
                                                                    step=step, step_min=step_min, selected=selected)

        else:
            df_score, score, df_score_min, score_min = cs.calc_coef(df, log_kernel, QC, threshold, level=level,
                                                                    coef_range=coef_range, coef_range_min=coef_range_min,
                                                                    step=step, step_min=step_min)

    elif QC.vary == 'direct_avg':
        df_score, score = cs.calc_coef(df, log_kernel, QC, threshold, level=level, coef_range=coef_range, step=step, selected=selected)
        print('Best coefficient:')
        print(score)
    else:
        df_score, score = cs.calc_coef(df, log_kernel, QC, threshold, level=level, coef_range=coef_range, step=step)
        print('Best coefficient:')
        print(score)

    # In the case there are several best scores
    if score.shape != (1, 5):
        score = score.iloc[0]
    if QC.vary == 'downward_avg':
        score_min = score_min.iloc[0]

    # Charging the new coeff
    if QC.vary == 'downward_avg':
        dic_coefs['COEF'][QC.coefficients[level]] = float(score[QC.coefficients[level]])
        dic_coefs['COEF'][QC.coefficients[level + '_min']] = float(score_min[QC.coefficients[level + '_min']])
    else:
        dic_coefs['COEF'][QC.coefficients[level]] = float(score[QC.coefficients[level]])

    # Plotting the result
    pl.plot_kde(df, log_kernel, QC, dic_coefs, level=level)

    if QC.vary == 'downward_avg':
        return QC.coefficients[level], float(score[QC.coefficients[level]]), QC.coefficients[level + '_min'], float(score_min[QC.coefficients[level + '_min']])
    else:
        return QC.coefficients[level], float(score[QC.coefficients[level]])
