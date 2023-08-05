from config.core import config
from pec2_pipeline import titanic_pipeline
from processing.data_manager import load_dataset, save_pipeline
from sklearn.model_selection import train_test_split


def execute_training() -> None:

    """Train the model."""

    # read training data
    data = load_dataset(file_name=config.app_config.data_file, delimiter=";")
    print(data.head())
    # Convert categorical to numerical
    data["sex"].replace(["male", "female"], [1, 0], inplace=True)
    # divide train and test
    X_train, X_test, Y_train, Y_test = train_test_split(
        data[config.model_config.features],
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.model_config.random_state,
    )

    # DataConversionWarning: A column-vector y was passed when a 1d array was expected.
    # Please change the shape of y to (n_samples, ), for example using ravel().
    titanic_pipeline.fit(X_train, Y_train.values.ravel())

    # persist trained model
    save_pipeline(pipeline_to_persist=titanic_pipeline)


if __name__ == "__main__":
    execute_training()
