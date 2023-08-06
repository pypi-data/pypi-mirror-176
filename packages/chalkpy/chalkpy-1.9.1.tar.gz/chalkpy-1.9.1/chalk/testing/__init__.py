import polars.testing

from chalk.features import DataFrame


def assert_frame_equal(a: DataFrame, b: DataFrame):
    return polars.testing.assert_frame_equal(a.to_polars().collect(), b.to_polars().collect())
