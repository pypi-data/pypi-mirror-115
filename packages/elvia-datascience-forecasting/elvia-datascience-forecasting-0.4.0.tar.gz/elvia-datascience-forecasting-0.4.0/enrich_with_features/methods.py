from azureml.core import Dataset  # type: ignore
from datetime import timedelta, datetime
import inspect
import logging
from logging import Logger
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from types import FrameType
from typing import cast, Optional, Union

from enrich_with_features.data_models import EndpointRequest
from enrich_with_features.errors import NotEnoughDataError, UnspecifiedTimeSpanError
from enrich_with_features.logs import LogEntry
from enrich_with_features.features.add_metadata import add_metadata
from enrich_with_features.features.dayofweek import dayofweek
from enrich_with_features.features.hourofday import hourofday
from enrich_with_features.features.monthyear import monthyear
from enrich_with_features.features.hourofweek import hourofweek
from enrich_with_features.features.school_holiday import school_holiday
from enrich_with_features.features.national_holiday import national_holiday
from enrich_with_features.features.temperature_hourly import temperature_hourly
from enrich_with_features.features.average_weekly_data import average_weekly_data
from enrich_with_features.features.shifted_hourly_load import shifted_hourly_load
from enrich_with_features.features.sin_cos_cyclical_feature import sin_cos_transformation


def enrich(
        df: pd.DataFrame,  # NOSONAR
        weekly_dataset: Dataset,
        holiday_path: str = '',
        token_weather: str = '',
        time_zone: bool = False,
        deployment: bool = False,
        logger: Optional[Logger] = None,
        endpoint_request: Optional[EndpointRequest] = None) -> pd.DataFrame:
    """
    This function takes in substations load as dataframe(df) and adds new features to 
    the dataframe which will be used to build machine learning models

    # Parameters
    --------------
    df          : Dataframe of consumption data
    weekly_dataset   : Weekly average cumsumtion AZURE DATASET
    holiday_path: The path of the json file that contains dates of national and school holidays
    token_weather: Token for Weather API
    time_zone   : Weather data comes with timezone UTC. It can be set to Oslo-timezone by writing 'time_zone = True'
    deployment  : If this function is used in deployment step, it should be set as 'True'
    logger : Logger object, optional

    # Returns
    --------------
    A pandas dataframe without index of 'date_tz' and feature of 'trafo'
    """

    log_counter: int = 0
    log_counter = add_debug_trace(
        f'Incoming df.shape: {str(df.shape)}, incoming weekly_dataset.shape: {str(weekly_dataset.to_pandas_dataframe().shape)}',
        logger, endpoint_request, log_counter)

    df = df.set_index('date_tz')
    log_counter = add_debug_trace(
        f'After setting index: {str(df.head().to_string())}', logger,
        endpoint_request, log_counter)

    # Adding 72, 96 and 168 hours shifting
    for hour in [72, 96, 168]:
        df = shifted_hourly_load(df, t=hour)
    df.dropna(inplace=True)

    # Adding days of a week to dataframe
    df = dayofweek(df)
    log_counter = add_debug_trace(
        f'After applying dayofweek: {str(df.head().to_string())}', logger,
        endpoint_request, log_counter)

    # Adding hours of a day to dataframe
    df = hourofday(df)
    log_counter = add_debug_trace(
        f'After applying hourofday: {str(df.head().to_string())}', logger,
        endpoint_request, log_counter)

    # Adding hour of week to dataframe (0 - 167)
    df = hourofweek(df)
    log_counter = add_debug_trace(
        f'After applying hourofweek: {str(df.head().to_string())}', logger,
        endpoint_request, log_counter)

    # Adding month of a year to dataframe
    df = monthyear(df)
    log_counter = add_debug_trace(
        f'After applying monthyear: {str(df.head().to_string())}', logger,
        endpoint_request, log_counter)

    # we reset index before merging with average_weekly_data, otherwise we will lose 'date_tz' index
    df.reset_index(inplace=True)
    log_counter = add_debug_trace(
        f'After resetting the index: {str(df.head().to_string())}', logger,
        endpoint_request, log_counter)

    # Adding average_weekly_data to dataframe
    df_average_weekly = average_weekly_data(weekly_dataset)
    df = df.merge(df_average_weekly,
                  left_on=['hourofweek', 'trafo'],
                  right_on=['houroftheweek', 'trafo'],
                  how='left')
    df.drop(['houroftheweek', 'hourofweek'], axis=1, inplace=True)
    log_counter = add_debug_trace(
        f'After merging with df_average_weekly: {str(df.head().to_string())}',
        logger, endpoint_request, log_counter)

    df = df.set_index('date_tz')  # setting index again
    df['trafo'] = df['trafo'].astype('category')
    log_counter = add_debug_trace(
        f'After setting index and adding trafo: {str(df.head().to_string())}',
        logger, endpoint_request, log_counter)

    # Adding school holiday to dataframe
    df = school_holiday(df, path_holiday=holiday_path)
    log_counter = add_debug_trace(
        f'After applying school_holiday : {str(df.head().to_string())}',
        logger, endpoint_request, log_counter)

    df['school_holiday'] = df['school_holiday'].astype(
        'bool')  # casting type from object to boolean
    log_counter = add_debug_trace(
        f'After changing school_holiday dtype: {str(df.head().to_string())}',
        logger, endpoint_request, log_counter)

    # Adding national holiday to dataframe
    df_national_holiday = national_holiday(df, path_holiday=holiday_path)
    df = df.merge(df_national_holiday,
                  left_on=['date_tz'],
                  right_on=['date_tz'],
                  how='left')

    # Adding Weather data
    start_date = df.index[0].strftime(format='%Y-%m-%d')
    end_date = (df.index[-1] + timedelta(days=1)).strftime(format='%Y-%m-%d')
    df_weather = temperature_hourly(df,
                                    'temperature',
                                    start_date=start_date,
                                    end_date=end_date,
                                    time_zone=time_zone,
                                    weather_token_id=token_weather)
    # Reset index to merge dataframes based on index column and trafo column
    df.reset_index(drop=False, inplace=True)
    df = df.merge(df_weather,
                  left_on=['date_tz', 'trafo'],
                  right_on=['time', 'trafo'],
                  how='left')
    df['trafo'] = df['trafo'].astype('category')
    # Drop these columns because we will not use them in ML model
    df.drop('time', axis=1, inplace=True)

    # Sine and cosine transformation
    cyclical_features = [('hourofday', 23), ('dayofweek', 6),
                         ('monthyear', 12)]
    for col in cyclical_features:
        sin_cos_transformation(df, col[0], col[1])
        df.drop([col[0]], axis=1, inplace=True)

    if deployment:
        # Drop the 3 cyclical features and other columns because we will not use them in ML model
        df.drop([
            'aggregated_per_mp', 'trafo', 'date_tz', 'station_name',
            'fylkesnavn', 'long', 'lat'
        ],
                axis=1,
                inplace=True)
    else:
        # Drop the 3 cyclical features and other columns because we will not use them in ML model
        df.drop(['station_name', 'fylkesnavn', 'long', 'lat'],
                axis=1,
                inplace=True)

    log_counter = add_debug_trace(f'Final df.shape : {str(df.shape)}', logger,
                                  endpoint_request, log_counter)

    return df


def _check_input_data(df: pd.DataFrame,
                      percentage: float = 0.1,
                      value_col: str = 'aggregated_per_mp',
                      trafo_col: str = 'trafo',
                      len_history: int = (365 + 366) * 24):
    '''
    This function checks the zero values ​​of the transformers in the dataset and if the zero values ​​in a transformer are more than one-tenth of the transformer's length, this          transformer is removed from the dataset.

    # Parameters
    --------------
    df            : Azure energy consumption dataset
    percentage    : Percentage that is used to select the appropriate transformers
    column_name   : Name of the column showing energy consumption 
    trafo_column  : Name of the column showing substations' names

    # Returns
    --------------
    A pandas dataframe with the transformers that has less zero values than one-tenth of their length.
    '''

    # Group by
    count_zeros_df = df.groupby(trafo_col).agg(lambda x: x.eq(0).sum())

    # empty_trafo_idx is a CategoricalIndex
    empty_trafo_idx = count_zeros_df.loc[
        count_zeros_df[value_col] > len_history * percentage].index
    #
    if not empty_trafo_idx.empty:
        df.drop(index=df.loc[df[trafo_col].isin(empty_trafo_idx)].index,
                inplace=True)
    #
    return df


def ingest_data(  # NOSONAR
        hist_cons_dataset: Dataset,  # NOSONAR
        metadata_dataset: Dataset,
        last_day: datetime = None,
        first_day: datetime = None,
        percentage: float = 0.9,
        trafo_name: str = '',
        deployment: bool = False,
        time_zone: bool = False,
        forecast_horizon: int = 67,
        outliers_exclusion: int = 5,
        logger: Optional[Logger] = None,
        endpoint_request: Optional[EndpointRequest] = None) -> pd.DataFrame:
    '''
    This function takes in Azure energy consumption dataset and its Azure metadata dataset. Substation Ids in the Azure energy consumption dataset
    will be renamed by using Driftsmerking name in the Azure metadata dataset. 

    # Parameters
    --------------
    hist_cons_dataset : Azure energy consumption dataset
    metadata_dataset   : Energy consumption Azure metadata dataset
    last_day      : Last day of the energy consumption data (datetime(year, month, day, hour, minute, second) )
    first_day     : First day of the energy consumption data (datetime(year, month, day, hour, minute, second) )
    percentage    : Percentage that is used to select the appropriate transformers
    time_zone     : Substation data comes with timezone UTC. It can be set to Oslo-timezone by writing 'time_zone = True'
    deployment    : If this function is used in deployment, it should be set as 'True', otherwise 'False'
    logger        : Logger object, optional
    endpoint_request : Argument to be used together with loggers of type LogEntry, optional

    # Returns
    --------------
    A pandas dataframe with the transformers that has rows greater than determined percentage(90%) of the number of hours in the selected date range

    :raises UnspecifiedTimeSpanError: last_day and first_day were needed, but at least one of them was unspecified
    :raises NotEnoughDataError: Not enough data    
    '''

    df: pd.DataFrame = hist_cons_dataset.to_pandas_dataframe()

    log_counter: int = 0
    log_counter = add_debug_trace(f'Incoming df.shape: {str(df.shape)}',
                                  logger, endpoint_request, log_counter)

    df['trafo'] = df['trafo'].astype('category')
    log_counter = add_debug_trace(
        f'Changed trafo dtype: {str(df.head().to_string())}', logger,
        endpoint_request, log_counter)

    # change series name
    df.rename(columns={"dtm": "date_tz"}, inplace=True)
    df['date_tz'] = pd.to_datetime(
        df['date_tz'], infer_datetime_format=True,
        utc=True)  # convert object date to datetime64[ns, UTC]
    #df.sort_values(by=['trafo', 'date_tz'], inplace=True)

    log_counter = add_debug_trace(
        f'modified index: {str(df.head().to_string())}', logger,
        endpoint_request, log_counter)
    log_counter = add_debug_trace(
        f'number of unique trafo: {str(df["trafo"].nunique())}', logger,
        endpoint_request, log_counter)

    if deployment:
        df = df.loc[df['trafo'] == trafo_name]
        log_counter = add_debug_trace(
            f'df.shape after filtering by trafo: {str(df.shape)}', logger,
            endpoint_request, log_counter)

        # Adding forecast_horizon hours to the index by shifting the existing index of forecast_horizon steps
        df = df.set_index('date_tz')
        log_counter = add_debug_trace(
            f'df after setting index: {str(df.head().to_string())}', logger,
            endpoint_request, log_counter)

        idx_horizon = df.shift(
            freq=f'{forecast_horizon}H').index[-forecast_horizon:]
        log_counter = add_debug_trace(
            f'df after shifting the index: {str(df.head().to_string())}',
            logger, endpoint_request, log_counter)

        other = pd.DataFrame([], columns=df.columns, index=[idx_horizon])
        other.reset_index(inplace=True)
        df.reset_index(inplace=True)
        df = df.append(other)
        # filling NaN values. ‘ffill’ stands for ‘forward fill’ and will propagate last valid observation forward.
        df = df.ffill()
        log_counter = add_debug_trace(
            f'df.shape after resetting index and forward filling: {str(df.shape)}',
            logger, endpoint_request, log_counter)

    else:  # training part

        # check the input data
        df = _check_input_data(df,
                               percentage=0.1,
                               value_col='aggregated_per_mp',
                               trafo_col='trafo',
                               len_history=len(df['date_tz'].unique()))

        log_counter = add_debug_trace(
            f'df after calling _check_input_data: {str(df.head().to_string())}',
            logger, endpoint_request, log_counter)

        # Keep columns that have more than 90% of the number of hours in the selected date range
        if not last_day or not first_day:
            raise UnspecifiedTimeSpanError

        date_range = last_day - first_day
        diff_hour = date_range.total_seconds(
        ) / 3600  # difference based on hour

        df_ranged = pd.DataFrame(columns=df.columns)
        for station_id in df['trafo'].unique():
            data_set = df.loc[df.trafo == station_id]
            if len(data_set) < diff_hour * percentage:
                continue
            df_ranged = df_ranged.append(data_set, ignore_index=True)
        df = df_ranged

        log_counter = add_debug_trace(
            f'df.head() after selecting trafo with more than 90% of data: {str(df.head().to_string())}',
            logger, endpoint_request, log_counter)

        # Raise exception if the dataframe is empty
        if df.empty:
            log_counter = add_debug_trace(
                'NotEnoughDataError: DataFrame is empty', logger,
                endpoint_request, log_counter)
            raise NotEnoughDataError

        # Remove outliers
        for station_id in df['trafo'].unique():
            v = df.loc[df['trafo'] == station_id, 'aggregated_per_mp']
            w = _remove_outliers(v, -outliers_exclusion, outliers_exclusion)
            df.loc[df['trafo'] == station_id, 'aggregated_per_mp'] = w.values

        log_counter = add_debug_trace(
            f'df.shape after removing outliers: {str(df.shape)}', logger,
            endpoint_request, log_counter)
        log_counter = add_debug_trace(
            f'df.head() after removing outliers: {str(df.head().to_string())}',
            logger, endpoint_request, log_counter)

    # Merging dataframe with substation metadata to add kommunenavn, latitude and longitude to the dataframe
    df_metadata = metadata_dataset.to_pandas_dataframe()
    df['station_name'] = df.trafo.apply(add_metadata, df_metadata=df_metadata)
    log_counter = add_debug_trace(
        f'df.head() after applying metadata: {str(df.head().to_string())}',
        logger, endpoint_request, log_counter)

    df_metadata.drop_duplicates(subset=['Driftsmerking'], inplace=True)
    df = df.merge(df_metadata,
                  left_on=['station_name'],
                  right_on=['Driftsmerking'],
                  how='left')
    df.drop(['Driftsmerking'], axis=1, inplace=True)
    log_counter = add_debug_trace(
        f'df.head() after merging metadata: {str(df.head().to_string())}',
        logger, endpoint_request, log_counter)

    # Casting object type to columns
    df['aggregated_per_mp'] = df['aggregated_per_mp'].astype(float)
    df['station_name'] = df['station_name'].astype('category')
    df['fylkesnavn'] = df['fylkesnavn'].astype('category')
    df['long'] = df['long'].astype(float)
    df['lat'] = df['lat'].astype(float)
    log_counter = add_debug_trace(
        f'df.head() after setting dtypes: {str(df.head().to_string())}',
        logger, endpoint_request, log_counter)

    if time_zone == True:
        df = df.set_index('date_tz')
        # Convert to 'Europe/Oslo' time zone
        df.index = df.index.tz_convert(tz='Europe/Oslo')
        df.reset_index(inplace=True)
    log_counter = add_debug_trace(
        f'df.head() after timezone manipulation: {str(df.head().to_string())}',
        logger, endpoint_request, log_counter)
    log_counter = add_debug_trace(f'Final df.shape: {str(df.shape)}', logger,
                                  endpoint_request, log_counter)

    return df


def _remove_outliers(hourly_ser: pd.Series,
                     z_tolerance_low: int = -5,
                     z_tolerance_high: int = 5):
    '''
    # Function detects and removes outliers from the dataframe using a rolling window,
    # using a 30D history mean avrage together with z_score to evaluate if a datapoint is an outlier.
    '''

    THIRTY_DAYS_HOURS = 720
    #Rename column for formating purpose

    #Find 30D mean avrage using the previouse 30D history
    MA_30D = hourly_ser.rolling(THIRTY_DAYS_HOURS, center=True).mean()

    #Fill naN values occuring the first 30D of the dataframe using backwards filling
    MA_30D = MA_30D.fillna(method='bfill')

    #Compute z_score for each datapoint, and append in new column
    load_MA_30D_zscore = (hourly_ser - MA_30D) / (hourly_ser.std(ddof=0))

    #Evaluate if a datapoint is to many standard deviations away from the average mean. After tuning the tolerance is chosen
    #to be -2. Only detecting outliers that are too far below the 30D mean, NOT above. Dataframe column for outlier,
    #value either 1/0, TRUE/FALSE.
    outlier_below_idx = (load_MA_30D_zscore < z_tolerance_low).astype(int)
    outlier_above_idx = (load_MA_30D_zscore > z_tolerance_high).astype(int)

    #Find index of the detected outliers above and below mean
    outlier_below = np.where(outlier_below_idx == 1)[0]
    outlier_above = np.where(outlier_above_idx == 1)[0]

    #Give outliers naN value and interoplate using linear method.
    for i in outlier_below:
        hourly_ser.iat[i] = np.nan
    hourly_ser = hourly_ser.interpolate(method='linear')

    for i in outlier_above:
        hourly_ser.iat[i] = np.nan
    hourly_ser = hourly_ser.interpolate(method='linear')

    print("  removed outliers below: ", len(outlier_below), " and above: ",
          len(outlier_above))

    return hourly_ser


def add_debug_trace(message: str,
                    logger: Union[LogEntry, logging.Logger] = None,
                    endpoint_request: Optional[EndpointRequest] = None,
                    log_counter: Optional[int] = None):

    if log_counter:
        log_counter += 1
        message = f'{str(caller_name())} - {str(log_counter)}.: {message}'
    else:
        message = f'{str(caller_name())} - {message}'

    if logger and isinstance(logger, LogEntry) and endpoint_request:
        logger.debug(msg=message, endpoint_request=endpoint_request)
    elif logger:
        logger.debug(msg=message)

    return log_counter if log_counter else None


def caller_name() -> str:
    """Return the calling function's name."""
    # Ref: https://stackoverflow.com/a/57712700/
    return cast(FrameType,
                cast(FrameType, inspect.currentframe()).f_back).f_code.co_name
