#!/usr/bin/perl -w

use strict;

my $post2LsoaFile = "PCD11_OA11_LSOA11_MSOA11_LAD11_EW_LU.csv";
# "L19 7NE","L19  7NE","E00033887","E01006686","Liverpool 053E","E02001399","Liverpool 053","E08000012","Liverpool","",0

my $imd2PostcodeFile = "1871524.csv";
# LSOA CODE,LA CODE,LA NAME,GOR CODE,GOR NAME,IMD SCORE,RANK OF IMD SCORE (where 1 is most deprived)
# E01000001,00AA,City of London,H,London,6.16,28814
# E01000002,00AA,City of London,H,London,5.59,29450

my %h=();
open(IN,$post2LsoaFile) or die;
while(<IN>) {
    my $line=$_;    
    chomp($line);
    my @a=split(/,/,$line);
    my $pc = $a[0];
    my $l = $a[3];
    $pc =~ s/\s//g;
    $pc =~ s/"//g;
    $l =~ s/"//g;
    #print $pc," => ",$l,"\n";
    $h{$l} = $pc;
}
close(IN);


open(IN,$imd2PostcodeFile) or die;
while(<IN>) {
    my $line=$_;
    chomp($line);
    if (m/LSOA/) {
        print $line,"\n"; next;
    }
    my @a=split(/,/,$line);
    my $pc = $a[0];
    $pc =~ s/\s//g;
    $pc =~ s/"//g;
    if (exists $h{$pc}) {
        print $line,",",$h{$pc},"\n";
    } else {
        print "no entry for $pc\n";
    }
}
close(IN);
