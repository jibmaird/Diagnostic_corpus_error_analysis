#!/usr/bin/perl -w

use strict;

chdir("/home/dmiraola/Diagnostic_corpus_error_analysis/experiments/ner/gold");
for(my $i=2;$i<=9;$i++) {
    system("cp -r /aitu-stor/ajimeno/ai4eye/ai4eye-nlp/data/$i/data/testing $i");
}
