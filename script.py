import json
import urllib.request
import pandas as pd

def calculate(url):
    """data processing module to returns the number of water points that are functional, number of whater points percommunity
    and the rank for each community by the percentage of broken waterpoints
    
    
    parameters:
    url (str): hyperlink of the dataset.
    
    returns: 
    dict: dictionary containing number of functional water points, water points per community, rank of each community by pct of broken water points"""
    
    with urllib.request.urlopen(url) as link:
        data = pd.DataFrame(json.loads(link.read().decode()))
    return {
        "number_functional": (data['water_point_condition']=='functioning').sum(),
        "number_water_points":data.groupby('communities_villages').size().to_dict(),
        "community_ranking":data.groupby('communities_villages')['water_point_condition'].value_counts(normalize=True).unstack().assign(broken_pct=lambda x: x['broken'], rank=lambda x: (100-x['broken']).rank(method='max', na_option='bottom')).reset_index().set_index(['communities_villages', 'broken_pct'])['rank'].sort_values().astype(int).to_dict()
    }

if __name__ == "__main__":
    url = input("Enter URL: ")
    print(calculate(url))