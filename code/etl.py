import pandas as pd
import os  

def top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    location_sums = violations_df.groupby('location')['amount'].sum().reset_index()
    top_locs = location_sums[location_sums['amount'] >= threshold]
    
    return top_locs
    
def top_locations_mappable(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    top_locs = top_locations(violations_df, threshold)
    location_coords = violations_df[['location', 'lat', 'lon']].drop_duplicates(subset='location')
    top_locs_mappable = pd.merge(top_locs, location_coords, on='location')
    
    return top_locs_mappable

def tickets_in_top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    top_locs = top_locations(violations_df, threshold)
    top_loc_list = top_locs['location'].tolist()
    tickets_top = violations_df[violations_df['location'].isin(top_loc_list)]
    
    return tickets_top

if __name__ == '__main__':
    '''
    Main ETL job. 
    '''
    os.makedirs('./cache', exist_ok=True) ##dir
    
    input_file = './cache/final_cuse_parking_violations.csv'
    violations_df = pd.read_csv(input_file)
    
    top_locs_df = top_locations(violations_df)
    top_locs_mappable_df = top_locations_mappable(violations_df)
    tickets_top_df = tickets_in_top_locations(violations_df)
    
    top_locs_df.to_csv('./cache/top_locations.csv', index=False)
    top_locs_mappable_df.to_csv('./cache/top_locations_mappable.csv', index=False)
    tickets_top_df.to_csv('./cache/tickets_in_top_locations.csv', index=False)
    
    print(f"Top locations: {len(top_locs_df)} rows")
    print(f"Top locations mappable: {len(top_locs_mappable_df)} rows")
    print(f"Tickets in top locations: {len(tickets_top_df)} rows")