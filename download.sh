#!/bin/bash

while read p; do
  wget "$p"
done <./DNAnexus_export_urls-20191012-013633.txt