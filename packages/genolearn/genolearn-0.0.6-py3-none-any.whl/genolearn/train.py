def main(path, model, data_config, model_config, train, test, K, order, order_key, ascending, min_count, target_subset, metric, mean_func, overwrite):
    
    params = {k : v for k, v in locals().items() if not k.startswith('_')}

    from genolearn.utils                 import create_log, check_config
    from genolearn.models.classification import get_model
    from genolearn.models                import grid_predictions
    from genolearn.dataloader            import DataLoader
    from genolearn.logger                import msg, print_dict, Writing
    
    import warnings
    import shutil
    import numpy as np
    import os
    import json
    import pickle
    
    if os.path.exists(path):
        if overwrite:
            shutil.rmtree(path)
        else:
            raise Exception(f'"{path}" already exists! Add the "--overwrite" flag to overwrite.')

    os.makedirs(path)

    warnings.simplefilter("ignore")
    os.environ["PYTHONWARNINGS"] = "ignore"

    data_config, model_config = map(check_config, (data_config, model_config))

    params['data_config']  = data_config
    params['model_config'] = model_config

    print_dict('executing "train.py" with parameters', params)

    kwargs     = {key : val for key, val in model_config.items() if isinstance(val, list)}
    common     = {key : val for key, val in model_config.items() if key not in kwargs}

    dataloader = DataLoader(**data_config)
    
    if order and order_key:
        name  = order
        order = dataloader.load_feature_selection(order).rank(ascending = ascending)[order_key]

    Model   = get_model(model)
    
    outputs, params = grid_predictions(dataloader, train, test, Model, K, order, common, min_count, target_subset, metric, mean_func, **kwargs)
    
    params['model'] = model
    
    model, predict, *probs = outputs.pop('best')

    target  = outputs['target']

    os.chdir(path)

    npz     = 'results.npz'
    pkl     = 'model.pickle'
    csv     = 'predictions.csv'
    js      = 'params.json'

    dump    = np.c_[outputs['identifiers'], np.array([target, predict]).T]
    headers = ['identifier', 'target', 'predict']

    if probs:
        for i, label in enumerate(dataloader.encoder):
            dump = np.c_[dump, probs[0][:,i].astype(str)]
            headers.append(label)

    dump = ','.join(headers) + '\n' + '\n'.join(','.join(row) for row in dump)

    with open(csv, 'w') as f:
        f.write(dump)

    with Writing(npz, inline = True):
        np.savez_compressed(npz, **outputs)

    with Writing(pkl, inline = True):
        with open(pkl, 'wb') as f:
            pickle.dump(model, f)

    with Writing(js, inline = True):
        with open(js, 'w') as f:
            f.write(json.dumps(params, indent = 4))
        
    create_log()

    msg('executed "train.py"')

    
if __name__ == '__main__':

    from   genolearn.models import classification
    from   genolearn.logger import print_dict

    import argparse
    
    parser = argparse.ArgumentParser('genolearn.train')

    parser.add_argument('path')
    parser.add_argument('model', choices = classification.valid_models)
    parser.add_argument('data_config')
    parser.add_argument('model_config')
    parser.add_argument('-train', nargs = '+')
    parser.add_argument('-test', nargs = '*')
    parser.add_argument('-K', nargs = '+', type = int)
    parser.add_argument('-order', default = None)
    parser.add_argument('-order_key', default = None)
    parser.add_argument('-ascending', default = False, type = bool)
    parser.add_argument('-min_count', default = 0, type = int)
    parser.add_argument('-target_subset', nargs = '*', default = None)
    parser.add_argument('-metric', default = 'recall')
    parser.add_argument('-mean_func', default = 'weighted_mean')
    parser.add_argument('--overwrite', action = 'store_true')

    args = parser.parse_args()

    main(**dict(args._get_kwargs()))

    


