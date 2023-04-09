from countryinfo import CountryInfo as Info
while True:
    country = Info(input('Enter country: ')).info()
    print(f'''
Name : {country['name']}
Capital : {country['capital']}
Region : {country['region']}   
Population : {country['population']}
Language : {country['languages']}
TimeZones : {country['timezones']}
Area : {country['area']} km²
Wiki : {country['wiki']}
''')
