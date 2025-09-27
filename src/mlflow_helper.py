"""Helper utilities for MLflow configuration in local runs."""
import os
import mlflow


def configure_mlflow_local(artifact_root: str = None):
    if artifact_root is None:
        artifact_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "artifacts"))
    os.makedirs(artifact_root, exist_ok=True)
    mlflow.set_tracking_uri(f"file://{artifact_root}")
    return mlflow.get_tracking_uri()


if __name__ == '__main__':
    print('MLflow helper module')
