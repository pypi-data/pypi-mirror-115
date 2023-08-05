# pDMN

## Welcome to the pDMN solver's code repository.

pDMN stands for Probabilistic Decision and Model Notation.
It is an extension to the [DMN](https://www.omg.org/spec/DMN/About-DMN/) standard, which aims to add probabilistic reasoning while maintaining DMN's goal of being readable and user-friendly.

## Installation and usage

In short for Linux: after cloning this repo, install the Python dependencies.

```
git clone https://gitlab.com/EAVISE/cdmn/pdmn-solver
cd pdmn-solver
pip3 install -r requirements.txt
```

After this, you can run the solver. Example usage is as follows:

```
python3 -O solver.py Name_Of_XLSX.xlsx -n "Name_Of_Sheet" -o output_name.idp
```
