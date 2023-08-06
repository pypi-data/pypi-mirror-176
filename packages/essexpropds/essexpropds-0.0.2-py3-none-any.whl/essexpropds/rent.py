import pyodbc
import pandas as pd
import warnings
from util import sql_conn

def rent_floor(date_min):
    '''
    Usage: Read YieldStar RentRecommendationHisotry SQL Server Data and output weighted Offered and RecentAverageEffective Rent by Floorplan
    Parameters: - str date_min: YYYY-MM-DD date format
    Return:     - pd.Dataframe df_tmp: the queried data 
    '''

    warnings.filterwarnings('ignore')
  
    ### Read YieldStar RentRecHistory data
    database = 'BI-RevenueManagement'
    query = f"""
        SELECT PropertyId, PropertyFloorPlan, Postdate, Actualunits units, Currentofferedeffectiverent rent_offer,
        Recentaverageeffectiverent rent_rae
        FROM fact.RentRecommendationHistory
        WHERE Postdate >= '{date_min}'
    """
    df_final = sql_conn(Database=database, Query=query, Server = 'azr-sql01-p.essexpropertytrust.com')
    
    return df_final

def rent_bed(date_min):
    '''
    Usage: Read YieldStar RentRecommendationHisotry SQL Server Data and output weighted Offered and RecentAverageEffective Rent by Bedroom
    Parameters: - str date_min: YYYY-MM-DD date format
    Return:     - pd.Dataframe df_tmp: the queried data 
    '''

    warnings.filterwarnings('ignore')
  
    ### Read YieldStar RentRecHistory data
    database = 'BI-RevenueManagement'
    query = f"""
        SELECT PropertyId, Bedroom, PropertyFloorPlan, Postdate, Actualunits, Currentofferedeffectiverent, Recentaverageeffectiverent
        FROM fact.RentRecommendationHistory
        WHERE Postdate >= '{date_min}'
    """
    df_rent = sql_conn(Database=database, Query=query, Server = 'azr-sql01-p.essexpropertytrust.com')
    
    ### Process data
    # Remove BMR and Pendhouse floorplans
    df_tmp = df_rent[~df_rent['PropertyFloorPlan'].str.contains('MOD|BMR|PENT')]
    
    # Calculate weight of bedroom rent
    df_tmp['units'] = df_tmp.groupby(['PropertyId', 'Bedroom', 'Postdate'])['Actualunits'].transform(sum)
    df_tmp['wgt'] = df_tmp['Actualunits']/df_tmp['units']
    df_tmp['rent_offer'] = df_tmp['wgt'] * df_tmp['Currentofferedeffectiverent']
    df_tmp['rent_rae'] = df_tmp['wgt'] * df_tmp['Recentaverageeffectiverent']
    
    # Calculate weighted Offered and RAE rents
    df_tmp['rent_offer'] = df_tmp.groupby(['PropertyId', 'Bedroom', 'Postdate'])['rent_offer'].transform(sum)
    df_tmp['rent_rae'] = df_tmp.groupby(['PropertyId', 'Bedroom', 'Postdate'])['rent_rae'].transform(sum)
    df_final = df_tmp.groupby(['PropertyId', 'Bedroom', 'Postdate', 'units'])[['rent_offer', 'rent_rae']].mean().reset_index()
    
    return df_final

def rent_property(date_min):
    '''
    Usage: Read YieldStar RentRecommendationHisotry SQL Server Data and output weighted Offered and RecentAverageEffective Rent by Property
    Parameters: - str date_min: YYYY-MM-DD date format
    Return:     - pd.Dataframe df_tmp: the queried data 
    '''

    warnings.filterwarnings('ignore')
  
    ### Read YieldStar RentRecHistory data
    database = 'BI-RevenueManagement'
    query = f"""
        SELECT PropertyId, PropertyFloorPlan, Postdate,  Actualunits, Currentofferedeffectiverent, Recentaverageeffectiverent
        FROM fact.RentRecommendationHistory
        WHERE Postdate >= '{date_min}'
    """
    df_rent = sql_conn(Database=database, Query=query, Server = 'azr-sql01-p.essexpropertytrust.com')
    
    ### Process data
    # Remove BMR and Pendhouse floorplans
    df_tmp = df_rent[~df_rent['PropertyFloorPlan'].str.contains('MOD|BMR|PENT')]
    
    # Calculate weight of bedroom rent
    df_tmp['units'] = df_tmp.groupby(['PropertyId', 'Postdate'])['Actualunits'].transform(sum)
    df_tmp['wgt'] = df_tmp['Actualunits']/df_tmp['units']
    df_tmp['rent_offer'] = df_tmp['wgt'] * df_tmp['Currentofferedeffectiverent']
    df_tmp['rent_rae'] = df_tmp['wgt'] * df_tmp['Recentaverageeffectiverent']
    
    # Calculate weighted Offered and RAE rents
    df_tmp['rent_offer'] = df_tmp.groupby(['PropertyId', 'Postdate'])['rent_offer'].transform(sum)
    df_tmp['rent_rae'] = df_tmp.groupby(['PropertyId', 'Postdate'])['rent_rae'].transform(sum)
    df_final = df_tmp.groupby(['PropertyId', 'Postdate', 'units'])[['rent_offer', 'rent_rae']].mean().reset_index()
    
    return df_final

def rent_portfolio(date_min):
    '''
    Usage: Read YieldStar RentRecommendationHisotry SQL Server Data and output weighted Offered and RecentAverageEffective Rent by Date
    Parameters: - str date_min: YYYY-MM-DD date format
    Return:     - pd.Dataframe df_tmp: the queried data 
    '''

    warnings.filterwarnings('ignore')
  
    ### Read YieldStar RentRecHistory data
    database = 'BI-RevenueManagement'
    query = f"""
        SELECT PropertyFloorPlan, Postdate, Actualunits, Currentofferedeffectiverent, Recentaverageeffectiverent
        FROM fact.RentRecommendationHistory
        WHERE Postdate >= '{date_min}'
    """
    df_rent = sql_conn(Database=database, Query=query, Server = 'azr-sql01-p.essexpropertytrust.com')
    
    ### Process data
    # Remove BMR and Pendhouse floorplans
    df_tmp = df_rent[~df_rent['PropertyFloorPlan'].str.contains('MOD|BMR|PENT')]
    
    # Calculate weight of bedroom rent
    df_tmp['units'] = df_tmp.groupby(['Postdate'])['Actualunits'].transform(sum)
    df_tmp['wgt'] = df_tmp['Actualunits']/df_tmp['units']
    df_tmp['rent_offer'] = df_tmp['wgt'] * df_tmp['Currentofferedeffectiverent']
    df_tmp['rent_rae'] = df_tmp['wgt'] * df_tmp['Recentaverageeffectiverent']
    
    # Calculate weighted Offered and RAE rents
    df_tmp['rent_offer'] = df_tmp.groupby(['Postdate'])['rent_offer'].transform(sum)
    df_tmp['rent_rae'] = df_tmp.groupby(['Postdate'])['rent_rae'].transform(sum)
    df_final = df_tmp.groupby(['Postdate', 'units'])[['rent_offer', 'rent_rae']].mean().reset_index()
    
    return df_final