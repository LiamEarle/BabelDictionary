import babeldictionary


def run(event, context):
    """
    Runs the package from Serverless
    :param event:
    :param context:
    :return:
    """
    babeldictionary.main()
    return 'BabelDictionary Successfully Invoked!'
