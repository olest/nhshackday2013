#!/usr/bin/perl -w

use strict;

#use String::Util 'trim';

my $postcodeFile = "T201307ADDR+BNFT_name.CSV";

my %h = ();
open(IN,$postcodeFile) or die;
while(<IN>) {

    my $line = $_;
    chomp($line);
    my ($name,$postCode) = split(/,/,$line);

    #print STDERR "$id => $postCode\n";
    $name =~ s/\s+$//g;
    $h{$name} = $postCode;

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

