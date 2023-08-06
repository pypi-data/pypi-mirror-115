# PFG - The Python Factor Graph Library

`PFG` is a lightweight Python library for building and performing inference
 on Factor Graphs. It is implemented in Python and all operations are
  vectorized, so it runs extremely quickly. 
  
`PFG` can perform inference using the Belief Propagation algorithm. In the
 case where factor graphs do not have a tree structure, `PFG` can perform the
  Loopy Belief Propagation algorithm, which isn't guaranteed to converge but
   usually gets good results in practice. When performing Loopy belief
    Propagation, `PFG` also allows the user to create a schedule of factors, so
     that in large graphs the user will have complete control over the order
      in which messages are passed during inference.
      
## Installation

To install `PFG`, simply run the following command:

```
pip install pfg
```

## Usage

For a complete introduction to `PFG`, and full coding examples, take a
 look at the sample notebook `example.ipynb`.