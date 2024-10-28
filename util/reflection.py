from flask import jsonify


def populate_object(obj, data_dictionary):
    if data_dictionary is None:
        return ({'message': f'Data dictionary is None: {data_dictionary}'})

    fields = data_dictionary.keys()

    for field in fields:
        try:
            getattr(obj, field)
            setattr(obj, field, data_dictionary[field])

        except AttributeError:
            return jsonify({'message': f'attribute {field} not in obj'})
