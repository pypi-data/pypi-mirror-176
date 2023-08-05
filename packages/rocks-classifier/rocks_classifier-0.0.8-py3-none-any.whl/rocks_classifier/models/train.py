# AUTOGENERATED! DO NOT EDIT! File to edit: ../../notebooks/03_d_train.ipynb.

# %% auto 0
__all__ = ['train', 'evaluate', 'main']

# %% ../../notebooks/03_d_train.ipynb 2
#!/usr/bin/env python
"""Trains a model on rocks dataset."""

import logging
import subprocess

import matplotlib.pyplot as plt
import tensorflow as tf

# import tensorflow_addons as tfa
import wandb
import hydra
from omegaconf import DictConfig, OmegaConf
from sklearn.metrics import classification_report

# speed improvements
from tensorflow.keras import backend as K
from tensorflow.keras import layers, mixed_precision
from wandb.keras import WandbCallback

from ..callbacks.callbacks import get_callbacks
from ..data.utils import get_tfds_from_dir, prepare
from .models import get_model
from .utils import get_lr_scheduler, get_model_weights, get_optimizer
from ..visualization.plot import plot_confusion_matrix

# %% ../../notebooks/03_d_train.ipynb 3
tf.get_logger().setLevel(logging.ERROR)
mixed_precision.set_global_policy("mixed_float16")


def train(
    cfg: DictConfig,
    train_dataset: tf.data.Dataset,
    val_dataset: tf.data.Dataset,
    class_weights: dict,
):
    """Train the model and returns model and history.

    Parameters
    ----------
    cfg : DictConfig
        Hydra Configuration
    train_dataset : tf.data.Dataset
        Train Dataset
    val_dataset : tf.data.Dataset
        Validation Dataset
    class_weights : dict
        Class weights dictionary

    Returns
    -------
    model and history
        model and history
    """
    # Initalize model
    tf.keras.backend.clear_session()

    model = get_model(cfg)
    model.summary()

    print(f"\nModel loaded: {cfg.backbone}.\n\n")
    lr_decayed_fn = get_lr_scheduler(cfg, cfg.lr)

    optimizer = get_optimizer(cfg, lr=lr_decayed_fn)
    optimizer = mixed_precision.LossScaleOptimizer(optimizer)  # speed improvements

    # f1_score_metrics = [tfa.metrics.F1Score(num_classes=cfg.num_classes, average="macro", threshold=0.5)]

    # Compile the model
    model.compile(
        optimizer=optimizer,
        loss=cfg.loss,
        metrics=[
            "accuracy",
        ],  # f1_score_metrics
    )

    callbacks, cfg = get_callbacks(cfg)
    verbose = 1

    history = model.fit(
        train_dataset,
        epochs=cfg.epochs,
        validation_data=val_dataset,
        callbacks=callbacks,
        class_weight=class_weights,
        workers=-1,
        verbose=verbose,
    )

    if not cfg.trainable and history.history["val_accuracy"][-1] > 0.75:
        model.layers[0].trainable = False
        # model.trainable = True
        for layer in model.layers[0].layers[-cfg.last_layers :]:
            layer.trainable = True
        # We unfreeze the top 20 layers while leaving BatchNorm layers frozen
        for layer in model.layers[0].layers:
            if isinstance(layer, layers.BatchNormalization):
                layer.trainable = False

        print("\nFinetuning model with BatchNorm layers freezed.\n")
        # print("\nBackbone layers\n\n")
        # for layer in model.layers[0].layers:
        #     print(layer.name, layer.trainable)
        #     lr_decayed_fn = (

        # cfg.reduce_lr.min_lr = cfg.reduce_lr.min_lr * 0.7
        lr_decayed_fn = get_lr_scheduler(cfg, cfg.lr / 10)
        # lr_decayed_fn = tf.keras.optimizers.schedules.CosineDecayRestarts(
        #     K.get_value(model.optimizer.learning_rate),
        #     first_decay_steps=cfg.lr_decay_steps,
        # )
        optimizer = get_optimizer(cfg, lr=lr_decayed_fn)

        # Compile the model
        model.compile(
            optimizer=optimizer,
            loss=cfg.loss,
            metrics=["accuracy"],  # f1_score_metrics
        )

        epochs = cfg.epochs // 3

        callbacks, cfg = get_callbacks(cfg)

        history = model.fit(
            train_dataset,
            epochs=epochs,
            validation_data=val_dataset,
            callbacks=callbacks,
            initial_epoch=len(history.history["loss"]),
            verbose=2,
        )

    return model, history


def evaluate(
    cfg: DictConfig,
    model: tf.keras.Model,
    history: dict,
    test_dataset: tf.data.Dataset,
    labels: list,
):
    """Evaluate the trained model on Test Dataset, log confusion matrix and classification report.

    Parameters
    ----------
    cfg : DictConfig
        Hydra Configuration.
    model : tf.keras.Model
        Tensorflow model.
    history : dict
        History object.
    test_dataset : tf.data.Dataset
        Test Dataset.
    labels : list
        List of Labels.
    """

    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    import numpy as np
    import pandas as pd
    import seaborn as sns

    # Scores
    test_dataset = prepare(test_dataset, cfg)
    scores = model.evaluate(test_dataset, return_dict=True)

    print("\n\nTest Dataset Results!")
    print("Scores: ", scores)

    # Predict

    y_true = tf.concat([y for x, y in test_dataset], axis=0)
    true_categories = tf.argmax(y_true, axis=1)
    y_pred = model.predict(test_dataset, verbose=1)
    predicted_categories = tf.argmax(y_pred, axis=1)

    # Confusion Matrix
    cm = plot_confusion_matrix(labels, true_categories, predicted_categories)

    def get_cm(model, test_dataset, y_true):

        y_prediction = model.predict(test_dataset)
        y_prediction = np.argmax(y_prediction, axis=1)
        y_test = np.argmax(y_true, axis=1)
        # Create confusion matrix and normalizes it over predicted (columns)
        result = confusion_matrix(y_test, y_prediction, normalize="pred")
        disp = ConfusionMatrixDisplay(confusion_matrix=result, display_labels=labels)
        disp.plot()
        plt.xticks(rotation=35)
        plt.savefig("confusion_matrix.png")
        plt.close()
        return result

    cm_sklearn = get_cm(model, test_dataset, y_true)

    # Classification Report
    cl_report = classification_report(
        true_categories,
        predicted_categories,
        labels=[i for i in range(cfg.num_classes)],
        target_names=labels,
        output_dict=False,
    )

    print(f"\nClassification Report\n{cl_report}")

    wandb.log({"Test Accuracy": scores["accuracy"]})
    wandb.log({"Confusion Matrix": cm})
    # wandb.log(
    #     {
    #         "Classification Report Image:": wandb.Image(
    #             "classification_report.png", caption="Classification Report"
    #         )
    #     }
    # )


@hydra.main(config_path="../../configs", config_name="config", version_base="1.2")
def main(cfg) -> None:
    """Run Main function.

    Parameters
    ----------
    cfg : DictConfig
        Hydra Configuration
    """
    
    print(OmegaConf.to_yaml(cfg))

    tf.keras.utils.set_random_seed(cfg.seed) # Setting global seed

    # WandB
    run = wandb.init(
        project=cfg.wandb.project,
        notes=cfg.notes,
        config=OmegaConf.to_container(cfg, resolve=True, throw_on_missing=True),
    )

    # artifact = wandb.Artifact("rocks", type="files")
    # artifact.add_dir("rocks_classifier/")
    # wandb.log_artifact(artifact)

    print(f"\nDatasets used for Training:- {cfg.dataset_id}")

    train_dataset, val_dataset, test_dataset = get_tfds_from_dir(cfg)
    labels = train_dataset.class_names
    cfg.num_classes = len(labels)

    class_weights = get_model_weights(train_dataset) if cfg.class_weights else None

    train_dataset = prepare(train_dataset, cfg, shuffle=True, augment=cfg.augmentation)
    val_dataset = prepare(val_dataset, cfg)

    model, history = train(cfg, train_dataset, val_dataset, class_weights)

    evaluate(cfg, model, history, test_dataset, labels)

    run.finish()



# %% ../../notebooks/03_d_train.ipynb 4
#| eval: false
if __name__ == "__main__":
    main()
