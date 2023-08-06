# Country Regex Package

**countre** is a package with functions to get standardised names or codes
from country names, as well as additional country information. Country names
often differ between data sources, therefore having standardised codes for each
country makes it easy to merge data from multiple sources.

The countries included are those defined by the International Organization for
Standardization. The list can be found
[here](https://www.iso.org/iso-3166-country-codes.html). The sources of the
country data can be found [here](https://github.com/mwtb47/country-summary-data).

## Installation

**countre** can be installed via pip from PyPi:

```
pip install countre
```

Functions can then be accessed in the following ways:
```
import countre
countre.country_info()
```
or
```
from countre import country_info
country_info()
```

## Functions

### countre.country_info(country_list, variables='iso3', no_match='no_match')

#### Parameters:   
&ensp; **country_list** : *list, Pandas series or Numpy array*  
&ensp; Country names, ISO 3166-1 alpha-2 codes or ISO 3166-1 alpha-3 codes.  

&ensp; **variables** : *str, list, default 'iso3'*  
&ensp; Select one or more from:  
&ensp;&ensp;&ensp; {'country', 'country_short', 'population_2020',  
&ensp;&ensp;&ensp;  'iso2', 'iso3', 'iso_num', 'calling_code', 'ccTLD',  
&ensp;&ensp;&ensp;  'latitude', 'longitude', 'flag', 'capital',  
&ensp;&ensp;&ensp;  'continent', 'sub_region', 'sovereign',  
&ensp;&ensp;&ensp;  'OECD', 'EU', 'EU_EEA', 'flag', 'country_sv',  
&ensp;&ensp;&ensp;  'capital_latitude_sexa', 'capital_longitude_sexa',  
&ensp;&ensp;&ensp;  'capital_longitude', 'capital_latitude', 'gdp_2020',  
&ensp;&ensp;&ensp;  'gdp_per_capita_2020', 'gdp_per_capita_ppp_2020',  
&ensp;&ensp;&ensp;  'total_area', 'land_area', 'water_area'}.

&ensp; **no_match** : *str, default 'no match'*  
&ensp; String returned for each country if no match is found.

#### Returns:
&ensp; List of values if only one variable is given.  
&ensp; Dictionary if more than one variable is given. The dictionary keys are  
&ensp; the variable names and the values are lists of values. This means it can  
&ensp; be used as follows to create a data frame with Pandas:  
&ensp;&ensp; ```pd.DataFrame(country_info(['GBR', 'SWE'], ['country', 'capital']))```

### countre.eu_27(code='country')

#### Parameters:   
&ensp; **code** : *str, default 'country'*  
&ensp; One from: {'country', 'iso2', 'iso3'}  

#### Returns:
&ensp; List of either country names, ISO 3166-1 alpha-2 codes or ISO 3166-1 alpha-3  
&ensp; codes of the 27 EU member countries.

### countre.oecd(code='country')

#### Parameters:   
&ensp; **code** : *str, default 'country'*  
&ensp; One from: {'country', 'iso2', 'iso3'}  

#### Returns:
&ensp; List of either country names, ISO 3166-1 alpha-2 codes or ISO 3166-1 alpha-3  
&ensp; codes of the 37 OECD member countries.
