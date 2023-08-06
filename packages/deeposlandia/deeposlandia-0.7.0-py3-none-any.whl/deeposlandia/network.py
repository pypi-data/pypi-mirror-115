"""Define a class that represents typical convolutional neural networks
"""

from tensorflow import keras as K


class ConvolutionalNeuralNetwork:
    """Convolutional neural network design

    Attributes
    ----------
    network_name : str
        Name of the network
    image_size : integer
        Input image size (height and width are equal)
    nb_channels : integer
        Number of input image channels (1 for greyscaled images, 3 for RGB
    images)
    nb_labels : integer
        Number of classes in the dataset glossary
    X : tensor
        (batch_size, image_size, image_size, nb_channels)-shaped input tensor;
    input image data
    """

    def __init__(
        self,
        network_name="mapillary",
        image_size=224,
        nb_channels=3,
        nb_labels=65,
        dropout=0.0,
    ):
        if image_size % 16 != 0:
            raise ValueError(
                "The chosen image size is not divisible "
                "per 16. To train a neural network with "
                "such an input size may fail."
            )
        self.network_name = network_name
        self.image_size = image_size
        self.nb_channels = nb_channels
        self.nb_labels = nb_labels
        self.dropout_rate = dropout
        self.in_tensor = K.layers.Input(
            shape=(image_size, image_size, nb_channels), name="input"
        )

    def layer_name(self, prefix, suffix):
        """Concatenate prefix and suffix to build a complete layer name

        Use the default Keras behavior if prefix is None

        Parameters
        ----------
        prefix : str
            Layer name prefix, refers to the layer block
        suffix : str
            Layer name suffix, refers to the layer type

        Returns
        -------
        str
            Complete layer name, build as prefix + suffix
        """
        return prefix + suffix if prefix is not None else None

    def convolution(
        self,
        in_layer,
        nb_filters,
        kernel_size,
        strides=1,
        dilation_rate=1,
        padding="same",
        activation="relu",
        batch_norm=True,
        block_name=None,
    ):
        """Apply a convolutional layer within a neural network

        Use Keras API

        Parameters
        ----------
        in_layer : tensor
            Input layer
        nb_filters : integer
            Number of convolution filters
        kernel_size : integer
            Convolution filter size, in pixel
        strides : integer
            Convolution strides, in pixel
        dilation_rate : integer
            Rate of dilation, for atrous convolution (default to 1, no
        dilation)
        padding : str
            Border pixel management ("valid" to apply convolution pixel only on
        image pixels, or "same" to replicate border pixels)
        activation : str
            Type of activation function to apply on the tensor at the end of
        the convolution block ('relu' by default)
        batch_norm : boolean
            If True, a batch normalization process is applied on `x` tensor
        before activation layer
        block_name : str
            Convolution block name, for identification purpose

        Returns
        -------
        tensor
            4D output layer
        """
        in_layer = K.layers.Conv2D(
            nb_filters,
            kernel_size=kernel_size,
            strides=strides,
            dilation_rate=dilation_rate,
            padding=padding,
            name=self.layer_name(block_name, "_conv"),
        )(in_layer)
        if batch_norm:
            in_layer = K.layers.BatchNormalization(
                name=self.layer_name(block_name, "_bn")
            )(in_layer)
        in_layer = K.layers.Activation(
            activation, name=self.layer_name(block_name, "_activation")
        )(in_layer)
        return in_layer

    def transposed_convolution(
        self,
        in_layer,
        nb_filters,
        kernel_size,
        strides=1,
        padding="same",
        activation="relu",
        batch_norm=True,
        block_name=None,
    ):
        """Build a layer seen as the transpose operation of classic
        convolution, for a convolutional neural network

        Use Keras API

        Parameters
        ----------
        in_layer : tensor
            Input tensor
        nb_filters : integer
            Number of convolution filters
        kernel_size : integer
            Convolution filter size, in pixel
        strides : integer
            Convolution strides, in pixel
        padding : str
            Border pixel management ("valid" to apply convolution pixel only on
        image pixels, or "same" to replicate border pixels)
        activation : str
            Type of activation function to apply on the tensor at the end of
        the convolution block ('relu' by default)
        batch_norm : boolean
            If True, a batch normalization process is applied on `x` tensor
        before activation layer
        block_name : str
            Transposed convolution block name, for identification purpose

        Returns
        -------
        tensor
            4D output layer
        """
        in_layer = K.layers.Conv2DTranspose(
            nb_filters,
            kernel_size=kernel_size,
            strides=strides,
            padding=padding,
            name=self.layer_name(block_name, "_transconv"),
        )(in_layer)
        if batch_norm:
            in_layer = K.layers.BatchNormalization(
                name=self.layer_name(block_name, "_bn")
            )(in_layer)
        in_layer = K.layers.Activation(
            activation, name=self.layer_name(block_name, "_activation")
        )(in_layer)
        return in_layer

    def maxpool(
        self, in_layer, pool_size, strides=1, padding="same", block_name=None
    ):
        """Apply a max pooling layer within a neural network

        Use Keras API

        Parameters
        ----------
        in_layer : tensor
            Input layer
        pool_size : integer
            Pooling kernel size, in pixel
        strides : integer
            Pooling strides, in pixel ; indicates the downscaling factor
        padding : str
            Border pixel management ("valid" to apply convolution pixel only on
        image pixels, or "same" to replicate border pixels)
        block_name : str
            Pooling block name, for identification purpose

        Returns
        -------
        tensor
            4D output layer
        """
        return K.layers.MaxPool2D(
            pool_size=pool_size,
            strides=strides,
            padding=padding,
            name=block_name,
        )(in_layer)

    def dense(
        self, in_layer, depth, activation="relu", batch_norm=True, block_name=None
    ):
        """Apply a fully-connected layer within a neural network

        Use Keras API

        Parameters
        ----------
        in_layer : tensor
            Input layer
        depth : integer
            Number of neurons used within the layer
        activation : str
            Type of activation function to apply on the tensor at the end of
        the convolution block ('relu' by default)
        batch_norm : boolean
            If True, a batch normalization process is applied on `x` tensor
        before activation layer
        block_name : str
            Fully-connected block name, for identification purpose

        Returns
        -------
        tensor
            Output layer
        """
        in_layer = K.layers.Dense(depth, name=self.layer_name(block_name, "_fc"))(in_layer)
        if batch_norm:
            in_layer = K.layers.BatchNormalization(
                name=self.layer_name(block_name, "_bn")
            )(in_layer)
        in_layer = K.layers.Activation(
            activation, name=self.layer_name(block_name, "_activation")
        )(in_layer)
        in_layer = K.layers.Dropout(
            self.dropout_rate, name=self.layer_name(block_name, "_dropout")
        )(in_layer)
        return in_layer

    def flatten(self, in_layer, block_name=None):
        """Apply a flattening operation to input tensor `in_layer`, to reduce its
        dimension; arises generally before a dense layer

        Parameters
        ----------
        in_layer : tensor
            Input layer; its shapes is necessarily larger than 3
        block_name : str
            Flatten block name, for identification purpose

        Returns
        -------
        tensor
            2D output layer
        """
        return K.layers.Flatten(name=block_name)(in_layer)

    def upsample(self, layer1, layer2, block_name=None):
        """Apply an upsampling operation on `layer1` and concatenate the
        resulting layer with `layer2`

        Parameters
        ----------
        layer1 : tensor
            First input layer, its shape must correspond to layer2 shape
        layer2 : tensor
            Second input layer, its shape must correspond to layer1 shape
        block_name : str
            Upsample block name, for identification purpose

        """
        upname = self.layer_name(block_name, "_up")
        ccname = self.layer_name(block_name, "_concat")
        upsample = K.layers.UpSampling2D(size=(2, 2), name=upname)(layer1)
        return K.layers.concatenate([upsample, layer2], axis=3, name=ccname)

    def add_dilated_context(self, input_layer):
        """Add a context block that corresponds to Yu et al. (2016)
        contribution, in order to aggregate multi-scale contextual information

        Parameters
        ----------
        input_layer : tensor
            Input layer, before to add multi-scale context

        """
        context = K.layers.ZeroPadding2D(33)(input_layer)
        context = self.convolution(
            context,
            nb_filters=2 * self.nb_labels,
            kernel_size=3,
            dilation_rate=1,
            padding="valid",
            block_name="conv1_ctx",
        )
        context = self.convolution(
            context,
            nb_filters=2 * self.nb_labels,
            kernel_size=3,
            dilation_rate=1,
            padding="valid",
            block_name="conv2_ctx",
        )
        context = self.convolution(
            context,
            nb_filters=4 * self.nb_labels,
            kernel_size=3,
            dilation_rate=2,
            padding="valid",
            block_name="conv3_ctx",
        )
        context = self.convolution(
            context,
            nb_filters=8 * self.nb_labels,
            kernel_size=3,
            dilation_rate=4,
            padding="valid",
            block_name="conv4_ctx",
        )
        context = self.convolution(
            context,
            nb_filters=16 * self.nb_labels,
            kernel_size=3,
            dilation_rate=8,
            padding="valid",
            block_name="conv5_ctx",
        )
        context = self.convolution(
            context,
            nb_filters=32 * self.nb_labels,
            kernel_size=3,
            dilation_rate=16,
            padding="valid",
            block_name="conv6_ctx",
        )
        context = self.convolution(
            context,
            nb_filters=32 * self.nb_labels,
            kernel_size=3,
            dilation_rate=1,
            padding="valid",
            block_name="conv7_ctx",
        )
        context = self.convolution(
            context,
            nb_filters=self.nb_labels,
            kernel_size=1,
            dilation_rate=1,
            padding="valid",
            activation="linear",
            block_name="conv8_ctx",
        )
        return context
