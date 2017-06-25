from collections import defaultdict


PLANS = "plans.csv"
SLCSP = "slcsp.csv"
ZIPS  = "zips.csv"


def main():

    # ==== Plans ===============================================================

    # Read "plans.csv" for the data on plans, but do not process the data to
    # ensure the file I/O operation is completed ASAP. I can speed up data
    # processing, but I am not aware of techniques to speed up disk I/O.
    plans = []
    with open(PLANS) as lines:
        for line in lines:
            plans.append(line)

    # Process the data on plans by parsing the data using ',' as the delimiter
    # and filtering for plans whose metal_level is 'Silver'.
    plans = map(lambda data: data.strip().split(','), plans)
    plans = filter(lambda data: data[2] == "Silver", plans)

    # Construct a dictionary of rates using a state and rate_area tuple as the
    # key and a set of rates as the value. Using a data structure such as a min
    # heap instead of a set would lead to better performance.
    rates = defaultdict(set)
    for plan in plans:
        plan_id, state, _, rate, rate_area = plan
        rates[(state, rate_area)].add(float(rate))

    # Map sort() and list() to transform the dictionary of unsorted set of rates
    # to a dictionary of sorted list of rates.
    rates = { key: sorted(list(value)) for key, value in rates.iteritems() }

    # ==========================================================================


    # ==== Zip Code ============================================================

    # Read "zips.csv" for the data on zips. For the same reason described in the
    # Plans section, do not process the data until after the file I/O operations
    # is complete.
    mappings = []
    with open(ZIPS) as lines:
        for line in lines:
            mappings.append(line)

    # Process the data on zip code mappings to county code and rate area by
    # parsing the data using ',' as the delimiter.
    mappings = map(lambda data: data.strip().split(','), mappings)

    # For the zip code mapping data, we need to construct three dictionaries:
    #
    # 1. A dictionary that maps zip codes to a state and rate area tuple.
    # 2. A dictionary that maps counties to a state and rate area tuple.
    # 3. A dictionary that maps zip codes to counties.
    #
    # The first dictionary serves to translate a zip code into a state and rate
    # area which will be used to find the SLCSP of the zip code. If the zip code
    # does not exist in the first dictionary, then the third dictionary will be
    # used to translate the zip code to a county. And lastly, the second
    # dictionary will then use the resulting county to return a state and rate
    # area that may return a SLCSP.
    zips     = defaultdict(set)
    counties = defaultdict(set)
    z2c      = defaultdict(set)
    for mapping in mappings:
        zipcode, state, county_code, _, rate_area = mapping
        zips[zipcode].add((state, rate_area))
        counties[county_code].add((state, rate_area))
        z2c[zipcode].add(county_code)

    # ==========================================================================


    # ==== SLCSP ===============================================================

    # Read "slcsp.csv" for the data on the zip codes to be processed. For the
    # same reason described in the previous sections, do not process the data
    # until after the file I/O operation is complete.
    cases = []
    with open(SLCSP) as lines:
        for line in lines:
            cases.append(line)

    # Skip the case created by the "zipcode" header line. It would be prudent
    # to have a secondary function or a method in a class validate the CSV
    # file (and for all of the CSV files). This line of code is executed with
    # the assumption that the file is valid.
    cases = cases[1:]

    # Process the data on the zip codes to be processed by stripping the newline
    # and the ',' from the zip codes.
    cases = map(lambda x: x[:-2], cases)

    # Use the data processed in the previous sections (Plan and Zip Code) to
    # compute the SLCSP.
    slcsp = []
    for case in cases:

        # Zip codes must have exactly one rate_area for the rate to be
        # unambiguous and valid.
        if len(zips[case]) == 1:
            # Get the state and rate_area from the set, which should contain
            # one state and rate_area.
            state, rate_area = zips[case].pop()

            # If the state and rate area maps to a rate, append the rate.
            if (state, rate_area) in rates:
                slcsp.append("%s,%s" % (case, rates[(state, rate_area)][1]))
                continue

            # TODO: If the state and rate area do not map to a rate, can we use
            # the county_code to find a rate? This needs further clarification.
            else:
                pass

        # If the zip code has more than one rate_area or the state and rate
        # area are not associated with a rate, then do not concatenate anything
        # to the line.
        slcsp.append("%s," % case)

    # ==========================================================================


    # ==== Results =============================================================

    # Write to modified-slcsp.csv because it is too risky to overwrite the
    # original file. In the real world, I would create a backup or use versioned
    # files.
    with open("modified-slcsp.csv", 'w') as fout:

        # Write the field name for "slcsp.csv".
        fout.write("zipcode,rate\n")

        # Write the results to the file.
        for line in slcsp:
            fout.write("%s\n" % line)

    # ==========================================================================


if __name__ == '__main__':
    main()

