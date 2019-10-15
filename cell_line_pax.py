from datanator_query_python.query import query_pax
from datanator_query_python.config import config as config_query
import pandas as pd


def organize_observation(observations, existing_dict):
    """reorganize observation 
    
    Args:
        observations (:obj:`list` of :obj:`dict`): list of observations
        existing_dict (:obj:`dict`): exisiting dictionary of abundances

    Returns:
        (:obj:`list` of :obj:`dict`): list of reorged observations
    """
    try:
        count = len(list(existing_dict.values())[0])
    except IndexError:
        count = 0
    existing_keys = set(existing_dict.keys())
    processed_keys = set()
    for obs in observations:
        if obs.get('protein_id') is not None:
            uniprot_id = obs['protein_id']['uniprot_id']
        else:
            continue
        abundance = float(obs['abundance'])
        exisitng_abundances = existing_dict.get(uniprot_id)
        if exisitng_abundances is None:
            tmp = [None] * count
            tmp.append(abundance)
            existing_dict[uniprot_id] = tmp
            processed_keys.add(uniprot_id)
        else:
            exisitng_abundances.append(abundance)
            processed_keys.add(uniprot_id)
    unprocessed_keys = existing_keys.difference(processed_keys)
    for key in unprocessed_keys:
        existing_dict[key].append(None)
    return existing_dict 



def main():
    db = 'datanator'
    conf = config_query.TestConfig()
    username = conf.MONGO_TEST_USERNAME
    password = conf.MONGO_TEST_PASSWORD
    MongoDB = conf.SERVER
    pax_manager = query_pax.QueryPax(MongoDB=MongoDB, db=db,
                 verbose=True, max_entries=20, username = username, password = password)
    publication = 'http://www.mcponline.org/cgi/doi/10.1074/mcp.M111.014050'
    file_name = publication.replace('/', '_')
    file_name = './' + file_name + '.csv'
    
    files, _ = pax_manager.get_file_by_publication(publication, projection={'_id': 0, 'file_name': 1, 'observation': 1})
    file_name = []
    prev = {}
    for file in files:
        file_name.append(file['file_name'])
        cur = organize_observation(file['observation'], prev)
        prev = cur
    df = pd.DataFrame.from_dict(cur, orient='index', columns=file_name)
    df.to_csv(file_name, header=True)

if __name__ == "__main__":
    main()