from app.feature_registry_loader import get_all_features


def detect_features(text: str):
    text = text.lower()

    detected = []

    for feature in get_all_features():

        for keyword in feature["keywords"]:

            if keyword in text:
                detected.append(feature["name"])
                break

    return detected


def compose_feature_files(features):
    files = {}

    registry = get_all_features()

    for feature_name in features:

        for feature in registry:

            if feature["name"] == feature_name:
                files.update(
                    feature.get("files", {})
                )

    return files