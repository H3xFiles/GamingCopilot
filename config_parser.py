import xml.etree.ElementTree as ET


class ConfigParserException(Exception):
    pass


def configParser(path):
    multipletargetsActions = []
    singletargetActions = []
    try:
        xml_config = ET.parse(path)
        root = xml_config.getroot()
    except ET.ParseError as error:
        raise ConfigParserException("Error parsing config file: {}\n".format(error))

    for child in root.iter('SingleTargetSpell'):
        getKeyNum = child.get('key')
        singletargetActions.append(getKeyNum)

    for child in root.iter('MultipleTargetsSpell'):
        getKeyNum = child.get('key')
        multipletargetsActions.append(getKeyNum)

    print("Config file parsed successfully.\n")

    return singletargetActions, multipletargetsActions
