import pandas as pd
import uuid
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score
from accelo_mlops import AcceloClient
from accelo_mlops.utils.errors import ProjectExistsError


# create client
client = AcceloClient(workspace='preview-alpha')
# exit(0)

# create assembly
try:
    client.create_project(name='click-prediction')
except ProjectExistsError as e:
    print(f'PIPELINE: Project Id: {client.project_id}, error message: {str(e)}')


### training pipeline starts
X, y = load_iris(return_X_y=True, as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
clf = RandomForestClassifier(max_depth=2, random_state=0)
clf.fit(X_train, y_train)
preds = clf.predict(X_test)
acc = accuracy_score(preds, y_test)
f1 = f1_score(preds, y_test, average='weighted')
feature_data = pd.DataFrame(X_test)


# register model
model_metadata = {
    'frequency': 'DAILY', 
    'model_type': 'binary_classification',
    'performance_metric': 'f1_score', 
    'model_obj': clf
}
client.register_model(
    project_id=client.project_id,
    model_name='click_prediction_alpha',
    model_version='v2',
    model_metadata=model_metadata,
    model_location='s3://model-artifactory/marketing-team/classification_click_1627899052.pkl',
    owner='research@preview.com',
    last_trained='2021-08-02',
    training_job_name='click_prediction_ml_pipeline',
    label='click',
    total_consumers=7,
    library='sklearn',
    status='active'
)


# setting id col for testing
id_col = [uuid.uuid4().__str__() for _ in range(X_train.shape[0])]
X_train['id_column'] = id_col[:]


# log baselines
client.log_baseline(
    model_id=client.model_id,
    model_version='v2',
    baseline_data=X_train,
    labels=y_train,
    label_name='flower_type',
    id_cols=['id_column'],
    publish_date='2021-06-01'
)

# adding the id_col to feature_data
feature_ids = [uuid.uuid4().__str__() for _ in range(feature_data.shape[0])]
feature_data['id_column'] = feature_ids[:]


# log predictions
ids = client.log_predictions(
    model_id=client.model_id,
    model_version='v2',
    feature_data=feature_data,
    predictions=preds,
    publish_date='2021-06-01'
)


# log actuals
client.log_actuals(
    model_id=client.model_id,
    model_version='v2',
    actual_ids=ids,
    actuals=y_test,
    publish_date='2021-06-01'
)
