#!/usr/bin/perl
# save_gsync.cgi
# Save default quotas for groups

require './quota-lib.pl';
&ReadParse();
$access{'default'} && &can_edit_filesys($in{'filesys'}) ||
	&error($text{'ssync_ecannot'});
$bsize = &block_size($in{'filesys'});
&lock_file("$module_config_directory/config");
$v = join(' ', &quota_parse("sblocks", $bsize),
	       &quota_parse("hblocks", $bsize),
	       ($in{'sfiles_def'} ? 0 : $in{'sfiles'}),
	       ($in{'hfiles_def'} ? 0 : $in{'hfiles'}) );
$k = "gsync_$in{'filesys'}";
if ($v eq "0 0 0 0") { delete($config{$k}); }
else { $config{$k} = $v; }
&write_file("$module_config_directory/config", \%config);
&unlock_file("$module_config_directory/config");
&webmin_log("sync", "group", $in{'filesys'}, \%in);
&redirect("list_groups.cgi?dir=".&urlize($in{'filesys'}));

