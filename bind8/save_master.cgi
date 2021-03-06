#!/usr/bin/perl
# save_master.cgi
# Save changes to master zone options in named.conf

require './bind8-lib.pl';
&ReadParse();
&error_setup($text{'master_err'});

$zone = &get_zone_name_or_error($in{'zone'}, $in{'view'});
$z = &zone_to_config($zone);
$zconf = $z->{'members'};
$dom = $zone->{'name'};
&can_edit_zone($zone) ||
	&error($text{'master_ecannot'});
$indent = $zone->{'view'} ? 2 : 1;

$access{'ro'} && &error($text{'master_ero'});
$access{'opts'} || &error($text{'master_eoptscannot'});
&lock_file(&make_chroot($z->{'file'}));

&save_choice("check-names", $z, $indent);
&save_choice("notify", $z, $indent);
&save_address("allow-update", $z, $indent);
&save_address("allow-transfer", $z, $indent);
&save_address("allow-query", $z, $indent);
&save_address("also-notify", $z, $indent);
&flush_file_lines();
&unlock_file(&make_chroot($z->{'file'}));
&webmin_log("opts", undef, $dom, \%in);
&redirect("edit_master.cgi?zone=$in{'zone'}&view=$in{'view'}");

