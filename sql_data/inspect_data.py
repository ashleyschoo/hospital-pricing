import logging
import os
import pandas as pd
import sys as sys


def main(argv=None):
	"""
	Utilize Pandas library to read in  DRG_Prices.csv file
	(tab delimited) hospital information .csv file (tab delimited).
	Extract regions, sub-regions, intermediate regions, country and areas, and
	other column data.  Filter out duplicate values and NaN values and sort the
	series in alphabetical order. Write out each series to a .csv file for inspection.
	"""
	if argv is None:
		argv = sys.argv

	msg = [
		'Source file read {0}',	#0
		'DRG Prices DRG Code written to file {0}',	#1
		'DRG Prices DRG Definition written to file {0}',	#2
		'DRG Prices Hospital Street Address written to file {0}',	#3
		'DRG Prices Hospital Zip Code written to file {0}',	#4				
		'DRG Prices Average Covered Charges written to file {0}',	#5
		'Hospital Information: Name written to file {0}',	#6
		'Hospital Information: Address  written to file {0}',	#7
		'Hospital Information: City written to file {0}',		#8
		'Hospital Information: State written to file {0}',		#9
		'Hospital Information: Zip Code written to file {0}',		#10
		'Hospital Information: Hospital Ownership written to file {0}',	#11
		'Hospital Information: Hospital Overall Score written to file {0}',	#12
		'Hospital Information: Hospital Safety Score written to file {0}',	#13	
		'Hospital Information: Hospital Readmission Score written to file {0}',	#14		
		'Poverty Zip Code written to file {0}',	#15
		'Poverty Zip Code Designation written to file {0}'	#16

	]

	# Setting logging format and default level
	logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

	# Read in DRG_Prices CMS data set
	drg_prices_csv = './input/drg_prices.csv'
	drg_data_frame = read_csv(drg_prices_csv, '\t')
	logging.info(msg[0].format(os.path.abspath(drg_prices_csv)))

	# Write DRG Code to a .csv file.
	drg_code = extract_filtered_series(drg_data_frame, 'DRG_Code')
	drg_code_csv = './output/drg_code.csv'
	write_series_to_csv(drg_code, drg_code_csv, '\t', False)
	logging.info(msg[1].format(os.path.abspath(drg_code_csv)))

	# Write DRG Definition to a .csv file.
	drg_def = extract_filtered_series(drg_data_frame, 'DRG Definition')
	drg_def_csv = './output/drg_def.csv'
	write_series_to_csv(drg_def, drg_def_csv, '\t', False)
	logging.info(msg[2].format(os.path.abspath(drg_def_csv)))

	# # Write Provider Street Address to a .csv file.
	prv_street_address = extract_filtered_series(drg_data_frame, 'Provider Street Address')
	prv_street_address_csv = './output/prv_street_address.csv'
	write_series_to_csv(prv_street_address, prv_street_address_csv, '\t', False)
	logging.info(msg[3].format(os.path.abspath(prv_street_address_csv)))

	# # Write Provider Zip to a .csv file.
	prv_zip = extract_filtered_series(drg_data_frame, 'Provider Zip Code')
	prv_zip_csv = './output/prv_zip.csv'
	write_series_to_csv(prv_zip, prv_zip_csv, '\t', False)
	logging.info(msg[4].format(os.path.abspath(prv_zip_csv)))

	# Write Average Covered Charges to a .csv file.
	drg_charge = extract_filtered_series(drg_data_frame, 'Average Covered Charges')
	drg_charge_csv = './output/drg_charge.csv'
	write_series_to_csv(drg_charge, drg_charge_csv, '\t', False)
	logging.info(msg[5].format(os.path.abspath(drg_charge_csv)))

	# Read Hospital Information data (tabbed separator)
	hospital_info_csv = './input/hospital_info.csv'
	hospital_data_frame = read_csv(hospital_info_csv, '\t')
	logging.info(msg[0].format(os.path.abspath(hospital_info_csv)))

	# Write hospital name to a .csv file
	hosp_name = extract_filtered_series(hospital_data_frame, 'Hospital Name')
	hosp_name_csv = './output/hosp_name.csv'
	write_series_to_csv(hosp_name, hosp_name_csv, '\t', False)
	logging.info(msg[6].format(os.path.abspath(hosp_name_csv)))

	# Write hospital address to a .csv file
	hosp_address = extract_filtered_series(hospital_data_frame, 'Address')
	hosp_address_csv = './output/hosp_address.csv'
	write_series_to_csv(hosp_address, hosp_address_csv, '\t', False)
	logging.info(msg[7].format(os.path.abspath(hosp_address_csv)))

	# Write hospital city to a .csv file
	hosp_city = extract_filtered_series(hospital_data_frame, 'City')
	hosp_city_csv = './output/hosp_city.csv'
	write_series_to_csv(hosp_city, hosp_city_csv, '\t', False)
	logging.info(msg[8].format(os.path.abspath(hosp_city_csv)))

	# Write hospital state to a .csv file
	hosp_state = extract_filtered_series(hospital_data_frame, 'State')
	hosp_state_csv = './output/hosp_state.csv'
	write_series_to_csv(hosp_state, hosp_state_csv, '\t', False)
	logging.info(msg[9].format(os.path.abspath(hosp_state_csv)))

	# Write hospital zip code to a .csv file
	hosp_zip = extract_filtered_series(hospital_data_frame, 'ZIP Code')
	hosp_zip_csv = './output/hosp_zip.csv'
	write_series_to_csv(hosp_zip, hosp_zip_csv, '\t', False)
	logging.info(msg[10].format(os.path.abspath(hosp_zip_csv)))

	# Write hospital ownership to a .csv file
	hosp_owner = extract_filtered_series(hospital_data_frame, 'Hospital Ownership')
	hosp_owner_csv = './output/hosp_owner.csv'
	write_series_to_csv(hosp_owner, hosp_owner_csv, '\t', False)
	logging.info(msg[11].format(os.path.abspath(hosp_owner_csv)))

	# Write hospital overall rating to a .csv file
	hosp_score = extract_filtered_series(hospital_data_frame, 'Hospital overall rating')
	hosp_score_csv = './output/hosp_score.csv'
	write_series_to_csv(hosp_score, hosp_score_csv, '\t', False)
	logging.info(msg[12].format(os.path.abspath(hosp_score_csv)))

	# Write hospital safety of care national comparison to a .csv file
	hosp_safety = extract_filtered_series(hospital_data_frame, 'Safety of care national comparison')
	hosp_safety_csv = './output/hosp_safety.csv'
	write_series_to_csv(hosp_safety, hosp_safety_csv, '\t', False)
	logging.info(msg[13].format(os.path.abspath(hosp_safety_csv)))

	# Write hospital readmission rate national comparison to a .csv file
	hosp_readmit = extract_filtered_series(hospital_data_frame, 'Readmission national comparison')
	hosp_readmit_csv = './output/hosp_readmit.csv'
	write_series_to_csv(hosp_readmit, hosp_readmit_csv, '\t', False)
	logging.info(msg[14].format(os.path.abspath(hosp_readmit_csv)))

	# Read Poverty Information data (tabbed separator)
	poverty_info_csv = './input/zip_code_designation.csv'
	poverty_data_frame = read_csv(poverty_info_csv, '\t')
	logging.info(msg[0].format(os.path.abspath(poverty_info_csv)))

	# Write poverty zip code to a .csv file
	pov_zip = extract_filtered_series(poverty_data_frame, 'ZIP')
	pov_zip = './output/pov_zip.csv'
	write_series_to_csv(pov_zip, pov_zip_csv, '\t', False)
	logging.info(msg[15].format(os.path.abspath(pov_zip_csv)))

	# Write poverty zip code designation to a .csv file
	pov_des = extract_filtered_series(poverty_data_frame, 'Zip Code Designation')
	pov_des_csv = './output/pov_des.csv'
	write_series_to_csv(pov_des, pov_des_csv, '\t', False)
	logging.info(msg[16].format(os.path.abspath(pov_des_csv)))		

def extract_filtered_series(data_frame, column_name):
	"""
	Returns a filtered Panda Series one-dimensional ndarray from a targeted column.
	Duplicate values and NaN or blank values are dropped from the result set which is
	returned sorted (ascending).
	:param data_frame: Pandas DataFrame
	:param column_name: column name string
	:return: Panda Series one-dimensional ndarray
	"""
	return data_frame[column_name].drop_duplicates().dropna().sort_values()


def read_csv(path, delimiter=','):
	"""
	Utilize Pandas to read in *.csv file.
	:param path: file path
	:param delimiter: field delimiter
	:return: Pandas DataFrame
	"""
	return pd.read_csv(path, sep=delimiter, engine='python')


def write_series_to_csv(series, path, delimiter=',', row_name=True):
	"""
	Write Pandas DataFrame to a *.csv file.
	:param series: Pandas one dimensional ndarray
	:param path: file path
	:param delimiter: field delimiter
	:param row_name: include row name boolean
	"""
	series.to_csv(path, sep=delimiter, index=row_name)


if __name__ == '__main__':
	sys.exit(main())