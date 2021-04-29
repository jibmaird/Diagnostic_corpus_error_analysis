#!/usr/bin/perl -w

# Instructions: https://bitbucket.org/nicta_biomed/brateval/src/master/

use strict;

my $gold = "/Users/david/Projects/Diagnostic_corpus_error_analysis/experiments/ner/gold/7";

my $pred_bert = "/Users/david/Projects/Diagnostic_corpus_error_analysis/experiments/ner/current/7/prediction_only";
my $pred_crf = "/Users/david/Projects/Diagnostic_corpus_error_analysis/experiments/ner/crf/7/prediction_only";


chdir("/Users/david/Projects/brateval/target");

system("java -cp brateval-0.3.0-SNAPSHOT.jar au.com.nicta.csp.brateval.CompareEntities -v $pred_bert $gold");
