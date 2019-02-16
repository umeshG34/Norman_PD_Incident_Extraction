#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

import normanpd
from normanpd import normanpd

def main(url):
    # Download data
    normanpd.fetchincidents(url)

    # Extract Data
    incidents = normanpd.extractincidents()

    # Create Dataase
    normanpd.createdb()

    # Insert Data
    normanpd.populatedb(incidents)

    # Print Status
    db = 'normanpd.db' #Location of the normanpd.db
    normanpd.status(db)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--arrests", type=str, required=True,
                help="The arrest summary url.")
    
    args = parser.parse_args()
    if args.arrests:
            main(args.arrests)
