from mpmath import mp

def n_of_pi_decimals(n):
    n = int(n)

    # Set the number of decimal places
    mp.dps = n + 2

    # Store Pi with the set precision
    pi_value = str(mp.pi)

    # Write Pi to a text file
    with open("npi_decimals.txt", "w") as f:
        f.write(pi_value)

def frac_of_pi_decimals(frac,n):
    n = int(n)

    # Set the number of decimal places
    mp.dps = n + 2

    # Store Pi with the set precision
    pi_value = str(mp.pi*frac)

    # Write Pi to a text file
    with open("timepi_decimals.txt", "w") as f:
        f.write(pi_value)