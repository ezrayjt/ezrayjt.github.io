import azure.functions as func
import mysql.connector, json, os, requests

class DatabaseManager:
    def __init__(self, host, user, password, database):
        # Initialize a connection to the MySQL database
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
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

    return DatabaseManager(
    host="ta21-2023s2.mysql.database.azure.com",
    user="TA21",
    password=db_password,
    database=db_name
    )

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Run a function that triggers every 5 minutes to prevent the function from going to sleep mode
# Runs only between 10pm to 5pm UTC which means in our timezone (AEST, UTC+10) it will be allowed to sleep from 3am to 8am
@app.schedule(schedule="0 */5 22-23,0-16 * * *", arg_name="timer")
def stayinalive(timer: func.TimerRequest):
    requests.get("https://ta21-2023-s2.azurewebsites.net/api/get_data")

@app.route()
def get_data(req: func.HttpRequest):
    db_manager = get_database_manager("energy")

    # SQL query to get data from the database
    query = "SELECT region_name, financial_start_year + 1, ROUND(electricity_usage), ROUND(gas_usage), ROUND(non_renewable_electricity_total), ROUND(renewable_electricity_total), ROUND(total_electricity_generation), ROUND(total_gas_generation) FROM regions JOIN energy_consumption USING (region_id) JOIN energy_generation USING (region_id, financial_start_year)"

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

# Route to get incandescent light bulb data for iteration 2
@app.route('get_incandescent', methods=['GET'])
def get_data_incandescent(req: func.HttpRequest):
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
            # no unit for efficiency so can sort based on the efficiency for the frontend
            'efficiency': efficiency
        })

    db_manager_iteration2.close()
    result_json = json.dumps(data)
    return func.HttpResponse(
      result_json,
      mimetype="application/json"
    )

# Route to get CFL data for iteration 2
@app.route('get_CFL', methods=['GET'])
def get_data_CFL(req: func.HttpRequest):
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
            'x-coordinate': x,
            'y-coordinate': y,
            'type': facility_management_type,
            'sub-type': facility_infrastructure_type,
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
