# Environment

- python 3.9+

# Doc
```
python -m flight_routes.main [args]
````
usage: main.py [-h] [--bags BAGS] [--return] csvPath origin destination

kiwi flight search

positional arguments:
csvPath
origin
destination

optional arguments:
-h, --help   show this help message and exit
--bags BAGS
--return
````


# Implementation

- code is self documented

### theory

1. process inputs and csv
1. sort flight base on departure time
3. create "chain" (its list of chained flights from origin to destination of last flight in chain)
4. iterate in sorted flights and enrich chains which are in same airports as flight origin if conditions to flight are
   met
5. if destination is final target add chain to "final flight plans"
6. iterate final flight plants to resolve data needed to json export
7. create json models
8. sort base on final price
8. json dumps

---
Autor Bc. Filip Agh



