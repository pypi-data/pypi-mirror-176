import numpy as np
import tensorflow as tf
from pytest_mock import MockFixture

from dfp.data import (
    _parse_function,
    convert_one_hot_to_image,
    decodeAllRaw,
    main,
    plotData,
    preprocess,
)


def _bytes_feature(value: bytes) -> tf.train.Feature:
    """Returns a bytes_list from a string / byte."""
    if isinstance(value, type(tf.constant(0))):
        value = (
            value.numpy()
        )  # BytesList won't unpack a string from an EagerTensor.
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


class TestDataCase:
    def test_convert_one_hot2img(self):
        hot = tf.random.uniform((1, 16, 16, 3), minval=0, maxval=1)
        hot = hot / tf.reduce_sum(hot, axis=-1, keepdims=True)
        res = convert_one_hot_to_image(hot, dtype="int", act="softmax")
        assert res.numpy().shape == (1, 16, 16, 1)

    def test_preprocess(self):
        img = tf.random.normal((26, 26, 3))
        b = tf.random.uniform(
            shape=(26, 26), minval=0, maxval=2, dtype=tf.int32
        )
        r = tf.random.uniform(
            shape=(26, 26), minval=0, maxval=8, dtype=tf.int32
        )
        img_, b_, r_, hb, hr = preprocess(img, b, r, size=26)
        assert img_.numpy().shape == (1, 26, 26, 3)
        assert b_.numpy().shape == (1, 26, 26)
        assert r_.numpy().shape == (1, 26, 26)
        assert hb.numpy().shape == (1, 26, 26, 3)
        assert hr.numpy().shape == (1, 26, 26, 9)

    def test_decodeAllRaw(self):
        inp = tf.constant("1")
        x = {"image": inp, "boundary": inp, "room": inp}
        i, b, r = decodeAllRaw(x)
        assert i.shape == (1,)
        assert b.shape == (1,)
        assert r.shape == (1,)

    def test_parse_function(self, mocker: MockFixture):
        encoded_image_string = np.array([[1, 2], [3, 4]]).tobytes()
        image = tf.compat.as_bytes(encoded_image_string)
        image = _bytes_feature(image)
        feature = {
            "image": image,
            "boundary": image,
            "room": image,
            "door": image,
        }
        tf_example = tf.train.Example(
            features=tf.train.Features(feature=feature)
        ).SerializeToString()

        res = _parse_function(tf_example)
        assert len(list(res.keys())) == 4

    def test_plotData(self, mocker: MockFixture):
        img = tf.random.normal((1, 26, 26, 3))
        b = tf.random.uniform(
            shape=(1, 26, 26), minval=0, maxval=2, dtype=tf.int32
        )
        r = tf.random.uniform(
            shape=(1, 26, 26), minval=0, maxval=8, dtype=tf.int32
        )
        hb = tf.random.uniform(shape=(1, 26, 26, 3), minval=0, maxval=1)
        hr = tf.random.uniform(shape=(1, 26, 26, 9), minval=0, maxval=1)
        mocker.patch("dfp.data.decodeAllRaw", return_value=(img, b, r))
        mocker.patch("dfp.data.preprocess", return_value=(img, b, r, hb, hr))
        eg = tf.convert_to_tensor(np.array([[1, 2], [3, 4]]).tobytes())
        plotData({"image": eg})

    def test_main(self, mocker: MockFixture):
        mocker.patch("dfp.data.plotData", return_value=None)
        mocker.patch("dfp.data.plt.show", return_value=None)
        arr = np.array([[1, 2], [3, 4]]).tobytes()
        arr = tf.data.Dataset.from_tensor_slices([arr])
        ds = tf.data.Dataset.zip((arr, arr))
        main(ds)
