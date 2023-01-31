## Overview
The input to this problem is a list of orders for rolls of paper of a particular width. Each of the orders is cut from a larger master roll of paper using a predefined pattern. The goal is to determine how many of each type of pattern is needed in order to fulfill all the demands.

## Input
The input data consists of:
| Order Width  | Number Ordered |
| ------------- | ------------- |
| 10  | 75  |
| 15  | 35  |
| 20  | 15  |

A list of patterns that can be cut from the master roll. For example, suppose the master roll has width 35 and we use the order widths defined above.
| Pattern ID  | Pattern Cut |
| ------------- | ------------- |
| 1  | -10-10-10-  |
| 2  | -10-10-15-  |
| 3  | -15-15-  |
| 4  | -15-20-  |

Pattern 1 cuts three rolls of width 10 from the master roll. Pattern 2 cuts two rolls of width 10 and one roll of width 15 from the master roll. Etc…

## Output
The output of the optimization should be the number of each type of pattern cut to fulfill all the orders.

## Goal
Minimize the total number or master rolls of paper cut subject to fulfilling all the orders
