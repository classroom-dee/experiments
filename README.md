## Experiments
This repository is a collection of **computational experiments**, **numerical simulations**, and **toolchain tests**.

Experiments are exploratory by design and may prioritize clarity and insight over performance or completeness.

Scripts are generally self-contained and parameter-driven.  
Generated artifacts (plots, animations, data snapshots) are gitignore-d.

## Repository Structure
The structure is intentionally lightweight and evolves as experiments accumulate.
```
experiments/
├── neo4j-stuff
├── simulations
|   ├── results : scripts will output image/animation results to this directory
|   └── *.py : simulation scripts
└── ** : repo configs
```

## Experiments & Explorations
| Name | Type | Description | Focus |
|--------|--------|--------|--------|
| **Iterated Quadratic Map (Mandelbrot)** | Simulation / Visualization | Escape-time simulation of the Mandelbrot set, including stepwise evolution and animation of boundary determination. | Nonlinear dynamics, fractals, temporal structure |
| **Neo4j Relationship Toy Model** | Toolchain / Data Modeling | Simple Neo4j experiment connecting three people via relationships and visualizing the resulting graph. Created as an introductory exploration of graph databases. | Graph modeling, relationships, visualization |

## Dependencies
Install common dependencies with:
`pip install -r requirements.txt --no-cache-dir`