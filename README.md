# Cellular Automata

## Conway's Game of Life

<img src="../master/Documentation/Conway.gif" width="200">

In [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) cells are classed as either dead (white) or alive (black) and at each time step:
1) A live cell with less than two live neighbours dies.
2) A live cell with more two or three live neighbours lives.
3) A live cell with more than three live neighbours dies.
4) A dead cell with exactly three live comes to life.

## Langston's Ant

<img src="../master/Documentation/Langston.gif" width="200">

In [Langston's Ant](https://en.wikipedia.org/wiki/Langton%27s_ant) a single square (the ant) turns to the right on white cells and to the left on black cells. It then flips the colour of the cell it is on and then moves forward at each timestep.

## Brian's Brain

<img src="../master/Documentation/Brian.gif" width="200">

In [Brian's Brain](https://en.wikipedia.org/wiki/Brian%27s_Brain) cells as classed as dead (white), dying (blue), or alive (black). At each time step:
1) Dead cells with exactly two living neighbours turn on.
2) Live cells become dying cells.
3) Dying cells become dead cells.

## Rule 110

<img src="../master/Documentation/110.gif" width="200">

[Rule 110](https://en.wikipedia.org/wiki/Rule_110) is an elementary cellular automaton (one-dimensional) with on or off states. The state of a cell after one timestep depends on its state and the states of its two neighbours according to

| | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <b>Pattern</b> | 111 | 110 | 101 | 100 | 011| 010 | 001 | 000|
| <b>New State</b> | 0 | 1 | 1 | 0 | 1 | 1 | 1 | 0 |

The y-axis denotes time.

## Rule 90

<img src="../master/Documentation/90.gif" width="200">

[Rule 90](https://en.wikipedia.org/wiki/Rule_90) is an elementary cellular automaton (one-dimensional) with on or off states. The state of a cell after one timestep is given as the exclusive or of its two neighbours.

The y-axis denotes time.

## Fluid simulation
<img src="../master/Documentation/fluid.gif" width="200">

Each cell contains a certain amount of liquid at any time. At each timestep, the liquid will flow downward if possible, or to the left or right. If a cell becomes pressurized, it's liquid can flow upwards. Based off of [this](http://www.jgallant.com/2d-liquid-simulator-with-cellular-automaton-in-unity/).
