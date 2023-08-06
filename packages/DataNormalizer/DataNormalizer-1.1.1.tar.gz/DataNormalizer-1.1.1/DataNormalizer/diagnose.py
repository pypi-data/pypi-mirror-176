# See if we can find the mismatch causing the error and fix it in normalise
import json
from math import floor
import re
from difflib import SequenceMatcher
from collections import namedtuple
import bisect
import numpy as np
from time import time

class Diagnose:

    def __init__(self):
        self._appData = None
        self._dataFrame = None
        self._rules = None

    @property
    def appData(self):
        return self._appData
    
    @appData.setter
    def appData(self, value):
        self._appData = json.dumps(value)

    @property
    def dataFrame(self):
        return self._dataFrame
    
    @dataFrame.setter
    def dataFrame(self, value):
        self._dataFrame = value

    @property
    def rules(self):
        return self._rules
    
    @rules.setter
    def rules(self, value):
        self._rules = value

    def obtainKeys(self):
        keys = {}
        jsonData = self._appData

        # Find uuid rename keys using negative lookahead regex; text between { and "type": "rename"
        renameUUIDKeys = re.findall(
            r'\{(?:(?!\{|' + re.escape('"type": "rename"') + r')[\s\S])*' + re.escape('"type": "rename"'), jsonData)
        uuidRegex = re.compile(
            r'[0-9a-z]{9}\_[0-9a-z]{4}\_[0-9a-z]{4}\_[0-9a-z]{4}\_[0-9a-z]{12}')
        uuidDollarRegex = re.compile(
            r'\$[0-9a-z]{9}\_[0-9a-z]{4}\_[0-9a-z]{4}\_[0-9a-z]{4}\_[0-9a-z]{12}')
        renameUUIDKeys = list(set(re.findall(uuidRegex, str(renameUUIDKeys))))

        # Find all $uuid keys
        dollarUUIDKeys = re.findall(uuidDollarRegex, jsonData)
        dollarUUIDKeys = [s.replace('$', '') for s in dollarUUIDKeys]

        # Remove styling parts
        jsonData = re.sub(
            re.escape('config": [') + '.*?' + re.escape('"id"'), '', jsonData)
        jsonData = re.sub(
            re.escape('styling": {') + '.*?' + re.escape('}'), '', jsonData)
        jsonData = re.sub(
            re.escape('styling": [') + '.*?' + re.escape(']'), '', jsonData)

        # Search normal and join keys
        normal_keys = re.findall(r'"key": "(.*?)"', jsonData)
        join_keys = re.findall(r'"join_key": "(.*?)"', jsonData)

        # Merge all key findings
        keys = set(normal_keys + join_keys + renameUUIDKeys + dollarUUIDKeys)
        return keys

    def matchKeys(self):
        keys = Diagnose.obtainKeys(self)

        # Compare the two lists of keys to eachother
        additionalKeys = list(self._dataFrame.columns.difference(keys))
        missingKeys = list(keys.difference(self._dataFrame.columns))

        values = namedtuple('keys', 'missingKeys additionalKeys')
        return values(missingKeys, additionalKeys)

    def fixMismatch(self, strictness=0.8):
        keys = Diagnose.matchKeys(self)
        dataframe = self._dataFrame

        if len(keys.missingKeys) < 1:
            return print("No missing keys")

        suggestions = []

        for i, missingKey in enumerate(keys.missingKeys):
            for additionalKey in keys.additionalKeys:
                similarity = SequenceMatcher(None, missingKey, additionalKey)

                # Check if missingKey looks like additionalKey
                if similarity.ratio() > strictness:
                    values = namedtuple('keys', 'missingKey additionalKey')
                    suggestions.append(values(missingKey, additionalKey))
                    keys.missingKeys.pop(i)

        print("\nWe did not find " + str(len(keys.missingKeys)) +
              " keys:\n" + str(sorted(keys.missingKeys, key=len)) + "\n")

        if len(suggestions) < 1:
            print("No matches, try lowering strictness")
            return dataframe

        # Propose suggestions
        for i, suggestion in enumerate(suggestions):
            print("Suggestion {}: missing '{}' might be additional: '{}'".format(
                i + 1, suggestion.missingKey, suggestion.additionalKey))

        # Ask user which suggestions to fix and then rename dataframe columns
        suggestionsToFix = list(map(int, input(
            "Which suggestion(s) do you want to fix? (example: 1 2 3): ").split()))
        for i in suggestionsToFix:
            dataframe = dataframe.rename(
                columns={suggestions[i - 1].additionalKey: suggestions[i - 1].missingKey})

        return dataframe

    def checkRules(self):
        dataframe = self._dataFrame
        rules = self._rules

        # Global settings
        resetCoverage = False
        globalCheckCoverage = False
        globalAction = False
        globalVerbose = "to-console"

        errorFile = None
        # regex to match the string to-file in between quotes or double quotes
        regex = re.compile(r'\"(to-file)\"|\'(to-file)\'')
        if regex.search(str(rules)):
            errorFile = open(str(floor(time())) + ".txt", "a")

        globalMapping = False   

        # Contains "action" and "verbose"
        errorsFound = False
        def handleError(i, value, rows):
            nonlocal errorsFound
            errorsFound = True

            action = globalAction
            if "action" in rules[j]:
                action = rules[j]["action"]

            if action == "np.nan":    
                rows[i] = np.nan
                
            if action == "drop":
                dataframe.drop(i, inplace=True)
            
            verbose = globalVerbose
            if "verbose" in rules[j]:
                verbose = rules[j]["verbose"]

            if verbose == "to-file":
                errorFile.write(str(rules[j]["column"]) + " mismatch row " + str(i) + " - " + str(value) + "\n")

            if verbose == "to-console":
                print(str(rules[j]["column"]) + " mismatch row "+ str(i) + " - " + str(value))

        j = -1
        while j < len(rules):
            j += 1
            if j >= len(rules):
                break

            # Global rules
            if not("column" in rules[j]):
                if "check-coverage" in rules[j]:
                    globalCheckCoverage = rules[j]["check-coverage"]

                if ("reset-coverage" in rules[j]):
                    if (bool)(rules[j]["reset-coverage"]):
                        resetCoverage = bool(rules[j]["reset-coverage"])

                if ("action" in rules[j]):    
                    globalAction = rules[j]["action"]

                if ("verbose" in rules[j]):    
                    globalVerbose = rules[j]["verbose"]

                if ("column-mapping" in rules[j]):
                    dataframe = dataframe.rename(columns=rules[j]["column-mapping"])
                
                if ("mapping" in rules[j]):
                    globalMapping = rules[j]["mapping"]

                continue

            # Column not found in dataset
            try:
                columnValues = dataframe[rules[j]["column"]]
            except:
                continue                    

            if "mapping" in rules[j] or globalMapping != False:
                mapping = globalMapping
                if "mapping" in rules[j]:
                    mapping = rules[j]["mapping"]

                columnValues = columnValues.replace(mapping)

            if "reset-coverage" in rules[j]:
                if (bool)(rules[j]["reset-coverage"]):
                    resetCoverage = (bool(rules[j]["reset-coverage"]))

            if "check-coverage" in rules[j] or globalCheckCoverage != False:
                if errorsFound and resetCoverage: errorsFound = False
                else:
                    checkCoverage = globalCheckCoverage
                    if "check-coverage" in rules[j]:
                        checkCoverage = (rules[j]["check-coverage"])
                    if re.match(r"^[1-9][0-9]?$|^100$", checkCoverage):
                        columnValues = columnValues.sample(frac=int(checkCoverage) / 100)

            if "selection" in rules[j]:
                sortedSelection = sorted(rules[j]["selection"])
                for i, value in columnValues.items():                    
                    index = bisect.bisect_left(sortedSelection, str(value))
                    if index >= len(sortedSelection) or sortedSelection[index] != value:
                        handleError(i, value, columnValues)

            if "regex" in rules[j]:
                for i, value in columnValues.items():
                    if not re.match(rules[j]["regex"], str(value)):
                        handleError(i, value, columnValues)

            if "type" in rules[j]:
                
                if rules[j]["type"] == "percentage":
                    for i, value in columnValues.items():
                        # Regex to match float between 0 and 100
                        if not re.match(r"^([0-9]|[1-9][0-9]|100)(\.[0-9]+)?$", str(value)):
                            handleError(i, value, columnValues)
                
                if rules[j]["type"] == "boolean":
                    for i, value in columnValues.items():
                        if value != True and value != False:
                            handleError(i, value, columnValues)
                
                if rules[j]["type"] == "float":
                    if (columnValues.dtype == float):
                        continue

                    for i, value in columnValues.items():
                        try:
                            float(value)
                        except ValueError:
                            handleError(i, value, columnValues)
                
                if rules[j]["type"] == "int":
                    if (columnValues.dtype == int):
                            continue

                    for i, value in columnValues.items():
                        try:
                            int(value)
                        except ValueError:
                            handleError(i, value, columnValues)

                if rules[j]["type"] == "positive-int":
                    for i, value in columnValues.items():
                        try:
                            if int(value) < 0:
                                handleError(i, value, columnValues)
                        except ValueError:
                            handleError(i, value, columnValues)

                if rules[j]["type"] == "negative-int":
                    for i, value in columnValues.items():
                        try:
                            if int(value) >= 0:
                                handleError(i, value, columnValues)
                        except ValueError:
                            handleError(i, value, columnValues)

                if rules[j]["type"] == "letters":
                    for i, value in columnValues.items():
                        if (value.isalpha() == False):
                            handleError(i, value, columnValues)

                if rules[j]["type"] == "postal_code":
                    columnValues.str.replace(r"[^a-zA-Z0-9]+", "", regex=True).str.upper()
                    for i, value in columnValues.items():

                        if not re.match(r"^[1-9][0-9]{3}\s?[a-zA-Z]{2}$", str(value)):
                            handleError(i, value, columnValues)

                if rules[j]["type"] == "longitude":
                    for i, value in columnValues.items():
                        if not re.match(r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$", str(value)):
                            handleError(i, value, columnValues)

                if rules[j]["type"] == "latitude":
                    for i, value in columnValues.items():
                        if not re.match(r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$", str(value)):
                            handleError(i, value, columnValues)            

            # Loop again because error in sample
            if (resetCoverage and errorsFound and len(columnValues) < len(dataframe[rules[j]["column"]])): 
                j -= 1
                continue

            dataframe[rules[j]["column"]].update(columnValues)
            errorsFound = False
        return dataframe