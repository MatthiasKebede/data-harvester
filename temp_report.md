# Migration for Data Harvester


## Callsites per module
### API Client
- `requests` - 1 import, 8 function calls, 1 exception

| Library | Cardinality | Elements | Properties |
|------------|-------------|---------------|-------------------|
| requests | one-to-one x8 | function call x8, exception x1 | argument addition |
| matplotlib |  |  |  |

### Analyzer
- `requests` - 1 import, 6 function calls
- `matplotlib` - 2 imports, 39 function calls

### Dashboard
- `requests` - 1 import, 5 function calls
- `matplotlib` - 2 imports, 27 function calls


## Overall 
