import itertools
import xml.etree.cElementTree as et

import numpy as np
import pandas as pd
import networkx as nx


def trackmate_peak_import(trackmate_xml_path, get_tracks=False):
    """Import detected peaks with TrackMate Fiji plugin.

    Parameters
    ----------
    trackmate_xml_path : str
        TrackMate XML file path.
    get_tracks : boolean
        Add tracks to label
    """

    root = et.fromstring(open(trackmate_xml_path).read())

    objects = []
    object_labels = {'FRAME': 't_stamp',
                     'POSITION_T': 't',
                     'POSITION_X': 'x',
                     'POSITION_Y': 'y',
                     'POSITION_Z': 'z',
                     'MEAN_INTENSITY': 'I',
                     'ESTIMATED_DIAMETER': 'w',
                     'QUALITY': 'q',
                     'ID': 'spot_id',
                     'MEAN_INTENSITY': 'mean_intensity',
                     'MEDIAN_INTENSITY': 'median_intensity',
                     'MIN_INTENSITY': 'min_intensity',
                     'MAX_INTENSITY': 'max_intensity',
                     'TOTAL_INTENSITY': 'total_intensity',
                     'STANDARD_DEVIATION': 'std_intensity',
                     'CONTRAST': 'contrast',
                     'SNR': 'snr'}

    features = root.find('Model').find('FeatureDeclarations').find('SpotFeatures')
    features = [c.get('feature') for c in features.getchildren()] + ['ID']

    spots = root.find('Model').find('AllSpots')
    trajs = pd.DataFrame([])
    objects = []
    for frame in spots.findall('SpotsInFrame'):
        for spot in frame.findall('Spot'):
            single_object = []
            for label in features:
                single_object.append(spot.get(label))
            objects.append(single_object)

    trajs = pd.DataFrame(objects, columns=features)
    trajs = trajs.astype(np.float)

    # Apply initial filtering
    initial_filter = root.find("Settings").find("InitialSpotFilter")

    trajs = filter_spots(trajs,
                         name=initial_filter.get('feature'),
                         value=float(initial_filter.get('value')),
                         isabove=True if initial_filter.get('isabove') == 'true' else False)

    # Apply filters
    spot_filters = root.find("Settings").find("SpotFilterCollection")

    for spot_filter in spot_filters.findall('Filter'):

        trajs = filter_spots(trajs,
                             name=spot_filter.get('feature'),
                             value=float(spot_filter.get('value')),
                             isabove=True if spot_filter.get('isabove') == 'true' else False)

    trajs = trajs.loc[:, object_labels.keys()]
    trajs.columns = [object_labels[k] for k in object_labels.keys()]
    trajs['label'] = np.arange(trajs.shape[0])

    # Get tracks
    if get_tracks:
        filtered_track_ids = [int(track.get('TRACK_ID')) for track in root.find('Model').find('FilteredTracks').findall('TrackID')]

        new_trajs = pd.DataFrame()
        label_id = 0
        trajs = trajs.set_index('spot_id')

        tracks = root.find('Model').find('AllTracks')
        for track in tracks.findall('Track'):

            track_id = int(track.get("TRACK_ID"))
            if track_id in filtered_track_ids:

                spot_ids = [(edge.get('SPOT_SOURCE_ID'), edge.get('SPOT_TARGET_ID'), edge.get('EDGE_TIME')) for edge in track.findall('Edge')]
                spot_ids = np.array(spot_ids).astype('float')
                spot_ids = pd.DataFrame(spot_ids, columns=['source', 'target', 'time'])
                spot_ids = spot_ids.sort_values(by='time')
                spot_ids = spot_ids.set_index('time')

                # Build graph
                graph = nx.Graph()
                for t, spot in spot_ids.iterrows():
                    graph.add_edge(int(spot['source']), int(spot['target']), attr_dict=dict(t=t))

                # Find graph extremities by checking if number of neighbors is equal to 1
                tracks_extremities = [node for node in graph.nodes() if len(list(graph.neighbors(node))) == 1]

                paths = []
                # Find all possible paths between extremities
                for source, target in itertools.combinations(tracks_extremities, 2):

                    # Find all path between two nodes
                    for path in nx.all_simple_paths(graph, source=source, target=target):

                        # Now we need to check wether this path respect the time logic contraint
                        # edges can only go in one direction of the time

                        # Build times vector according to path
                        t = []
                        for i, node_srce in enumerate(path[:-1]):
                            node_trgt = path[i + 1]
                            t.append(graph.edges[(node_srce, node_trgt)]["attr_dict"]['t'])

                        # Will be equal to 1 if going to one time direction
                        if len(np.unique(np.sign(np.diff(t)))) == 1:
                            paths.append(path)

                # Add each individual trajectory to a new DataFrame called new_trajs
                for path in paths:
                    traj = trajs.loc[path].copy()
                    traj['label'] = label_id
                    label_id += 1

                    new_trajs = new_trajs.append(traj)

        trajs = new_trajs

    return trajs


def filter_spots(spots, name, value, isabove):
    if isabove:
        spots = spots[spots[name] > value]
    else:
        spots = spots[spots[name] < value]

    return spots
