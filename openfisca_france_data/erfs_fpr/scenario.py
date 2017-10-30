# -*- coding: utf-8 -*-


from openfisca_france_data.surveys import AbstractErfsSurveyScenario

import logging
log = logging.getLogger(__name__)


class ErfsFprSurveyScenario(AbstractErfsSurveyScenario):
    collection = 'openfisca_erfs_fpr'
    used_as_input_variables = [
        'activite',
        'autonomie_financiere',
        'categorie_salarie',
        'chomage_brut',
        'chomage_imposable',
        'contrat_de_travail',
        'cotisation_sociale_mode_recouvrement',
        'date_naissance',
        'effectif_entreprise',
        'f4ba',
        'heures_remunerees_volume',
        'loyer',
        'pensions_alimentaires_percues',
        'rag',
        'retraite_brute',
        'retraite_imposable',
        'ric',
        'rnc',
        'statut_marital',
        'salaire_de_base',
        'statut_occupation_logement',
        'taxe_habitation',
        'zone_apl',
        ]
    # Might be used: hsup
    default_value_by_variable = dict(
        cotisation_sociale_mode_recouvrement = 2,
        # taux_incapacite = .50,
        )
    input_data_survey_prefix = 'openfisca_erfs_fpr_data'
    non_neutralizable_variables = [
        'menage_ordinaire',
        'idfam_original',
        'idfoy_original',
        'idmen_original',
        # 'rempli_obligation_scolaire',
        # 'ressortissant_eee',
        'wprm_init',
        ]

    def __init__(self, year = None):
        assert year is not None
        self.year = year

    @classmethod
    def build_input_data(cls, year = None):
        assert year is not None
        from openfisca_france_data.erfs_fpr.input_data_builder import build
        build(year = year)

    def custom_input_data_frame(self, input_data_frame, **kwargs):
        # input_data_frame['salaire_imposable_pour_inversion'] = input_data_frame.salaire_imposable
        period = kwargs.get('period', None)
        if 'loyer' in input_data_frame:
            input_data_frame['loyer'] = 12 * input_data_frame.loyer

        input_data_frame.loc[
            input_data_frame.categorie_salarie.isin(range(2, 7)),
            'categorie_salarie'
            ] = 1

        for variable in ['quifam', 'quifoy', 'quimen']:
            log.debug(input_data_frame[variable].value_counts(dropna = False))

        input_data_frame['rpns'] = input_data_frame.rnc + input_data_frame.rag + input_data_frame.ric
        input_data_frame['rpns_individu'] = input_data_frame.rnc + input_data_frame.rag + input_data_frame.ric

        variables_revenus_independants = [
            'ric',
            'rag',
            'rnc',
            ]

        for variable in variables_revenus_independants:
            input_data_frame[variable] = 0

        if period.unit == 'month' and period.size == 12:
            # Il faut mettre des variables mensualisées !
            variables_annuelles = [
                'rpns',
                'rpns_individu',
                ]
            for variable in variables_annuelles:
                if variable in input_data_frame.columns:
                    input_data_frame[variable] = (
                        input_data_frame[variable] / 12) * (
                        input_data_frame[variable] >= 0
                        )
