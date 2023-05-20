import configparser

# Specify the file path
file_path = '../configfiles/machineConfig.ini'

# Read the file content
with open(file_path, 'r') as file:
    file_content = file.read()

# Create a ConfigParser object and read the content
config = configparser.ConfigParser()
config.read_string(file_content)

# Get the values of timezone and UTC
timezone = config.get('timezone', 'timezone')
utc = config.get('timezone', 'UTC')

# Print the values
print('Timezone:', timezone)
print('UTC:', utc)