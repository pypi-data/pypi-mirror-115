# statsnz

A collection of functions to enable ease of use of the various Stats New Zealand APIs, in python.

Installion:

  pip install statsnz



Examples:


Geocoding:


  To get the region with a set of coordinates:

    from statsnz import statsnz

    region_example = statsnz("YOUR_API_KEY").get_region(-41.242,172.323)


  Or TLA:

    region_example = statsnz("YOUR_API_KEY").get_tla(-41.242,172.323)

  Or DHB:

      region_example = statsnz("YOUR_API_KEY").get_dhb(-41.242,172.323)



  Or a custom layer:

    region_example = statsnz("YOUR_API_KEY").get_custom(-41.242,172.323)


Odata API:


    from statsnz import statsnz

    statsnz = statsnz("YOUR_API_KEY")
    service = 'https://api.stats.govt.nz/opendata/v1'
    endpoint = 'EmploymentIndicators'
    entity = 'Resources'
    query_option = "10" ##Top 10 records



    Observations = statsnz.get_odata_api(service, endpoint, entity, query_option)
