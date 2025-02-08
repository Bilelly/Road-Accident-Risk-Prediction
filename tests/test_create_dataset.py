from src.prediction_profils_accidents_graves.create_dataset import create_dataset


def test_create_dataset_contains_required_columns():
    # Given
    required_columns = [
        # From CARACTERISTIQUES table
        "numero_accident",
        "jour_accident",
        "mois_accident",
        "annee_accident",
        "heure_accident",
        "conditions_lumieres",
        "departement",
        "commune",
        "localisation",
        "type_intersection",
        "conditions_atmospheriques",
        "type_collision",
        "adresse",
        "latitude",
        "longitude",
        # From LIEUX table
        "categorie_route",
        "numero_route",
        "indice_route",
        "lettre_route",
        "regime_circulation",
        "nombre_voies",
        "presence_voie_reservee",
        "profil_route",
        "numero_pr",
        "distance_pr",
        "tracage_route",
        "lartpc",
        "larrout",
        "etat_surface",
        "infrastructure",
        "situation_accident",
        "vitesse_max_autorisee",
        # From VEHICULES table
        "identifiant_vehicule",
        "numero_vehicule",
        "sens_circulation",
        "categorie_vehicule",
        "obstacle_fixe_heurte",
        "obstacle_mobile_heurte",
        "point_choc_initial",
        "manoeuvre_avant_accident",
        "type_motorisation",
        "nombre_occupants_tc",
        # From USAGERS table
        "identifiant_usager",
        "place_occupant",
        "categorie_usager",
        "gravite_blessure",
        "sexe_usager",
        "annee_naissance",
        "motif_deplacement",
        "equipement_securite_1",
        "equipement_securite_2",
        "equipement_securite_3",
        "localisation_pieton",
        "action_pieton",
        "etat_pieton",
    ]

    # When
    df = create_dataset()

    # Then
    for column in required_columns:
        assert column in df.columns, f"Column {column} is missing from the dataset"


def test_create_dataset_contains_data_for_all_years():
    # Given
    expected_years = {2020, 2021, 2022, 2023}

    # When
    df = create_dataset()

    # Then
    actual_years = set(df["annee_accident"].astype(int).unique())
    assert actual_years == expected_years, f"Expected years {expected_years}, but got {actual_years}"
