# General Information
The DataNormalizer package is made to help data scientists with validating and normalising data that they are going to import. Right now the library is able to validate columns and check datasets based on a set of rules like custom data types. 
 
```python
import DataNormalizer
```

### Setting variables
The DataNormalizer library might need the details of the target app. These setting are set through properties.
```python
Clappform.Auth(baseURL="https://dev.clappform.com/", username="user@email.com", password="password")
Diagnose = DataNormalizer.Diagnose()
Diagnose.appData = Clappform.App("appname").ReadOne(extended=True)
Diagnose.dataFrame = pandas.read_excel("../data.xlsx")
Diagnose.rules = json.load(open('../rules.json'))
```

### checkRules
Function that will check the custom rules against your dataframe. Requires dataFrame and rules. Returns a dataframe
```python
Diagnose = DataNormalizer.Diagnose()
Diagnose.dataFrame = pandas.read_excel("../data.xlsx")
Diagnose.rules = json.load(open('../rules.json'))
result = Diagnose.checkRules()
```
Rules are added in a JSON file. Every column has its own rule, however rules without a column name are seen as global rules. 
```json
{
    "reset-coverage":"True",
    "action": "np.nan"
},
{ 
    "column": "gemeente",
    "check-coverage": "10",
    "selection": [ "Aa en Hunze", "Aalsmeer", "Aalten", "Achtkarspelen"]
},
{
    "column": "postalCode",
    "type": "postal_code"
}
```
Supported keys are
keys          | value                                   | explanation                                            | Global
------------- | -------------                           | -------------                                          | -------------
column        | gemeente                                | On which column does this rule apply                   | No
type          | postal_code / int / string...           | What should the values of this column be               | No
action        | np-nan                                  | What to do with the value if incorrect                 | Yes
selection     | [ "Aa en Hunze", "Aalsmeer", "Aalten"]  | The values must be one of these values                 | No
mapping       | {"bad": "0","moderate": "1"}            | Map values to something else                           | No
regex         | [1-9][0-9]?$^100$                       | Column value should look like this regex               | No
check-coverage| 50                                      | Take a smaller sample of the column, in percentage     | Yes
coverage-reset| True / False                            | If an error is found in the sample, fall back to 100%  | Yes

Supported values for types
type          | explanation        
------------- | -------------
int         | accepts ints and floats get decimal removed
positive-int | same as int but only positive and zero  
negative-int | same as int but only negative   
string | characters accepted   
float | decimal numbers accepted   
boolean | makes lowercase and accepts true / false    
postal_code | accepts 1111AB format. Removes special chars then makes string uppercase
latitude / longitude | accepts 32.111111 format
letters | only accepts letters 

Supported values for action
action          | explanation        
------------- | -------------
np.nan         | Replaces mismatches with np.nan

### obtainKeys
Function that will find keys needed for the app, needs appData. Returns keys
```python
Diagnose = DataNormalizer.Diagnose()
Diagnose.appData = Clappform.App("appname").ReadOne(extended=True)
Diagnose.obtainKeys()
```

### matchKeys
Function that will find missing keys, needs appData and dataFrame. Returns missing and additional keys
```python
Diagnose = DataNormalizer.Diagnose()
Diagnose.appData = Clappform.App("appname").ReadOne(extended=True)
Diagnose.dataFrame = pandas.read_excel("../data.xlsx")
Diagnose.matchKeys()
```

### fixMismatch
Function that will suggest changes to your dataset based on missing keys, needs appData and dataFrame. Lowering the strictness will increase the amount of matches with possible keys. Needs appData and dataFrame. Interaction via terminal.
```python
Diagnose = DataNormalizer.Diagnose()
Diagnose.appData = Clappform.App("appname").ReadOne(extended=True)
Diagnose.dataFrame = pandas.read_excel("../data.xlsx")
Diagnose.fixMismatch(strictness = 0.8)
```