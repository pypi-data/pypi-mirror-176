import pandas as pd
from config.core import config
from pipeline import genero_pipe
from processing.data_manager import load_dataset, save_pipeline
from sklearn.model_selection import train_test_split


def run_training() -> None:
    """Train the model."""

    # read training data
    data = load_dataset(file_name=config.app_config.training_data_file)
    # divide train and test
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, #features
        Y, #labels
        test_size=0.3, #portion to test
        random_state=0 #seed definition)
    )
    X_train = pd.DataFrame(X_train, columns=["pclass", "name", "sex", "age", "sibsp", "parch", "ticket", "fare","cabin", "embarked"])
    X_test = pd.DataFrame(X_test, columns=["pclass", "name", "sex", "age", "sibsp", "parch", "ticket", "fare","cabin", "embarked"])
    Y_train = pd.DataFrame(Y_train, columns=["survived"])
    Y_test = pd.DataFrame(Y_test, columns=["survived"])

    # DataConversionWarning: A column-vector y was passed when a 1d array was expected.
    # Please change the shape of y to (n_samples, ), for example using ravel().
    genero_pipe.fit(X_train, Y_train.values.ravel())

    # persist trained model
    save_pipeline(pipeline_to_persist=genero_pipe)


if __name__ == "__main__":
    run_training()
