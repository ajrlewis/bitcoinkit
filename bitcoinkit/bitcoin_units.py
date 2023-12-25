SATOSHIS_PER_BITCOIN = 100_000_000
MILLI_SATOSHIS_PER_SATOSHI = 1_000


def bitcoins_to_satoshis(bitcoins):
    return int(bitcoins * SATOSHIS_PER_BITCOIN)


def satoshis_to_bitcoins(satoshis):
    return satoshis / SATOSHIS_PER_BITCOIN


def satoshis_to_millisatoshis(satoshis):
    return satoshis * MILLI_SATOSHIS_PER_SATOSHI


def millisatoshis_to_satoshis(millisatoshis):
    return millisatoshis / MILLI_SATOSHIS_PER_SATOSHI


def main():
    bitcoins = 0.5
    satoshis = bitcoins_to_satoshis(bitcoins)
    print(f"{bitcoins} bitcoins is equal to {satoshis:,} satoshis")

    satoshis = 50_000_000
    bitcoins = satoshis_to_bitcoins(satoshis)
    print(f"{satoshis:,} satoshis is equal to {bitcoins} bitcoins")

    satoshis = 1_000_000
    millisatoshis = satoshis_to_millisatoshis(satoshis)
    print(f"{satoshis:,} satoshis is equal to {millisatoshis:,} millisatoshis")

    millisatoshis = 1_000_000
    satoshis = millisatoshis_to_satoshis(millisatoshis)
    print(f"{millisatoshis:,} millisatoshis is equal to {satoshis} satoshis")


if __name__ == "__main__":
    main()
