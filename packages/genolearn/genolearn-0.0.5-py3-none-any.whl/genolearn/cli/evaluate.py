def evaluate_cli(model, data_config, feature_selection, ascending, key, values, output):
    from   genolearn.dataloader import DataLoader
    from   genolearn.utils      import check_config

    import joblib
    import pandas as pd

    model       = joblib.load(model)
    data_config = check_config(data_config)
    dataloader  = DataLoader(**data_config)

    if feature_selection and key:
        features = dataloader.load_feature_selection(feature_selection).rank(ascending = ascending)[key]
    else:
        features = None

    X   = dataloader.load_X(*values, features = features)

    df  = pd.DataFrame(index = dataloader.identifiers)
    df['hat'] = dataloader.decode(model.predict(X))
    
    if hasattr(model, 'predict_proba'):
        prob = model.predict_proba(X)
        for i, name in enumerate(dataloader.encoder):
            df[f'P({name})'] = prob[:,i]
    
    df.to_csv(output)
