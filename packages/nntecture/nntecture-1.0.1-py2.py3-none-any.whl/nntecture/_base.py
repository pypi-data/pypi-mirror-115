"""Main module."""

# Author: Kristian Bonnici <kristiandaaniel@gmail.fi>

import graphviz


class DrawNN:
    """
    DrawNN is a class for Neural Network architecture visualization.

    Parameters
    ----------
    layers : list
        Number of neurons for each layer. I.e. [2,4,3,1] is constructed as
        2 Neurons in the input layer, 4 Neurons in the 1st hidden layer,
        3 Neurons in the 2nd hidden layer, and 1 Neuron in the output layer.

    nn_type : {'ANN', 'RNN'}, default='ANN'
        This parameter specifies the type of the Neural Network.
        - if `'ANN'`, a Artificial Neural Network (ANN) will be created;
        - if `'RNN'`, a Recurrent Neural Network (RNN) will be created;
    """

    def __init__(self,
                 layers,
                 nn_type='ANN'):
        self.layers = layers

        # init neural network
        nn = graphviz.Graph()
        nn.label = "layer 1 (input layer)"
        for layer_num, n_nodes in enumerate(layers):
            if layer_num + 1 < len(layers):
                next_n_nodes = layers[layer_num + 1]
                for node in range(n_nodes):
                    if nn_type is 'RNN' and layer_num is not 0:
                        nn.edge('L' + str(layer_num) + '-' + str(node + 1),
                                'L' + str(layer_num) + '-' + str(node + 1))
                    for next_node in range(next_n_nodes):
                        nn.edge('L' + str(layer_num) + '-' + str(node + 1),
                                'L' + str(layer_num + 1) + '-' + str(next_node + 1))

        self.graph_object = nn

    def draw(self,
             direction='LR',
             linewidth=1.0,
             size='4,4!',
             fillcolor=None,
             node_labels=None,
             graph_label=None,
             node_fontsize=10,
             graph_fontsize=12,
             node_fontcolor='#000000',
             graph_fontcolor='#000000',
             fontname='helvetica'):
        """
        Draw Neural Network architecture.

        Parameters
        ----------
        direction : {'LR', 'RL', 'UD', 'DU'}, default='LR'
            This parameter specifies the direction of the Neural Network.
            - if `'LR'`, from left to right;
            - if `'RL'`, from right to left;
            - if `'UD'`, from up to down;
            - if `'DU'`, from down to up;

        linewidth : float, default=1.0, minimum=0.0
            Specifies the width of the lines and curves.

        size : str, default='4,4!'
            Maximum width and height of drawing, in inches.
            If size ends in an exclamation point "!", then size is taken to be the desired minimum size.

        fillcolor : str, default=None
            Color used to fill the background of a node.
            - if None, fillcolor of "#D3D3D3" will be applied;

        node_labels : True or str, default=True
             Labels for the nodes.
             - if True, nodes will have a layer number, and number of a node in the layer;

        graph_label : str, default=None
            Label for the graph.

        node_fontsize : float, default=10, minimum=1.0
            Font size, in points, used for node labels.

        graph_fontsize : float, default=12, minimum=1.0
            Font size, in points, used for graph label.

        node_fontcolor : str, default='#000000'
            Color used for node labels.

        graph_fontcolor : str, default='#000000'
            Color used for graph label.

        fontname : str, default='helvetica'
            Font used for text.

        Returns
        -------
        display : :class:`~nntecture.DrawNN.graph_object`

        """

        self.graph_object.attr(rankdir=direction, size=size)

        # fonts
        self.graph_object.node_attr["fontsize"] = "{}".format(node_fontsize)
        self.graph_object.graph_attr["fontsize"] = "{}".format(graph_fontsize)
        self.graph_object.node_attr["fontname"] = fontname
        self.graph_object.graph_attr["fontname"] = fontname
        self.graph_object.node_attr["fontcolor"] = node_fontcolor
        self.graph_object.graph_attr["fontcolor"] = graph_fontcolor

        self.graph_object.node_attr["fixedsize"] = "false"
        self.graph_object.edge_attr["penwidth"] = str(linewidth)
        self.graph_object.node_attr["style"] = "filled"
        if fillcolor is not None:
            self.graph_object.node_attr["fillcolor"] = fillcolor
        else:
            self.graph_object.node_attr["fillcolor"] = "#D3D3D3"
        self.graph_object.node_attr["shape"] = "circle"
        self.graph_object.node_attr["fixedsize"] = "true"
        if node_labels is None:
            self.graph_object.node_attr["label"] = ""
        elif node_labels is True:
            pass
        else:
            self.graph_object.node_attr["label"] = node_labels
        if graph_label is not None:
            self.graph_object.graph_attr["label"] = graph_label
        return self.graph_object

    def save(self,
             filename='nn_tecture',
             output_format='pdf',
             dpi=96.0,
             size='4,4!',
             directory=None,
             cleanup=True,
             view=True):
        """
        Save the current Neural Network architecture drawing.

        Parameters
        ----------
        filename : str, default='nn_tecture'
            Name of the file to be saved.

        output_format : str, default='pdf'
            Format of the file to be saved.

        dpi : float, default=96.0
            Specifies the expected number of pixels per inch on a display device.
            For bitmap output,
            dpi guarantees that text rendering will be done more accurately, both in size and in placement.
            For SVG output,
            dpi guarantees the dimensions in the output correspond to the correct number of points or inches.

        size : str, default='4,4!'
            Maximum width and height of drawing, in inches.
            If size ends in an exclamation point "!", then size is taken to be the desired minimum size.

        directory : default=None
            Directory where the file should be saved.
            - if None, file is saved to current working directory (cwd);

        cleanup : {True, False}, default=True
            Delete the source file after successful rendering.

        view : {True, False}, default=True
            Open the rendered result with the default application.

        """
        self.graph_object.attr(size=size)
        self.graph_object.graph_attr['dpi'] = str(dpi)
        self.graph_object.render(filename=filename,
                                 format=output_format,
                                 directory=directory,
                                 cleanup=cleanup,
                                 view=view)
