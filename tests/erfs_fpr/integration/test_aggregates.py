# -*- coding: utf-8 -*-

import numpy as np
import pytest

from openfisca_france.france_taxbenefitsystem import FranceTaxBenefitSystem  # type: ignore
from openfisca_france_data import france_data_tax_benefit_system
from openfisca_france_data.erfs_fpr.get_survey_scenario import get_survey_scenario
from openfisca_france_data.aggregates import Aggregates


@pytest.fixture
def tbs() -> FranceTaxBenefitSystem:
    return france_data_tax_benefit_system


def test_erfs_fpr_survey_simulation_aggregates(tbs, year = 2014, rebuild_input_data = False):
    np.seterr(all = "raise")

    survey_scenario = get_survey_scenario(
        tax_benefit_system = tbs,
        baseline_tax_benefit_system = tbs,
        year = year,
        rebuild_input_data = rebuild_input_data,
        )

    aggregates = Aggregates(survey_scenario = survey_scenario)

    assert aggregates.compute_aggregates(use_baseline = True, actual = False)


def test_erfs_fpr_aggregates_reform(tbs, year = 2014, rebuild_input_data = False, reform = "plf2015"):
    """
    test aggregates value with data
    :param year: year of data and simulation to test agregates
    :param reform: optional argument, put an openfisca_france.refoms object, default None
    """
    np.seterr(all = "raise")

    survey_scenario = get_survey_scenario(
        baseline_tax_benefit_system = tbs,
        year = year,
        rebuild_input_data = rebuild_input_data,
        reform = reform,
        )

    aggregates = Aggregates(survey_scenario = survey_scenario)
    assert aggregates.compute_aggregates()
    assert aggregates.compute_difference()
