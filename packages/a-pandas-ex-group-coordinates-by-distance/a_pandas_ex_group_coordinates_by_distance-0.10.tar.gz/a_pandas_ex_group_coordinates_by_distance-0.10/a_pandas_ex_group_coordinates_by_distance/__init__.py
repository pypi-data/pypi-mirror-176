from typing import Union

import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame


def euclidean_distance(df1, df2, cols):
    return np.linalg.norm(df1[cols].values - df2[cols].values, axis=1)


def group_coordinates_by_distance(
    coordinates: Union[tuple, list, pd.DataFrame],
    max_euclidean_distance: Union[float, int] = 100,
) -> pd.DataFrame:
    if not isinstance(coordinates, pd.DataFrame):
        df4 = (
            pd.DataFrame.from_records(coordinates, columns=["x", "y"])
            .drop_duplicates()
            .reset_index(drop=True)
        )
    else:
        df4 = coordinates
        df4.columns = ["x", "y"]
    results = []
    for _ in range(len(df4)):
        tdf = pd.DataFrame(
            np.repeat(df4.iloc[_ : _ + 1].__array__(), len(df4)).reshape((2, -1))
        ).T
        tdf.columns = ["x", "y"]
        results.append(euclidean_distance(df1=tdf, df2=df4, cols=["x", "y"]))
    df = pd.DataFrame(results)

    alltogether = []
    for col in df.columns:
        tog = df4.loc[df.loc[df[col] < max_euclidean_distance].index]
        alltogether.append(tog.copy())

    donealready = []
    groupcoords = []
    dfcounter = 0
    for raa in range(len(alltogether)):
        groupcoordstemp = []
        for ra in range(len(alltogether)):
            if ra in donealready:
                continue
            gut = alltogether[ra].loc[
                (alltogether[ra]["x"].isin(alltogether[raa]["x"]))
                & (alltogether[ra]["y"].isin(alltogether[raa]["y"]))
            ]
            if gut.empty:
                continue
            donealready.append(ra)
            groupcoordstemp.append(gut.copy())
        if groupcoordstemp:
            groupcoords.append(
                pd.concat(groupcoordstemp.copy(), ignore_index=True)
                .drop_duplicates()
                .reset_index(drop=True)
                .assign(item=dfcounter)
            )
            dfcounter += 1
    df = pd.concat(groupcoords).reset_index(drop=True)
    df.columns = ["x", "y", "item"]
    return df


def pd_add_group_coordinates_by_distance():
    pd.Q_group_coordinates_by_distance_df = group_coordinates_by_distance
    DataFrame.d_group_coordinates_by_distance_df = group_coordinates_by_distance


# from a_pandas_ex_group_coordinates_by_distance import pd_add_group_coordinates_by_distance
# pd_add_group_coordinates_by_distance()
# import pandas as pd
# coordinates = [(745.8010864257812, 519.8585205078125),
#  (747.8574829101562, 522.5038452148438),
#  (747.9273071289062, 517.1298828125),
#  (747.9273071289062, 517.1298828125),
#  (750.921142578125, 522.3074951171875),
#  (756.1781005859375, 449.8744812011719),
#  (757.0703125, 461.237548828125),
#  (757.0703125, 461.237548828125),
#  (757.1057739257812, 438.6798095703125),
#  (830.8739624023438, 144.21884155273438),
#  (759.8501586914062, 435.39776611328125),
#  (759.8501586914062, 435.39776611328125),
#  (761.2493896484375, 468.02178955078125),
#  (761.2493896484375, 468.02178955078125),
#  (764.5658569335938, 521.395263671875),
#  (1079.3170166015625, 199.76937866210938),
#  (770.1127319335938, 474.63946533203125),
#  (770.3933715820312, 425.3490295410156),
#  (773.7312622070312, 516.6536254882812),
#  (776.908447265625, 515.5355224609375),
#  (776.908447265625, 515.5355224609375),
#  (778.0835571289062, 520.68896484375),
#  (779.8836059570312, 519.2072143554688),
#  (780.3491821289062, 420.33465576171875),
#  (780.3491821289062, 420.33465576171875),
#  (782.48388671875, 478.8080139160156),
#  (782.48388671875, 478.8080139160156),
#  (1083.74462890625, 151.22621154785156),
#  (1083.74462890625, 151.22621154785156),
#  (1083.74462890625, 151.22621154785156),
#  (1083.74462890625, 151.22621154785156),
#  (784.2761840820312, 478.5111083984375),
#  (759.8501586914062, 435.39776611328125),
#  (784.2761840820312, 478.5111083984375),
#  (819.1412353515625, 137.67359924316406),
#  (819.1412353515625, 137.67359924316406),
#  (819.1412353515625, 137.67359924316406),
#  (797.492919921875, 524.4356079101562),
#  (825.904541015625, 125.7273941040039),
#  (826.0745849609375, 149.3106231689453),
#  (800.8538818359375, 446.9717102050781),
#  (800.8538818359375, 446.9717102050781),
#  (801.9922485351562, 517.8736572265625),
#  (801.9922485351562, 517.8736572265625),
#  (802.3947143554688, 520.4193725585938),
#  (802.3947143554688, 520.4193725585938),
#  (804.0225830078125, 519.9164428710938),
#  (804.0225830078125, 519.9164428710938),
#  (808.3038940429688, 431.790771484375),
#  (808.3038940429688, 431.790771484375),
#  (809.5233154296875, 464.2477722167969),
#  (809.5233154296875, 464.2477722167969),
#  (812.5013427734375, 438.7483825683594),
#  (813.3584594726562, 449.6587829589844)]
#
# df=pd.Q_group_coordinates_by_distance_df(coordinates=coordinates,max_euclidean_distance=100)
#
# df2=pd.DataFrame(coordinates)
# df2.d_group_coordinates_by_distance_df()
