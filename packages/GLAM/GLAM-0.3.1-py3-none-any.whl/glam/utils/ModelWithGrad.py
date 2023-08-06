import tensorflow as tf


class ModelWithGrad(tf.keras.Model):
    """
    A wrapping class that track gradient norms while training.
    It provides a workaround to spot gradient vanishing while the model has been specified with tensorflow to keras interface.

    It doesn't affect the original model training loop but just add additional metrics.

    Reference: https://keras.io/guides/customizing_what_happens_in_fit/


    >>model_spec = baseline_model.build_training_model()
    >>model = ModelWithGrad(model_spec.input, model_spec.output)
    """

    def train_step(self, data: tf.data.Dataset) -> dict:
        x, y = data

        with tf.GradientTape() as tape:
            y_pred = self(x, training=True)  # type:ignore pyright can't find _call_ on the base
            loss = self.compiled_loss(y, y_pred, regularization_losses=self.losses)

        # compute gradients
        trainable_vars = self.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)

        # calcualte gradients norms - this is our metric to track gradient vanishing
        grad_norms = [tf.norm(g) for g in gradients if isinstance(g, tf.Tensor)]

        # update weights
        self.optimizer.apply_gradients(zip(gradients, trainable_vars))

        # update metrics (includes the metric that tracks the loss)
        self.compiled_metrics.update_state(y, y_pred)

        # return a dict mapping metric names to current value
        return {
            **{m.name: m.result() for m in self.metrics},
            **{
                "min_grad_norm": tf.reduce_min(tf.stack(grad_norms)),
                "max_grad_norm": tf.reduce_max(tf.stack(grad_norms)),
            },
        }