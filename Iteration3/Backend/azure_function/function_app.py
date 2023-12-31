import azure.functions as func
import mysql.connector, json, os, requests

class DatabaseManager:
    def __init__(self, host, user, password, database):
        # Initialize a connection to the MySQL database
        self.connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        # Create a cursor object to interact with the database
        self.cursor = self.connection.cursor()

    def execute_query(self, query):
        # Execute the provided SQL query using the cursor
        self.cursor.execute(query)
        # Fetch the results of the query
        result = self.cursor.fetchall()
        return result

    def close(self):
        # Close the cursor and the database connection
        self.cursor.close()
        self.connection.close()

def get_database_manager(db_name: str):
    db_password = os.environ["mysql_database"]
    return DatabaseManager(host="ta21-2023s2.mysql.database.azure.com", user="TA21", password=db_password, database=db_name)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Run a function that triggers every 5 minutes to prevent the function from going to sleep mode
# Runs only between 10pm to 5pm UTC which means in our timezone (AEST, UTC+10) it will be allowed to sleep from 3am to 8am
@app.schedule(schedule="0 */5 22-23,0-16 * * *", arg_name="timer")
def stayinalive(timer: func.TimerRequest):
    return

@app.route('get_data')
def get_data_energy(req: func.HttpRequest):
    db_manager = get_database_manager("energy")

    # SQL query to get data from the database
    query = "SELECT region_name, financial_start_year + 1, ROUND(electricity_usage) / 1000, ROUND(gas_usage), ROUND(non_renewable_electricity_total) / 1000, ROUND(renewable_electricity_total) / 1000, ROUND(total_electricity_generation) / 1000, ROUND(total_gas_generation) FROM regions JOIN energy_consumption USING (region_id) JOIN energy_generation USING (region_id, financial_start_year)"

    # Execute the query using the DatabaseManager
    result = db_manager.execute_query(query)

    # Process the query result and format it as JSON
    data = [{
            'region': region,
            'financial year': year,
            'electricity_usage': electricity_usage,
            'gas_usage': gas_usage,
            'non_renewable_source_electricity_generated': elect_non_renewable_generated,
            'renewable_source_electricity_generated': elect_renewable_generated,
            'total_electricity_generated': total_elect_generated,
            'total_gas_generated': total_gas_generated
        } for region, year, electricity_usage, gas_usage, elect_non_renewable_generated, elect_renewable_generated, total_elect_generated, total_gas_generated in result]

    db_manager.close()
    result_json = json.dumps(data)
    
    return func.HttpResponse(
      result_json,
      mimetype="application/json"
    )

### Iteration 2

# Route to get incandescent light bulb data for iteration 2
@app.route(methods=['GET'])
def get_incandescent(req: func.HttpRequest):
    db_manager_iteration2 = get_database_manager("iteration2")

    # SQL query to get data from the database
    query = "SELECT i.brand, i.model_number, i.lamp_power_watts, ROUND(i.lamp_light_lumens), i.lamp_life_hours, GROUP_CONCAT(m.manufacturer_country) AS country_list, ROUND(i.lamp_light_lumens / i.lamp_power_watts) AS efficiency FROM incandescents i JOIN incandescent_manufacturing m ON i.ID = m.incandescent_ID GROUP BY i.brand, i.model_number, i.lamp_power_Watts, i.lamp_light_lumens, i.lamp_life_hours"

    # Execute the query using the DatabaseManager
    result = db_manager_iteration2.execute_query(query)

    # Process the query result and format it as JSON
    data = []
    for each in result:
        brand = each[0].title()
        model_number = each[1]
        lamp_power_watts = each[2]
        lamp_light_lumens = each[3]
        lamp_life_hours = each[4]
        country_list = each[5]
        efficiency = each[6]

        data.append({
            'brand': brand,
            'model': model_number,
            'power': lamp_power_watts,
            'brightness': lamp_light_lumens,
            'life': lamp_life_hours,
            'manufacturer_country': country_list,
            # no unit for efficiency so we can sort based on the efficiency for the frontend
            'efficiency': efficiency
        })

    db_manager_iteration2.close()
    result_json = json.dumps(data)
    return func.HttpResponse(
      result_json,
      mimetype="application/json"
    )

# Route to get CFL data for iteration 2
@app.route(methods=['GET'])
def get_CFL(req: func.HttpRequest):
    db_manager_iteration2 = get_database_manager("iteration2")

    # SQL query to get data from the database
    query = "SELECT brand, model_number, manufacturer_country, lamp_power_watts, ROUND(lamp_light_lumens), colour_temperature, lamp_life_hours, ROUND(lamp_light_lumens / lamp_power_watts) FROM CFLs"

    # Execute the query using the DatabaseManager
    result = db_manager_iteration2.execute_query(query)

    # Process the query result and format it as JSON
    data = []
    for each in result:
        brand = each[0].title()
        model_number = each[1]
        manufacturer_country = each[2]
        lamp_power_watts = each[3]
        lamp_light_lumens = each[4]
        colour_temperature = each[5]
        lamp_life_hours = each[6]
        efficiency = each[7]

        data.append({
            'brand': brand,
            'model': model_number,
            'power': lamp_power_watts,
            'brightness': lamp_light_lumens,
            'life': lamp_life_hours,
            'manufacturer_country': manufacturer_country,
            'colour_temperature': colour_temperature,
            # no unit for efficiency so can sort based on the efficiency for the frontend
            'efficiency': efficiency
        })

    db_manager_iteration2.close()
    result_json = json.dumps(data)
    return func.HttpResponse(
      result_json,
      mimetype="application/json"
    )

# Route to get waste management facilities data for iteration 2
@app.route('get_waste_mgmt_facilities', methods=['GET'])
def get_data_waste_facilities(req: func.HttpRequest):
    db_manager_iteration2 = get_database_manager("iteration2")

    # SQL query to get data from the database
    query = "SELECT x, y, facility_management_type, facility_infrastructure_type, facility_owner, facility_name, state_or_territory, address, suburb, postcode FROM waste_management_facilities"

    # Execute the query using the DatabaseManager
    result = db_manager_iteration2.execute_query(query)

    # Process the query result and format it as JSON
    data = []
    for each in result:
        x = each[0]
        y = each[1]
        facility_management_type = each[2].title()
        facility_infrastructure_type = each[3].title()
        facility_owner = each[4].title()
        facility_name = each[5].title()
        state_or_territory = each[6]
        address = each[7].title()
        suburb = each[8].title()
        postcode = each[9]

        data.append({
            'longitude': x,
            'latitude': y,
            'type': facility_management_type,
            'subtype': facility_infrastructure_type,
            'owner': facility_owner,
            'name': facility_name,
            'state': state_or_territory,
            'address': address,
            'suburb': suburb,
            'postcode': postcode
        })

    db_manager_iteration2.close()
    result_json = json.dumps(data)
    return func.HttpResponse(
      result_json,
      mimetype="application/json"
    )

### Iteration 3

# Route to get refrigerators data
@app.route(methods=['GET'])
def get_refrigerators(req: func.HttpRequest):
    db_manager_iteration3 = get_database_manager("iteration3")

    # SQL query to get data from the database
    # query = "SELECT brand, model_number, is_refrigerator, is_freezer, energy_usage_kwh_per_month, total_volume_litres, star_rating FROM Refrigerators"
    query = "SELECT brand, CASE WHEN is_refrigerator = 1 AND is_freezer = 1 THEN 'Fridge&Freezer' WHEN is_refrigerator = 1 AND is_freezer = 0 THEN 'Fridge' ELSE 'Freezer' END AS 'type', ROUND(AVG(energy_usage_kwh_per_month), 3) AS average_energy_consumption, star_rating, CASE WHEN total_volume_litres <= 200 THEN 'Small' WHEN total_volume_litres <= 350 THEN 'Medium' WHEN total_volume_litres <= 500 THEN 'Large' ELSE 'Extra Large' END AS volume_category FROM Refrigerators GROUP BY brand, type, volume_category, star_rating ORDER BY count(*) DESC, brand, type, star_rating, volume_category"

    # Execute the query using the DatabaseManager
    result = db_manager_iteration3.execute_query(query)
    
    # Process the query result and format it as JSON
    data = []
    for each in result:
        brand = each[0].title()
        type = each[1]
        average_energy_consumption = float(each[2])
        star_rating = float(each[3])
        volume_category = each[4].title()

        data.append({
            'brand': brand,
            'type': type,
            'average_energy_consumption' : average_energy_consumption,
            'star_rating': star_rating,
            'volume_category': volume_category
        })

    db_manager_iteration3.close()
    return func.HttpResponse(
      json.dumps(data),
      mimetype="application/json"
    )

@app.route('get_fridge_avg_consumption', methods=['GET'])
def get_data_fridge_avg_consumption(req: func.HttpRequest):
    db_manager_iteration3 = get_database_manager("iteration3")

    # SQL query to get data from the database
    query = "SELECT CASE WHEN is_refrigerator = 1 AND is_freezer = 1 THEN 'Fridge&Freezer' WHEN is_refrigerator = 1 AND is_freezer = 0 THEN 'Fridge' ELSE 'Freezer' END AS 'type', ROUND(AVG(energy_usage_kwh_per_month), 3) AS average_energy_consumption, star_rating FROM Refrigerators GROUP BY type, star_rating ORDER BY type, star_rating"

    # Execute the query using the DatabaseManager
    result = db_manager_iteration3.execute_query(query)

    # Process the query result and format it as JSON
    data = []
    for each in result:
        type = each[0].title()
        average_energy_consumption = float(each[1])
        star_rating = float(each[2])

        data.append({
            'type': type,
            'Star Rating': star_rating,
            'Average Energy Consumption (kW)' : average_energy_consumption,
        })

    db_manager_iteration3.close()
    return func.HttpResponse(
      json.dumps(data),
      mimetype="application/json"
    )

@app.route(methods=['GET'])
def get_fridge_highest_rating_consumption(req: func.HttpRequest):
    db_manager_iteration3 = get_database_manager("iteration3")
    
    # SQL query to get data from the database
    query = "WITH RankedRefrigerators AS (SELECT CASE WHEN is_refrigerator = 1 AND is_freezer = 1 THEN 'Fridge&Freezer' WHEN is_refrigerator = 1 AND is_freezer = 0 THEN 'Fridge' ELSE 'Freezer' END AS 'type', ROUND(AVG(energy_usage_kwh_per_month), 3) AS average_energy_consumption, star_rating, ROW_NUMBER() OVER (PARTITION BY CASE WHEN is_refrigerator = 1 AND is_freezer = 1 THEN 'Fridge&Freezer' WHEN is_refrigerator = 1 AND is_freezer = 0 THEN 'Fridge' ELSE 'Freezer' END ORDER BY star_rating DESC) AS RowNum FROM Refrigerators GROUP BY CASE WHEN is_refrigerator = 1 AND is_freezer = 1 THEN 'Fridge&Freezer' WHEN is_refrigerator = 1 AND is_freezer = 0 THEN 'Fridge' ELSE 'Freezer' END, star_rating) SELECT type, average_energy_consumption, star_rating FROM RankedRefrigerators WHERE RowNum = 1 ORDER BY type"

    # Execute the query using the DatabaseManager
    result = db_manager_iteration3.execute_query(query)

    # Process the query result and format it as JSON
    data = []
    for each in result:
        type = each[0].title()
        average_energy_consumption = float(each[1])
        star_rating = float(each[2])

        data.append({
            'type': type,
            'Star Rating': star_rating,
            'Average Energy Consumption (kW)' : average_energy_consumption,
        })

    db_manager_iteration3.close()
    return func.HttpResponse(
      json.dumps(data),
      mimetype="application/json"
    )

# Route to get air conditioners data
@app.route(methods=['GET'])
def get_ac_cooling(req: func.HttpRequest):
    db_manager_iteration3 = get_database_manager("iteration3")

    # SQL query to get data from the database
    # query = "SELECT brand, model_number, cooling_usage_kw, heating_usage_kw, ROUND(cooling_star_rating,1), ROUND(heating_star_rating,1) FROM air_conditioners"
    query = "SELECT brand, ROUND(AVG(cooling_usage_kw),3)*30, ROUND(cooling_star_rating,1) FROM air_conditioners GROUP BY brand, cooling_star_rating"

    # Execute the query using the DatabaseManager
    result = db_manager_iteration3.execute_query(query)

    # Process the query result and format it as JSON
    data = []
    for each in result:
        brand = each[0].title()
        average_energy_consumption = float(each[1])
        star_rating = float(each[2])

        data.append({
            'brand': brand,
            'average_energy_consumption':average_energy_consumption,
            'star_rating': star_rating
        })

    db_manager_iteration3.close()
    return func.HttpResponse(
      json.dumps(data),
      mimetype="application/json"
    )

@app.route(methods=['GET'])
def get_ac_heating(req: func.HttpRequest):
    db_manager_iteration3 = get_database_manager("iteration3")

    # SQL query to get data from the database
    query = "SELECT brand, ROUND(AVG(heating_usage_kw),3), ROUND(heating_star_rating,1) FROM air_conditioners GROUP BY brand, heating_star_rating"

    # Execute the query using the DatabaseManager
    result = db_manager_iteration3.execute_query(query)

    # Process the query result and format it as JSON
    data = []
    for each in result:
        brand = each[0].title()
        average_energy_consumption = float(each[1])
        star_rating = float(each[2])

        data.append({
            'brand': brand,
            'average_energy_consumption': average_energy_consumption,
            'star_rating': star_rating
        })

    db_manager_iteration3.close()
    return func.HttpResponse(
      json.dumps(data),
      mimetype="application/json"
    )

@app.route(methods=['GET'])
def get_ac_cooling_avg_consumption(req: func.HttpRequest):
    db_manager_iteration3 = get_database_manager("iteration3")

    # SQL query to get data from the database
    query = "SELECT ROUND(AVG(cooling_usage_kw), 3) AS average_energy_consumption, ROUND(cooling_star_rating,1) AS cooling_star_rating FROM air_conditioners GROUP BY cooling_star_rating HAVING cooling_star_rating >= 1.0 ORDER BY cooling_star_rating"

    # Execute the query using the DatabaseManager
    result = db_manager_iteration3.execute_query(query)

    # Process the query result and format it as JSON
    data = []
    for each in result:
        average_energy_consumption = float(each[0])
        star_rating = float(each[1])

        data.append({
            'Star Rating': star_rating,
            'Average Energy Consumption (kW)' : average_energy_consumption,
        })

    db_manager_iteration3.close()
    return func.HttpResponse(
      json.dumps(data),
      mimetype="application/json"
    )

@app.route(methods=['GET'])
def get_ac_heating_avg_consumption(req: func.HttpRequest):
    db_manager_iteration3 = get_database_manager("iteration3")

    # SQL query to get data from the database
    query = "SELECT ROUND(AVG(heating_usage_kw), 3) AS average_energy_consumption, ROUND(heating_star_rating,1) AS heating_star_rating FROM air_conditioners GROUP BY heating_star_rating HAVING heating_star_rating >= 1.0 ORDER BY heating_star_rating"

    # Execute the query using the DatabaseManager
    result = db_manager_iteration3.execute_query(query)

    # Process the query result and format it as JSON
    data = []
    for each in result:
        average_energy_consumption = float(each[0])
        star_rating = float(each[1])

        data.append({
            'Star Rating': star_rating,
            'Average Energy Consumption (kW)' : average_energy_consumption,
        })

    db_manager_iteration3.close()
    return func.HttpResponse(
      json.dumps(data),
      mimetype="application/json"
    )

@app.route(methods=['GET'])
def get_ac_heating_highest_rating_consumption(req: func.HttpRequest):
    db_manager_iteration3 = get_database_manager("iteration3")

    # SQL query to get data from the database
    query = "SELECT ROUND(AVG(heating_usage_kw), 3) AS average_energy_consumption, ROUND(heating_star_rating,1) AS heating_star_rating FROM air_conditioners GROUP BY heating_star_rating HAVING heating_star_Rating >= 1.0 ORDER BY heating_star_rating DESC LIMIT 1"

    # Execute the query using the DatabaseManager
    result = db_manager_iteration3.execute_query(query)

    # Process the query result and format it as JSON
    data = []
    for each in result:
        average_energy_consumption = float(each[0])
        star_rating = float(each[1])

        data.append({
            'Star Rating': star_rating,
            'Average Energy Consumption (kW)' : average_energy_consumption,
        })

    db_manager_iteration3.close()
    return func.HttpResponse(
      json.dumps(data),
      mimetype="application/json"
    )

@app.route(methods=['GET'])
def get_ac_cooling_highest_rating_consumption(req: func.HttpRequest):
    db_manager_iteration3 = get_database_manager("iteration3")

    # SQL query to get data from the database
    query = "SELECT ROUND(AVG(cooling_usage_kw), 3) AS average_energy_consumption, ROUND(cooling_star_rating,1) AS cooling_star_rating FROM air_conditioners GROUP BY cooling_star_rating HAVING cooling_star_Rating >= 1.0 ORDER BY cooling_star_rating DESC LIMIT 1"

    # Execute the query using the DatabaseManager
    result = db_manager_iteration3.execute_query(query)

    # Process the query result and format it as JSON
    data = []
    for each in result:
        average_energy_consumption = float(each[0])
        star_rating = float(each[1])

        data.append({
            'Star Rating': star_rating,
            'Average Energy Consumption (kW)' : average_energy_consumption,
        })

    db_manager_iteration3.close()
    return func.HttpResponse(
      json.dumps(data),
      mimetype="application/json"
    )