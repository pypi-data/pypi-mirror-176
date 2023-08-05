def feature_importance_cli(path, feature_selection, key, model, output):
    from   genolearn.dataloader         import DataLoader
    from   genolearn.feature_importance import FeatureImportance
    from   genolearn.logger             import Writing
    
    import pickle

    import numpy as np


    dataloader = DataLoader(path, None, None, None)

    selection  = dataloader.load_feature_selection(feature_selection)

    features   = dataloader.features(selection[key].argsort()[::-1])

    with open(model, 'rb') as f:
        model = pickle.load(f)

    importance = FeatureImportance(model)

    scores     = importance.feature_scores
    ranks      = importance.feature_ranks()

    features   = features[ranks]

    with Writing(output):
        np.savez(output, features = features[:len(ranks)], ranks = ranks, scores = scores)
