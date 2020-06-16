'''
Tests of djia_npp_bokey.py module

Three main tests:
* make sure that running the module as a script python djia_npp_bokey.py
  results in a saved html file and two csv data files in the correct
  directories
* data files are created with both download_from_internet==True and
  download_from_internet==False.
'''

import pytest
import datetime as dt
# import os
# import pathlib
# import runpy
# import numpy as np
# import matplotlib.image as mpimg
import djia_npp_bokeh as djia

# Create function to validate datetime text


def validate(date_text):
    try:
        if date_text != dt.datetime.strptime(
                            date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False


# Test whether running the script of the module results in an html figure and
# two datasets
# def test_html_fig_script():
#     script = pathlib.Path(__file__, '..',
#                           'scripts').resolve().glob('djia_npp_bokeh.py')
#     runpy.run_path(script)
#     assert fig

# Test that djia_npp() function returns html figure and valid string and saves
# html figure file and two csv files.
@pytest.mark.parametrize('frwd_mths_main', [6])
@pytest.mark.parametrize('bkwd_mths_main', [1])
@pytest.mark.parametrize('frwd_mths_max', [12])
@pytest.mark.parametrize('bkwd_mths_max', [4])
@pytest.mark.parametrize('djia_end_date', ['today', '2020-06-09'])
@pytest.mark.parametrize('download_from_internet', [True, False])
@pytest.mark.parametrize('html_show', [False])
@pytest.mark.parametrize('matplotlib', [False])
def test_html_fig(frwd_mths_main, bkwd_mths_main, frwd_mths_max, bkwd_mths_max,
                  djia_end_date, download_from_internet, html_show,
                  matplotlib):
    # The case when djia_end_date == 'today' and download_from_internet ==
    # False must be skipped because we don't have the data saved for every date
    if djia_end_date == 'today' and not download_from_internet:
        pytest.skip('Invalid case')
        assert True
    else:
        fig, end_date_str = djia.djia_npp(
            frwd_mths_main=frwd_mths_main, bkwd_mths_main=bkwd_mths_main,
            frwd_mths_max=frwd_mths_max, bkwd_mths_max=bkwd_mths_max,
            djia_end_date=djia_end_date,
            download_from_internet=download_from_internet,
            html_show=html_show, matplotlib=matplotlib)
        assert fig
        assert validate(end_date_str)
    # assert html file exists
    # assert djia series csv file exists
    # assert djia ColumnDataSource source DataFrame csv file exists


# # Load in test results and parameters
# CUR_PATH = os.path.abspath(os.path.dirname(__file__))
# base_ss = utils.safe_read_pickle(
#     os.path.join(CUR_PATH, 'test_io_data', 'SS_vars_baseline.pkl'))
# base_tpi = utils.safe_read_pickle(
#     os.path.join(CUR_PATH, 'test_io_data', 'TPI_vars_baseline.pkl'))
# base_params = utils.safe_read_pickle(
#     os.path.join(CUR_PATH, 'test_io_data', 'model_params_baseline.pkl'))
# base_taxfunctions = utils.safe_read_pickle(
#     os.path.join(CUR_PATH, 'test_io_data', 'TxFuncEst_baseline.pkl'))
# reform_ss = utils.safe_read_pickle(
#     os.path.join(CUR_PATH, 'test_io_data', 'SS_vars_reform.pkl'))
# reform_tpi = utils.safe_read_pickle(
#     os.path.join(CUR_PATH, 'test_io_data', 'TPI_vars_reform.pkl'))
# reform_params = utils.safe_read_pickle(
#     os.path.join(CUR_PATH, 'test_io_data', 'model_params_reform.pkl'))
# reform_taxfunctions = utils.safe_read_pickle(
#     os.path.join(CUR_PATH, 'test_io_data', 'TxFuncEst_reform.pkl'))


# test_data = [(base_tpi, base_params, reform_tpi, reform_params,
#               'pct_diff', None, None),
#              (base_tpi, base_params, reform_tpi, reform_params, 'diff',
#               None, None),
#              (base_tpi, base_params, reform_tpi, reform_params, 'cbo',
#               None, None),
#              (base_tpi, base_params, reform_tpi, reform_params,
#               'levels', None, None),
#              (base_tpi, base_params, None, None, 'levels', None, None),
#              (base_tpi, base_params, None, None, 'levels', [2040, 2060],
#               None),
#              (base_tpi, base_params, None, None, 'levels', None,
#               'Test plot title')
#              ]


# @pytest.mark.parametrize(
#     'base_tpi,base_params,reform_tpi,reform_parms,plot_type,' +
#     'vertical_line_years,plot_title',
#     test_data, ids=['Pct Diff', 'Diff', 'CBO', 'Levels w reform',
#                     'Levels w/o reform', 'Vertical line included',
#                     'Plot title included'])
# def test_html_fig_script(frwd_mths_main, bkwd_mths_main, frwd_mths_max,
#                          bkwd_mths_max,
#                          djia_end_date, download_from_internet, html_show,
#                          matplotlib):
#     fig = output_plots.plot_aggregates(
#         base_tpi, base_params, reform_tpi=reform_tpi,
#         reform_params=reform_params, var_list=['Y', 'r'],
#         plot_type=plot_type, num_years_to_plot=20,
#         vertical_line_years=vertical_line_years, plot_title=plot_title)
#     assert fig


# test_data = [(base_tpi, base_params, None, None, None, None),
#              (base_tpi, base_params, reform_tpi, reform_params, None,
#               None),
#              (base_tpi, base_params, reform_tpi, reform_params,
#               [2040, 2060], None),
#              (base_tpi, base_params, None, None, None,
#               'Test plot title')
#              ]


# def test_plot_aggregates_save_fig(tmpdir):
#     path = os.path.join(tmpdir, 'test_plot.png')
#     output_plots.plot_aggregates(
#         base_tpi, base_params, plot_type='levels', path=path)
#     img = mpimg.imread(path)

#     assert isinstance(img, np.ndarray)


# test_data = [(base_tpi, base_params, None, None, None, None, 'levels'),
#              (base_tpi, base_params, reform_tpi, reform_params, None,
#               None, 'levels'),
#              (base_tpi, base_params, reform_tpi, reform_params, None,
#               None, 'diffs'),
#              (base_tpi, base_params, reform_tpi, reform_params,
#               [2040, 2060], None, 'levels'),
#              (base_tpi, base_params, None, None, None,
#               'Test plot title', 'levels')
#              ]


# @pytest.mark.parametrize(
#     'base_tpi,base_params,reform_tpi,reform_params,' +
#     'vertical_line_years,plot_title,plot_type',
#     test_data, ids=['No reform', 'With reform', 'Differences',
#                     'Vertical line included', 'Plot title included'])
# def test_plot_gdp_ratio(base_tpi, base_params, reform_tpi,
#                         reform_params, vertical_line_years, plot_title,
#                         plot_type):
#     fig = output_plots.plot_gdp_ratio(
#         base_tpi, base_params, reform_tpi=reform_tpi,
#         reform_params=reform_params, plot_type=plot_type,
#         vertical_line_years=vertical_line_years, plot_title=plot_title)
#     assert fig


# def test_plot_gdp_ratio_save_fig(tmpdir):
#     path = os.path.join(tmpdir, 'test_plot.png')
#     output_plots.plot_aggregates(
#         base_tpi, base_params, reform_tpi=reform_tpi,
#         reform_params=reform_params, path=path)
#     img = mpimg.imread(path)

#     assert isinstance(img, np.ndarray)


# def test_ability_bar():
#     fig = output_plots.ability_bar(
#         base_tpi, base_params, reform_tpi, reform_params,
#         plot_title=' Test Plot Title')
#     assert fig


# def test_ability_bar_save_fig(tmpdir):
#     path = os.path.join(tmpdir, 'test_plot.png')
#     output_plots.ability_bar(
#         base_tpi, base_params, reform_tpi, reform_params, path=path)
#     img = mpimg.imread(path)

#     assert isinstance(img, np.ndarray)


# def test_ability_bar_ss():
#     fig = output_plots.ability_bar_ss(
#         base_ss, base_params, reform_ss, reform_params,
#         plot_title=' Test Plot Title')
#     assert fig


# @pytest.mark.parametrize(
#     'by_j,plot_data', [(True, False), (False, False), (False, True)],
#     ids=['By j', 'Not by j', 'Plot data'])
# def test_ss_profiles(by_j, plot_data):
#     fig = output_plots.ss_profiles(
#         base_ss, base_params, reform_ss, reform_params, by_j=by_j,
#         plot_data=plot_data, plot_title=' Test Plot Title')
#     assert fig


# def test_ss_profiles_save_fig(tmpdir):
#     path = os.path.join(tmpdir, 'test_plot.png')
#     output_plots.ss_profiles(
#         base_ss, base_params, reform_ss, reform_params, path=path)
#     img = mpimg.imread(path)

#     assert isinstance(img, np.ndarray)


# @pytest.mark.parametrize(
#     'by_j', [True, False], ids=['By j', 'Not by j'])
# def test_tpi_profiles(by_j):
#     fig = output_plots.tpi_profiles(
#         base_tpi, base_params, reform_tpi, reform_params, by_j=by_j,
#         plot_title=' Test Plot Title')
#     assert fig


# test_data = [(base_params, base_ss, None, None, 'levels', None),
#              (base_params, base_ss, reform_params, reform_ss, 'levels',
#               None),
#              (base_params, base_ss, reform_params, reform_ss, 'diff',
#               None),
#              (base_params, base_ss, reform_params, reform_ss,
#               'pct_diff', None),
#              (base_params, base_ss, reform_params, reform_ss,
#               'pct_diff', 'Test Plot Title')
#              ]


# def test_tpi_profiles_save_fig(tmpdir):
#     path = os.path.join(tmpdir, 'test_plot.png')
#     output_plots.tpi_profiles(
#         base_tpi, base_params, reform_tpi, reform_params, path=path)
#     img = mpimg.imread(path)

#     assert isinstance(img, np.ndarray)


# @pytest.mark.parametrize(
#     'base_params,base_ss,reform_params,reform_ss,plot_type,plot_title',
#     test_data, ids=['Levels', 'Levels w/ reform', 'Differences',
#                     'Pct Diffs', 'Plot title included'])
# def test_ss_3Dplot(base_params, base_ss, reform_params, reform_ss,
#                    plot_type, plot_title):
#     fig = output_plots.ss_3Dplot(
#         base_params, base_ss, reform_params=reform_params,
#         reform_ss=reform_ss, plot_type=plot_type, plot_title=plot_title)
#     assert fig


# def test_ss_3Dplot_save_fig(tmpdir):
#     path = os.path.join(tmpdir, 'test_plot.png')
#     output_plots.ss_3Dplot(
#         base_params, base_ss, reform_params=reform_params,
#         reform_ss=reform_ss, path=path)
#     img = mpimg.imread(path)

#     assert isinstance(img, np.ndarray)


# @pytest.mark.parametrize(
#     'base_tpi,base_params,reform_tpi, reform_params,ineq_measure,' +
#     'pctiles,plot_type',
#     [(base_tpi, base_params, None, None, 'gini', None, 'levels'),
#      (base_tpi, base_params, reform_tpi, reform_params, 'gini', None,
#       'levels'),
#      (base_tpi, base_params, reform_tpi, reform_params, 'var_of_logs',
#       None, 'diff'),
#      (base_tpi, base_params, reform_tpi, reform_params, 'pct_ratio',
#       (0.9, 0.1), 'levels'),
#      (base_tpi, base_params, reform_tpi, reform_params, 'top_share',
#       (0.01), 'pct_diff')],
#     ids=['Just baseline', 'Baseline + Reform',
#          'Base + Refore, var logs, diff',
#          'Base + Refore, pct ratios',
#          'Base + Refore, top share, pct diff'])
# def test_inequality_plot(base_tpi, base_params, reform_tpi,
#                          reform_params, ineq_measure, pctiles,
#                          plot_type):
#     fig = output_plots.inequality_plot(
#         base_tpi, base_params, reform_tpi=reform_tpi,
#         reform_params=reform_params, ineq_measure=ineq_measure,
#         pctiles=pctiles, plot_type=plot_type)
#     assert fig


# def test_inequality_plot_save_fig(tmpdir):
#     path = os.path.join(tmpdir, 'test_plot.png')
#     output_plots.inequality_plot(
#         base_tpi, base_params, reform_tpi=reform_tpi,
#         reform_params=reform_params, path=path)
#     img = mpimg.imread(path)

#     assert isinstance(img, np.ndarray)


# def test_plot_all(tmpdir):
#     base_output_path = os.path.join(CUR_PATH, 'test_io_data', 'OUTPUT')
#     reform_output_path = os.path.join(CUR_PATH, 'test_io_data', 'OUTPUT')
#     output_plots.plot_all(base_output_path, reform_output_path, tmpdir)
#     img1 = mpimg.imread(os.path.join(tmpdir, 'MacroAgg_PctChange.png'))
#     img2 = mpimg.imread(os.path.join(
#         tmpdir, 'SSLifecycleProfile_Cons_Reform.png'))
#     img3 = mpimg.imread(os.path.join(
#         tmpdir, 'SSLifecycleProfile_Save_Reform.png'))

#     assert isinstance(img1, np.ndarray)
#     assert isinstance(img2, np.ndarray)
#     assert isinstance(img3, np.ndarray)
