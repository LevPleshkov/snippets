from qgis.processing import alg


@alg(name='save_attributes_2', label='Еще атрибуты в CSV', group='', group_label='')
@alg.input(type=alg.SOURCE, name='INPUT', label='Входной слой')
@alg.input(type=alg.FILE_DEST, name='OUTPUT', label='Выходной слой')
def processAlgorithm(self, parameters, context, feedback, inputs):
    """
    Here is where the processing itself takes place.
    """

    # Retrieve the feature source and sink. The 'dest_id' variable is used
    # to uniquely identify the feature sink, and must be included in the
    # dictionary returned by the processAlgorithm function.
    source = self.parameterAsSource(
        parameters,
        'INPUT',
        context
    )

    csv_file = self.parameterAsFileOutput(parameters, 'OUTPUT', context)

    field_names = [field.name() for field in source.fields()]
    features = source.getFeatures()

    with open(csv_file, 'w') as file:
        headers = ','.join(field_names) + '\n'
        file.write(headers)

        for i, feature in enumerate(features):
            if feedback.isCanceled():
                break
            line = ','.join(str(feature[name]) for name in field_names) + '\n'
            file.write(line)

            feedback.setProgressText(f'Line {i+1} ready.')
