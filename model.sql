CREATE OR REPLACE MODEL `project-493921.airplane.flight_delay_model_fast`
OPTIONS(
  model_type='logistic_reg',
  input_label_cols=['predicted_is_delayed'],
  max_iterations=20,
  early_stop=TRUE,
  min_rel_progress=0.01,
  ls_init_learn_rate=0.1,
  data_split_method='AUTO'
) AS
SELECT
  predicted_is_delayed,
  Reporting_Airline,
  Origin,
  Dest,
  CRSDepTime,
  AvgPrecip,
  AvgVisibility,
  AvgWindSpeed
FROM
  `project-493921.airplane.airportweather_cleaned`
