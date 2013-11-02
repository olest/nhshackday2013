#!/usr/bin/perl -w

use strict;

my $postcodeFile = "T201307ADDR+BNFT_postcode.CSV";

my %h = ();
open(IN,$postcodeFile) or die;
while(<IN>) {

    my $line = $_;
    chomp($line);
    my ($id,$postCode) = split(/,/,$line);

    $id =~ s/\s+$//g; 
    #print STDERR "$id => $postCode\n";
    $h{$id} = $postCode;

}

close(IN);

my $prescriptionsFile = "T201307PDPI+BNFT.CSV";
open(IN,$prescriptionsFile) or die;
while(<IN>) {

    my $line=$_;
    chomp($line);
    if ($line =~ m/^ SHA/) {
        print;
        next;
    }
    my @f = split(/,/,$line);    
    $f[2] = $h{$f[2]};
    print join(",",@f),"\n";

}
close(IN);

