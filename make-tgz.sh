#!/bin/bash
cd reports/final_paper
make
cd ../../
cp reports/final_paper/main.pdf robinett-royer-report.pdf
tar zcf robinett-royer-source.tar.gz $(git ls-files)
