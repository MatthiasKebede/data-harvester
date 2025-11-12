# Migration for Data Harvester
First migration is `requests` to `httpx`, second is now `tablib` to `pandas`.

## Callsites & Changes per Module
### API Client
- `requests` - 2 imports, 8 function calls, 1 exception
    | Cardinality | Count |
    |------------|-------------|
    | one-to-zero | 2 |
    | one-to-one (import) | 1 |
    | one-to-one (func call) | 6 |
    | one-to-one (type/exception) | 2 |
    | many-to-one | 2 |

### Analyzer
- `tablib` - 1 import, X function calls
    | Cardinality | Count |
    |------------|-------------|
    | one-to-zero | 6 |
    | one-to-one (import) | 1 |
    | one-to-one (func call) | 6 |
    | many-to-one | 7 |

### Dashboard
- `tablib` - 1 import, X function calls
    | Cardinality | Count |
    |------------|-------------|
    | one-to-zero | 3 |
    | one-to-one (import) | 1 |
    | one-to-one (func call) | 3 |
    | many-to-one | 5 |


## Overall 
