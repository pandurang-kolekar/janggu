

class BwDataset(object):
    """BlueWhale Dataset interface.

    The BlueWhale dataset mimics a numpy array such that it can be
    seamlessly used in conjunction with keras.

    Parameters
    -----------
    name : str
        Name of the dataset

    Attributes
    ----------
    name : str
        Name of the dataset
    shape : tuple
        numpy-style shape of the dataset
    """

    # list of data augmentation transformations
    transformations = []

    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        """Name of the Dataset"""
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise Exception('name must be a string')
        self._name = value

    def __getitem__(self, idxs):

        data = self.data[idxs]

        for tr in self.transformations:
            data = tr(data)

        return data

    def __len__(self):
        pass

    @property
    def shape(self):
        """Shape of the dataset"""
        pass


def inputShape(bwdata):
    """Extracts the shape of a provided Input-BwDataset.

    Parameters
    ---------
    bwdata : :class:`BwDataset` or list(:class:`BwDataset`)
        BwDataset or list(BwDataset).

    Returns
    -------
    dict
        Dictionary with dataset names as keys and the corrsponding
        shape as value.
    """
    if isinstance(bwdata, BwDataset):
        bwdata = [bwdata]

    if isinstance(bwdata, list):
        x = {}
        for el in bwdata:
            shape = el.shape[1:]
            if shape == ():
                shape = (1,)
            x[el.name] = {'shape': shape}
        return x
    else:
        raise Exception('inputSpace wrong argument: {}'.format(bwdata))


def outputShape(bwdata, loss, activation='sigmoid',
                loss_weight=1.):
    """Extracts the shape of a provided Output-BwDataset.

    Parameters
    ---------
    bwdata : :class:`BwDataset` or list(:class:`BwDataset`)
        BwDataset or list(BwDataset).
    loss : str or objective function.
        Keras compatible loss function. See https://keras.io/losses.
    activation : str
        Output activation function. Default: 'sigmoid'.
    loss_weights : float
        Loss weight used for fitting the model. Default: 1.

    Returns
    -------
    dict
        Dictionary description of the network output.
    """

    if isinstance(bwdata, BwDataset):
        bwdata = [bwdata]

    if isinstance(bwdata, list):
        x = {}
        for el in bwdata:
            shape = el.shape[1:]
            if shape == ():
                shape = (1,)
            x[el.name] = {'shape': shape,
                          'loss': loss,
                          'loss_weight': loss_weight,
                          'activation': activation}
        return x
    else:
        raise Exception('outputSpace wrong argument: {}'.format(bwdata))
