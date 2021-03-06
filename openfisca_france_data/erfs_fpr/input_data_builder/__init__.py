# -*- coding: utf-8 -*-

import logging


#from multipledispatch import dispatch  # type: ignore


from openfisca_france_data.erfs_fpr.input_data_builder import (
    step_01_preprocessing as preprocessing,
    # step_02_imputation_loyer as imputation_loyer,
    step_03_variables_individuelles as variables_individuelles,
    step_04_famille as famille,
    step_05_final as final,
    )

log = logging.getLogger(__name__)


#@dispatch(int)
def build(year: int, export_flattened_df_filepath: str = None) -> None:
    """
    Ici on va nettoyer et formatter les donnés ERFS-FPR, pour les rendre OpenFisca-like
    """

    # Step 01 : la magie de ce qui nous intéresse : le formattage OpenFisca
    #
    # - Formattage des différentes variables
    # - On merge les tables individus / menages
    #
    # Note : c'est ici où on objectivise les hypothèses, step 1
    preprocessing.build_merged_dataframes(year = year)

    # Step 02 : Si on veut calculer les allocations logement, il faut faire le matching avec une autre enquête (ENL)
    #
    # openfisca_survey_collection = SurveyCollection(name = 'openfisca')
    # stata_directory = openfisca_survey_collection.config.get('data', 'stata_directory')
    # stata_file = os.path.join(stata_directory, 'log_men_ERFS.dta')
    # imputation_loyer.merge_imputation_loyer(stata_file = stata_file, year = year)

    # Step 03 : on commence par les variables indivuelles
    variables_individuelles.build_variables_individuelles(year = year)

    # Step 04 : ici on va constituer foyer et famille à partir d'invididu et ménage
    #
    # - On fait individu/ménage pour pouvoir faire des familles (foyers sociaux)
    # - On va faire des suppositions pour faire les familles
    # - On va faire les foyers fiscaux à partir des familles
    # - On va faire de suppositions pour faire les foyers fiscaux
    famille.build_famille(year = year)

    # Affreux ! On injectait tout dans un même DataFrame !!!
    # C'est très moche !
    #
    # On crée une df par entité par période.
    # Elles sont stockées dans un fichier h5
    final.create_input_data_frame(year = year, export_flattened_df_filepath = export_flattened_df_filepath)


if __name__ == '__main__':
    import sys
    import time
    start = time.time()
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    year = 2014
    export_flattened_df_filepath = "./dummy_data.h5"  # Could be disabled with None
    build(year = year, export_flattened_df_filepath = export_flattened_df_filepath)
    # TODO: create_enfants_a_naitre(year = year)

    log.info("Script finished after {}".format(time.time() - start))
    print(time.time() - start)
