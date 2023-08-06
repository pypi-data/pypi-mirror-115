[![3D fonts](https://see.fontimg.com/api/renderfont4/aM4g/eyJyIjoiZnMiLCJoIjoxNTYsInciOjIwMDAsImZzIjo3OCwiZmdjIjoiI0VGNzRCNyIsImJnYyI6IiNGREY5RjkiLCJ0IjoxfQ/Tk50ZWN0dXJl/adamas-regular.png)](https://www.fontspace.com/category/3d)

--------------------------------------

![PyPI Version](https://img.shields.io/pypi/v/nntecture)
![License](https://img.shields.io/pypi/l/nntecture)

**NNtecture** is a Python package for Neural Network architecture visualization.

***

Install
-------

NNtecture package runs under Python 3.6+. It can be installed from
[PyPI](https://pypi.org/project/nntecture/):

``` {.sourceCode .python}
pip install nntecture
```

To render the generated DOT source code, you also need to install [Graphviz](https://www.graphviz.org/) ([download page](https://www.graphviz.org/download/)).

Make sure that the directory containing the ``dot`` executable is on your
systems' path.

***

Tutorial
--------

### Basic Usage

After installation, the package is ready to be imported.

``` {.sourceCode .python}
from nntecture import DrawNN
```

Creating your Neural Network architecture with NNtecture is designed to be as easy and intuitive as possible. Drawing a simple architecture can be done in a single line of code (see below).

``` {.sourceCode .python}
DrawNN([2, 4, 4, 2]).draw()
```

<p align="center">
  <img src="https://github.com/kristianbonnici/nntecture/blob/master/img/basic_drawing.jpg?raw=true" width="400" />
</p>

### Built In Customization

The capabilities are not limited into this base form. The architecture can be easily customised as demonstrated in below example.

``` {.sourceCode .python}
# init
nn = DrawNN([3, 3, 3, 3], nn_type='RNN')

# draw
nn.draw(fillcolor='#AF628F',
        graph_label='Recurrent Neural Network (RNN)',
        linewidth=0.5,
        fontname='times',
        node_labels=True,
        node_fontcolor='#ffffff')
```
<p align="center">
  <img src="https://github.com/kristianbonnici/nntecture/blob/master/img/rnn.jpg?raw=true" width="400" />
</p>

### Saving Results

Once satisfied with the architecture, the results can be saved into your desired form.

``` {.sourceCode .python}
# create your architecture
perceptron = DrawNN([2, 1])
perceptron.draw(graph_label='Perceptron (P)', fillcolor='lightblue', linewidth=4)

# save to file
perceptron.save(filename='perceptron', output_format='jpg', size='5,5!', view=True)
```

<p align="center">
  <img src="https://github.com/kristianbonnici/nntecture/blob/master/img/perceptron.jpg?raw=true" width="200" />
</p>

### Advanced Customization Capabilities

Styling your architecture is not limited into the built-in capabilities. In addition, by accessing <code>graph_object</code>, one can further customise the drawing with [graphviz](https://pypi.org/project/graphviz/) (see example below). For more instructions, see [graphviz documentation](https://graphviz.org/documentation/).

``` {.sourceCode .python}
# init
nn = DrawNN([4, 3, 2, 1])
nn.draw(direction='UD', fillcolor='blue')

# further customization
nn.graph_object.edge_attr["style"] = "setlinewidth(2)"
nn.graph_object.edge_attr['color'] = 'purple'
nn.graph_object.graph_attr['bgcolor'] = 'black'
nn.graph_object.node_attr["color"] = "white"

# display
nn.graph_object
```

<p align="center">
  <img src="https://github.com/kristianbonnici/nntecture/blob/master/img/advanced_customization.jpg?raw=true" width="300" />
</p>
