# Migration for Data Harvester
First migration is `requests` to `httpx`, second is now `matplotlib` to `plotly`.

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
- `matplotlib` - 2 imports, 40 function calls
    | Cardinality | Count |
    |------------|-------------|
    | one-to-zero | 3 |
    | one-to-one (import) | 2 |
    | one-to-one (func call) | 4 |
    | many-to-one | 13 |

### Dashboard
- `matplotlib` - 2 imports, 28 function calls
    | Cardinality | Count |
    |------------|-------------|
    | one-to-zero | 3 |
    | one-to-one (import) | 2 |
    | one-to-one (func call) | 5 |
    | many-to-one | 11 |


## Overall 
