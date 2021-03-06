# Frequent-Collision Blockchains for Local Geographic Authentication

This repository is a prototype for simulating blockchain protocols distributed over a smartphone *ad hoc* network
([SPAN](https://en.wikipedia.org/wiki/Smartphone_ad_hoc_network)).

## The Motivating Problem

Geographical authentication is the task of certify that
someone is at a certain place;
that is, the task of authenticating someone's geographical location.
This problemhas been considered for over 20 years.
Denning and MacDoran consider the problem of finding the location of anintruder;
other applications include geographically restricted broadcasts,
checkins at Foursquare, and withdrawing cash at an ATM.

Beyond the scope of simple geographical authentication, however, are applications in which both geographical data
and post facto temporal data are useful, such as proving someone was or was not present in a certain vicinity within
a certain timeframe. This is most useful in cases of conflicting information or in cases sensitive to the falsification
of geo-temporal data.

Were geo-temporal data for individual persons to be continually produced and stored, a centralized solution for
managing these data would be far from ideal. First off, centralized solutions create a single point of failure. Further,
a centralized solution is susceptible to the falsification of data by the central node. In the first example below, the
government could try to coerce the centralized node to censor or misrepresent data about the protester. In order
to preclude these weaknesses of endemic to centralized solutions, a decentralized solution is necessary.

This project exists to explore the prospect of using *high-collision blockchains* as a decentralized ledger for local, historical
geographic authentication. Specifically, our `simulation` module is a Python module which seeks to simulate the the dynamics of a
blockchain-like distributed ledger implemented over a smart phone *ad hoc* network ([SPAN](https://en.wikipedia.org/wiki/Smartphone_ad_hoc_network)).
The modules seeks abstract how "blocks" and "transactions" are formalized and verified, and allows the user to pass messages between adjacent nodes,
award legitimate blocks, etc. at rates set by the user. The framework also seeks to accomodate various SPAN topologies and event accomodates the evolution
thereof over time.

## Organization of this Repo

For convenience, the creators of this project have the repo split into `reports` and `simulation` directories. The paper resulting from this project can
compiled by running the `makefile` found in `reports/final_paper` (in addition to certain LaTeX package dependencies, running the `makefile`
successfully requires installation of `latexmk`).

All commands here described should be executed with `simulation` as the current working directory.

### Organization of `simulation` Module

Here, we construct the `simulation` module from the ground up: that is, from its most atomic data types to its most high-level simulation machinery.
We feel that this approach is the most intuitive way to describe the structure of the module.

#### `person_node`

This class is defined in `node_props.py`, and its purpose is to represent, in a most abstract sense, an individual node in a SPAN. The `name` attribute is
meant to allow for easy equality checks and hashability, and the `neighbors` attribute is a set of other `person_node` instances with whom the node is
currently in contact. It is for the purpose of meaningfully (and dynamically) maintaining the `neighbors` attribute that all other attributes
and methods are written.

To support dynamic SPAN topologies, the `person_node` class takes `add_behavior` and `drop_behavior` functions as inputs, which become the methods
`person_node.add_behavior` and `person_node.drop_behavior`, respectively. While `drop_behavior` need not have information about nodes which are not
currently neighbors, the `add_behavior` method requires knowledge about the properties of other `person_node` instances in the same universe. For this reason,
there is a required `universe` argument of type `universe_wrapper` (see below). Determining how neighbors from this `universe` attribute are added/dropped
are further nuanced by arguments for determining the probability of not adding/dropping a neighbor when the opportunity arises (`pass_prob`) and for determining,
if action should take place, whether that action should be a call to `person_node.add_behavior` or `person_node.drop_behavior` (`get_add_prob`).

#### `toroidal_node`

`toroidal_node` is a subclass of the `person_node` class. It is specifically designed to implement the aforementioned `person_node` functionality
under the assumption that nodes form connections based on the evolution of a random geometric graph embedded in the unit torus (for a full explanation,
please see our final writeup under `reports/final_paper`).

#### `cooperative_node`

The `person_node` class is made simply for the purposes of abstracting the dynamic formation of transient connections in a SPAN topology. The `cooperative_node`
subclass of the `person_node` class layers, on top of the SPAN functionality, the message-passing and block-storage machinery necessary to distribute a blockchain
over a SPAN. Messages are passed, and blocks awarded, according to an adaptation of the Bitcoin protocol as described in our final writeup (under
`reports/final_paper`).

#### Wrappers

The `universe_wrapper` class exists to coordinate changes in connections between `person_node` instances comprising a single SPAN. Just as the `cooperative_node`
class inherits from the `person_node` class, the `cooperative_wrapper` class inherits the coordinated SPAN functionality from the `universe_wrapper` class, in
addition to coordinating all problem formulation, message passing, and block propagation between `cooperative_node` instances in the SPAN.

### Prerequisites

Beyond the requisite Python 3 packages (to be listed here), the user should have a terminal-executable version
of [Graphviz](https://graphviz.org/) which supports the .dot file format.

### Installing

If the prerequisites above are installed, this repo should be usable out of the box.
The user might have to give executability permissions to `.sh` files. These are only used to generate figures;
however, to support safe internet practices, the creators encourage users to only run these files with **limited** permissions.

## Running the tests

To run all tests of the underlying simulation framework, simply call `nosetests3` or the like from the directory `simulation`.

The shell script `simulation/test_figure_props.sh` is written so that users can subjectively determine whether figures are being
generated appropriately (it is hard to check this any way other than graphically; these figure tests are deliberately separated
from the rest of the test suite for this reason).

## Built With

* [Graphviz](https://graphviz.org/)
* The Python Science Stack

## Authors

* **Ryan Robinett** - *U Chicago Department of Computer Science*
* **Tiago Royer** - *U Chicago Department of Computer Science*

## License

This project is not yet licensed.

## Acknowledgments

* Started as a project for Ben Zhao and Heather Zheng's CS33300: Graduate Computer Networking taught Fall 2019
