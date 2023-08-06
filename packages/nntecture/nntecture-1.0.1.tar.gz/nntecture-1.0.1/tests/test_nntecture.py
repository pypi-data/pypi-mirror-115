#!/usr/bin/env python

"""Tests for `nntecture` package."""

from nntecture import DrawNN
import graphviz


def test_drawnn():
    # ========== OBJECT & METHODS ==========

    # test RNN
    assert DrawNN([4, 3, 1, 1], nn_type='RNN').layers == [4, 3, 1, 1]

    # confirm that graphviz.dot.Graph object is returned with draw() method
    assert isinstance(DrawNN([1, 2, 3, 1]).draw(), type(graphviz.dot.Graph())) is True

    # confirm that NoneType is returned with draw() method
    #assert isinstance(DrawNN([1, 2, 3, 1]).save(view=False), type(None)) is True

    # confirm that there are no errors with looped variables
    assert isinstance(DrawNN([1, 2, 3, 1]).draw(fillcolor='#000000'), type(graphviz.dot.Graph())) is True
    # test labels
    assert isinstance(DrawNN([4, 4, 5, 2]).draw(node_labels=True), type(graphviz.dot.Graph())) is True
    assert isinstance(DrawNN([4, 4, 5, 2]).draw(node_labels='x'), type(graphviz.dot.Graph())) is True
    assert isinstance(DrawNN([4, 4, 5, 2]).draw(graph_label='ANN'), type(graphviz.dot.Graph())) is True
