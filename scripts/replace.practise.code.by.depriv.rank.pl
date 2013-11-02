#!/usr/bin/perl -w

use strict;

my $postcodeFile = "/home/ole/src/how.poor.is.my.postcode/wkc.pc.imd.lookup.csv";

my %h = ();
open(IN,$postcodeFile) or die;
while(<IN>) {

    my $line = $_;
    #print $line;
    chomp($line);
    my @a = split(/,/,$line);
    $a[2] =~ s/"//g;
    #print STDERR $a[2]," => ",$a[-2],"\n";
    $h{$a[2]} = $a[-2];
}

close(IN);

my $prescriptionsFile = "T201307PDPI+BNFT_postcode.CSV";
open(IN,$prescriptionsFile) or die;
while(<IN>) {

    my $line=$_;
    chomp($line);
    if ($line =~ m/^ SHA/) {
        print $line,",IMD score\n";
        next;
    }
    my @f = split(/,/,$line);    
    if (defined $h{$f[2]}) {
        #$f[2] = $h{$f[2]};
        print join(",",@f),$h{$f[2]},"\n";
    }

}
close(IN);

