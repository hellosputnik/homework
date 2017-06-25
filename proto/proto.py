#!/usr/bin/env python

import struct
import sys


# ==== Data Structures =========================================================

class Header(object):
    def __init__(self, magic_string, version, number_of_records):
        self.magic_string      = magic_string
        self.version           = ord(version)
        self.number_of_records = struct.unpack("!I", number_of_records)[0]


class Record(object):
    def __init__(self, rtype, timestamp, user_id):
        self.rtype             = ord(rtype)
        self.timestamp         = struct.unpack("!I", timestamp)[0]
        self.user_id           = struct.unpack("!Q", user_id)[0]

    def set_amount_in_dollars(self, amount_in_dollars):
        self.amount_in_dollars = struct.unpack("!d", amount_in_dollars)[0]


class Answers(object):
    def __init__(self):
        self.credits          = 0.0
        self.debits           = 0.0
        self.autopays_started = 0
        self.autopays_ended   = 0
        self.balance_of_user  = 0.0

# ==============================================================================


# ==== Helper Functions ========================================================

def parse(fin):
    # Read the header section.
    header = Header(fin.read(4), fin.read(1), fin.read(4))

    # Read the records (based on the information from the header).
    records = []
    for _ in xrange(header.number_of_records):
        # Read the record type, Unix timestamp, and user ID.
        record = Record(fin.read(1), fin.read(4), fin.read(8))

        # For record types of 0 or 1, read the amount in dollars.
        if record.rtype == 0 or record.rtype == 1:
            record.set_amount_in_dollars(fin.read(8))

        # Add record to list of records.
        records.append(record)

    # Return the parsed data.
    return records

# ==============================================================================


# ==== main ====================================================================

def main():
    # Get the number of arguments.
    argc = len(sys.argv)

    # Handle incorrect number of arguments.
    if argc != 2:
        print "Usage: python %s [file]" % sys.argv[0]
        return

    # Set the file name.
    file_name = sys.argv[1]

    # Open the file as an input stream and parse the file for the records.
    with open(file_name) as fin:
        records = parse(fin)

    # Note: The ledger does not seem to be necessary to answer the questions.
    # Create a ledger for the balances.
    # ledger = collections.defaultdict(float)

    # Iterate through each record and process the data.
    user_id = 2456938384156277127
    answers = Answers()
    for record in records:
        # 0x00: Debit
        if record.rtype == 0:
            answers.debits  += record.amount_in_dollars
            if record.user_id == user_id:
                print user_id, record.amount_in_dollars
                answers.balance_of_user -= record.amount_in_dollars
        # 0x01: Credit
        if record.rtype == 1:
            answers.credits += record.amount_in_dollars
            if record.user_id == user_id:
                print user_id, record.amount_in_dollars
                answers.balance_of_user += record.amount_in_dollars
        # 0x02: StartAutopay
        if record.rtype == 2:
            answers.autopays_started += 1
        # 0x03: EndAutopay
        if record.rtype == 3:
            answers.autopays_ended   += 1

    # Print the answers.
    print "The total amount in dollars of debit is $%.2f." % answers.debits
    print "The total amount in dollars of debit is $%.2f." % answers.credits
    print "%d autopays were started." % answers.autopays_started
    print "%d autopays were ended."   % answers.autopays_ended
    print "The balance of user ID %d is $%.2f." % (user_id, answers.balance_of_user)

# ==============================================================================


if __name__ == '__main__':
    main()

